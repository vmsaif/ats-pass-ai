from datetime import datetime
from prettytable import PrettyTable
import os
import sqlite3
import time
from path.output_file_paths import PATHS

class Limiter:
    # Constants for rate limits
    # Gemini 1.5 pro
    LLM_LARGE_RPM_LIMIT = 2
    LLM_LARGE_TOKEN_PER_MINUTE_LIMIT = 32000
    LLM_LARGE_DAILY_REQUEST_LIMIT = 50

    # Gemini 1.0 pro
    LLM_SMALL_RPM_LIMIT = 15
    LLM_SMALL_TOKEN_PER_MINUTE_LIMIT = 32000
    LLM_SMALL_DAILY_REQUEST_LIMIT = 1500

    # Paid, Comment out for free version
    LLM_LARGE_RPM_LIMIT = 360
    LLM_LARGE_TOKEN_PER_MINUTE_LIMIT = 2000000
    LLM_LARGE_DAILY_REQUEST_LIMIT = 10000

    LLM_SMALL_RPM_LIMIT = 360
    LLM_SMALL_TOKEN_PER_MINUTE_LIMIT = 120000
    LLM_SMALL_DAILY_REQUEST_LIMIT = 30000
    # ----------------------------

    # Time constants
    SECONDS_IN_MINUTE = 65
    SECONDS_IN_DAY = 86400

    # Database configuration
    DB_DIR = PATHS['limiter_db_dir']

    def __init__(self, llm_size: str, llm, langchainMethods: bool = True):
        self.langchainMethods = langchainMethods
        self.llm = llm
        self.llm_size = llm_size.upper()
        self._set_limits(llm_size)
        self._config_db()

    def request_limiter(self, output):
        timestamp = datetime.now().timestamp()
        # Check if RPM limit is reached
        if self._count_requests_in_last_period('minute') >= self.llm_rpm_limit:
            print(f"RPM limit exceeded. Waiting {self.SECONDS_IN_MINUTE} seconds to start next minute.")
            time.sleep(self.SECONDS_IN_MINUTE)  # Sleep 1 minute
            return False  # Indicate that RPM limit was exceeded
        if self._count_requests_in_last_period('day') >= self.llm_daily_request_limit:
            print("Daily limit exceeded. Do you want to continue?")
            answer = input("Enter 'yes' to continue, or 'no' to stop: ")
            if answer.lower() != 'yes':
                return False
        
        self._record_request(timestamp)
        return True  # Request processed successfully

    def _set_limits(self, llm_size: str):
        if llm_size == 'LARGE':
            self.llm_rpm_limit = self.LLM_LARGE_RPM_LIMIT
            self.llm_daily_request_limit = self.LLM_LARGE_DAILY_REQUEST_LIMIT
            self.llm_token_per_minute_limit = self.LLM_LARGE_TOKEN_PER_MINUTE_LIMIT
        elif llm_size == 'SMALL':
            self.llm_rpm_limit = self.LLM_SMALL_RPM_LIMIT
            self.llm_daily_request_limit = self.LLM_SMALL_DAILY_REQUEST_LIMIT
            self.llm_token_per_minute_limit = self.LLM_SMALL_TOKEN_PER_MINUTE_LIMIT
        elif llm_size == 'ANY':
            print("Using None for LLM size. Limits will not be set.")
        else:
            raise ValueError("Invalid LLM size. Must be either 'LARGE' or 'SMALL'")

    def _config_db(self):
        if not os.path.exists(self.DB_DIR):
            os.makedirs(self.DB_DIR)
        db_path = PATHS['limiter_db_file']
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Requests (
                request_time TEXT,
                llm_size TEXT
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Tokens (
                usage_time REAL,
                tokens_used INTEGER,
                llm_size TEXT
            )
        ''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def _record_request(self, timestamp):
        self.cursor.execute('INSERT INTO Requests (request_time, llm_size) VALUES (?, ?)', (timestamp, self.llm_size))
        self.conn.commit()

    def record_token_usage(self, output):
        if(self._count_tokens_in_last_minute() >= self.llm_token_per_minute_limit):
            print(f"Token limit exceeded. Waiting {self.SECONDS_IN_MINUTE} seconds to start next minute.")
            time.sleep(self.SECONDS_IN_MINUTE)

        # now, we can proceed to record the token usage and thus the program.
        if(self.langchainMethods):
            tokens_used = self.llm.get_num_tokens(output.raw_output)
        else:
            # langchainMethods is False, meaning it is a direct gemini model. This is a llm_task.py file call.
            token_dict_from_gemini = self.llm.count_tokens(contents = output)
            tokens_used = token_dict_from_gemini.total_tokens
            
        timestamp = datetime.now().timestamp()
        self.cursor.execute('INSERT INTO Tokens (usage_time, tokens_used, llm_size) VALUES (?, ?, ?)', (timestamp, tokens_used, self.llm_size))
        self.conn.commit()
        return True

    def _count_tokens_in_last_minute(self):
        current_timestamp = datetime.now().timestamp()
        period_start_timestamp = current_timestamp - self.SECONDS_IN_MINUTE

        self.cursor.execute('SELECT SUM(tokens_used) FROM Tokens WHERE usage_time >= ? AND llm_size = ?', 
                            (period_start_timestamp, self.llm_size))
        
        result = self.cursor.fetchone()[0]
        if result is None:
            result = 0
        return result

    def _count_requests_in_last_period(self, period):
        current_timestamp = datetime.now().timestamp()
        period_start_timestamp = current_timestamp - (self.SECONDS_IN_MINUTE if period == 'minute' else self.SECONDS_IN_DAY)
        
        self.cursor.execute('SELECT COUNT(*) FROM Requests WHERE request_time >= ? AND llm_size = ?', 
                            (period_start_timestamp, self.llm_size))
        result = self.cursor.fetchone()
        if result is None:
            result = 0
        else:
            result = result[0]
        return result

# class ends here

def printRemainingRequestsPerDay():
    for size in ['SMALL', 'LARGE']:
        limiter = Limiter(size, None, False)
        # Use the appropriate daily request limit based on the size of the LLM
        if size == 'SMALL':
            rpd_remaining = limiter.LLM_SMALL_DAILY_REQUEST_LIMIT - limiter._count_requests_in_last_period('day')
        elif size == 'LARGE':
            rpd_remaining = limiter.LLM_LARGE_DAILY_REQUEST_LIMIT - limiter._count_requests_in_last_period('day')
        
        print(f"{size} LLM Remaining RPD: {rpd_remaining}")


def time_stamp_to_human_readable(time_stamp):
    return datetime.fromtimestamp(time_stamp).strftime('%Y-%m-%d %H:%M:%S')

def print_rpd_table(llm_size: str = None, upto: int = 100):
    # Printing Requests table

    if(llm_size == None):
        # get upto requests
        execute_string = f"SELECT * FROM Requests ORDER BY llm_size ASC, request_time DESC LIMIT {upto}"
    else:
        execute_string = f"SELECT * FROM Requests where llm_size = '{llm_size}' ORDER BY request_time DESC LIMIT {upto}"

    limiter = Limiter('ANY', None, False)

    # Printing Requests table
    limiter.cursor.execute(execute_string)
    requests = limiter.cursor.fetchall()
    requests_table = PrettyTable()
    requests_table.field_names = ["#", "Request Time", "LLM Size"]
    for i, row in enumerate(requests, start=1):
        # Convert the timestamp to a human-readable format
        human_readable_time = time_stamp_to_human_readable(float(row[0]))
        requests_table.add_row([i, human_readable_time, row[1]])
    print("Requests Table:")
    print(requests_table)
    print(f"\nLimited output to {upto} entries.\n")

def print_token_table():
    limiter = Limiter('ANY', None, False)
    current_time = datetime.now()
    sum_window = current_time.timestamp() - Limiter.SECONDS_IN_DAY # 24 hours ago
    
    # Printing Tokens table
    limiter.cursor.execute("SELECT * FROM Tokens ORDER BY llm_size ASC, usage_time DESC")
    tokens = limiter.cursor.fetchall()
    tokens_table = PrettyTable()
    tokens_table.field_names = ["#", "Usage Time", "Tokens Used", "LLM Size"]
    for i, row in enumerate(tokens, start=1):
        # Convert the timestamp to a human-readable format
        human_readable_time = time_stamp_to_human_readable(float(row[0]))
        tokens_table.add_row([i, human_readable_time, row[1], row[2]])
    print("Tokens Table:")
    print(tokens_table)

    # Calculate and print the sum of tokens used in the last 24 hours
    limiter.cursor.execute("""
        SELECT llm_size, SUM(tokens_used)
        FROM Tokens
        WHERE usage_time >= ?
        GROUP BY llm_size
        """, (sum_window,)) # last comma is necessary for a single-element tuple
    sum_tokens = limiter.cursor.fetchall()
    sum_table = PrettyTable()
    sum_table.field_names = ["LLM Size", "Tokens Used in Last 24 Hours"]
    for row in sum_tokens:
        sum_table.add_row(row)
    print("Sum of Tokens Used in Last 24 Hours:")
    print(sum_table)

def cleanTable():
    print("\nCleaning table...\n")
    limiter = Limiter('ANY', None, False)
    limiter.cursor.execute('DELETE FROM Requests WHERE llm_size = "SMALL"')
    limiter.conn.commit()

    limiter.cursor.execute('DELETE FROM Requests WHERE llm_size = "LARGE"')
    limiter.conn.commit()

if __name__ == '__main__':
    # printRemainingRequestsPerDay()
    print_rpd_table('LARGE', 50)
    # print_token_table()