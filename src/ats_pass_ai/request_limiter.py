from datetime import datetime, timedelta
import os
import sqlite3
import time

class RequestLimiter:
    # Constants for rate limits
    # Gemini 1.5 pro
    LLM_LARGE_RPM_LIMIT = 2
    LLM_LARGE_DAILY_REQUEST_LIMIT = 50

    # Gemini 1.0 pro
    LLM_SMALL_RPM_LIMIT = 15
    LLM_SMALL_DAILY_REQUEST_LIMIT = 1500

    # Time constants
    SECONDS_IN_MINUTE = 60
    SECONDS_IN_DAY = 86400

    # Database configuration
    DB_DIR = 'custom_db'
    DB_FILE = 'request_limiter.db'

    def __init__(self, llm_size: str):
        self.llm_size = llm_size.upper()
        self._set_limits(llm_size)
        self._config_db()

    def run(self, output):
        timestamp = datetime.now().timestamp()
        # Check if RPM limit is reached
        if self._count_requests_in_last_period('minute') >= self.llm_rpm_limit:
            time_to_wait = self.SECONDS_IN_MINUTE
            print(f"RPM limit exceeded. Waiting {time_to_wait} seconds to start next minute.")
            time.sleep(time_to_wait)  # Sleep 1 minute
            return False  # Indicate that RPM limit was exceeded
        if self._count_requests_in_last_period('day') >= self.llm_daily_request_limit:
            print("Daily limit exceeded. Do you want to continue?")
            answer = input("Enter 'yes' to continue, or 'no' to stop: ")
            if answer.lower() != 'yes':
                return False
        
        self._record_request(timestamp)
        return True  # Request processed successfully

    # def _calculate_time_to_next_minute(self, current_time):
    #     """Calculate the time remaining to the start of the next minute."""
    #     seconds_current_minute = current_time % 60  # Find out how many seconds have passed in the current minute
    #     seconds_until_next_minute = 60 - seconds_current_minute  # Calculate how many seconds are left until the next minute
    #     return seconds_until_next_minute
    
    def _set_limits(self, llm_size: str):
        if llm_size == 'LARGE':
            self.llm_rpm_limit = self.LLM_LARGE_RPM_LIMIT
            self.llm_daily_request_limit = self.LLM_LARGE_DAILY_REQUEST_LIMIT
        elif llm_size == 'SMALL':
            self.llm_rpm_limit = self.LLM_SMALL_RPM_LIMIT
            self.llm_daily_request_limit = self.LLM_SMALL_DAILY_REQUEST_LIMIT
        else:
            raise ValueError("Invalid LLM size. Must be either 'LARGE' or 'SMALL'")

    def _config_db(self):
        if not os.path.exists(self.DB_DIR):
            os.makedirs(self.DB_DIR)
        db_path = os.path.join(self.DB_DIR, self.DB_FILE)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Requests (
                request_time TEXT,
                llm_size TEXT
            )
        ''')
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def _record_request(self, timestamp):
        self.cursor.execute('INSERT INTO Requests (request_time, llm_size) VALUES (?, ?)', (timestamp, self.llm_size))
        self.conn.commit()

    def _count_requests_in_last_period(self, period):
        current_timestamp = datetime.now().timestamp()
        period_start_timestamp = current_timestamp - (self.SECONDS_IN_MINUTE if period == 'minute' else self.SECONDS_IN_DAY)
        
        self.cursor.execute('SELECT COUNT(*) FROM Requests WHERE request_time >= ? AND llm_size = ?', 
                            (period_start_timestamp, self.llm_size))
        return self.cursor.fetchone()[0]

def printRemainingRequestsPerDay():
    for size in ['SMALL', 'LARGE']:
        limiter = RequestLimiter(size)
        # Use the appropriate daily request limit based on the size of the LLM
        if size == 'SMALL':
            rpd_remaining = limiter.LLM_SMALL_DAILY_REQUEST_LIMIT - limiter._count_requests_in_last_period('day')
        elif size == 'LARGE':
            rpd_remaining = limiter.LLM_LARGE_DAILY_REQUEST_LIMIT - limiter._count_requests_in_last_period('day')
        
        print(f"{size} LLM Remaining RPD: {rpd_remaining}")

def printWholeTable():
    limiter = RequestLimiter('SMALL')
    limiter.cursor.execute('SELECT COUNT(*) FROM Requests WHERE llm_size = "SMALL"')
    print("\nSmall LLM:\n")
    for row in limiter.cursor.fetchall():
        print(row)

    limiter = RequestLimiter('LARGE')
    limiter.cursor.execute('SELECT * FROM Requests WHERE llm_size = "LARGE"')
    print("\nLarge LLM:\n")
    for row in limiter.cursor.fetchall():
        print(row)

def cleanTable():
    print("\nCleaning table...\n")
    limiter = RequestLimiter('SMALL')
    limiter.cursor.execute('DELETE FROM Requests WHERE llm_size = "SMALL"')
    limiter.conn.commit()

    limiter = RequestLimiter('LARGE')
    limiter.cursor.execute('DELETE FROM Requests WHERE llm_size = "LARGE"')
    limiter.conn.commit()

# if __name__ == '__main__':
#     RequestLimiter.printRemainingRequestsPerDay()
#     printWholeTable()