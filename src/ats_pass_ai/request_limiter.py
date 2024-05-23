
from datetime import timedelta
import os
import time
import sqlite3

class RequestLimiter:
    # Constants for limits
    LLM_LARGE_RPM_LIMIT = 2
    LLM_LARGE_DAILY_REQUEST_LIMIT = 50
    LLM_SMALL_RPM_LIMIT = 15
    LLM_SMALL_DAILY_REQUEST_LIMIT = 1500
    SECONDS = 60
    DAY_IN_SECONDS = 86400

    # Database configuration
    DB_DIR = 'custom_db'
    DB_FILE_LARGE_LLM = 'request_limiter_large_llm.db'
    DB_FILE_SMALL_LLM = 'request_limiter_small_llm.db'

    def __init__(self, llm_size: str):
        self.last_request_time = time.time()
        self.request_count = 0
        self._set_limits(llm_size)
        self._config_db(llm_size)
        self.request_count_today, self.first_request_time = self._get_todays_count()

    def run(self, output):
        now = time.time()
        self._check_and_reset()  # Ensures that counts are reset if the time has exceeded 24 hours

        if self.request_count >= self.llm_rpm_limit and (now - self.last_request_time < self.SECONDS):
            time_to_sleep = self.SECONDS - (now - self.last_request_time)
            time.sleep(time_to_sleep)
            self.request_count = 0

        self.request_count += 1
        self.request_count_today += 1
        self._update_count(self.request_count_today)
        self.last_request_time = now
        return True

    def _set_limits(self, llm_size: str):
        if llm_size == 'large':
            self.llm_rpm_limit = self.LLM_LARGE_RPM_LIMIT
            self.llm_daily_request_limit = self.LLM_LARGE_DAILY_REQUEST_LIMIT
        elif llm_size == 'small':
            self.llm_rpm_limit = self.LLM_SMALL_RPM_LIMIT
            self.llm_daily_request_limit = self.LLM_SMALL_DAILY_REQUEST_LIMIT
        else:
            raise ValueError("Invalid LLM size. Must be either 'large' or 'small'")

    def _config_db(self, llm_size: str):
        if not os.path.exists(self.DB_DIR):
            os.makedirs(self.DB_DIR)
        db_path = os.path.join(self.DB_DIR, getattr(self, f"DB_FILE_{llm_size.upper()}_LLM"))
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._setup_database()

    def __del__(self):
        self.conn.close()

    def _setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Requests (
                count INTEGER DEFAULT 0,
                first_request_time REAL
            )
        ''')
        self.conn.commit()

    def _get_todays_count(self):
        self.cursor.execute('SELECT count, first_request_time FROM Requests')
        row = self.cursor.fetchone()
        if row:
            return row
        else:
            now = time.time()
            self.cursor.execute('INSERT INTO Requests (count, first_request_time) VALUES (0, ?)', (now,))
            self.conn.commit()
            return 0, now

    def _update_count(self, new_count):
        self.cursor.execute('UPDATE Requests SET count = ?', (new_count,))
        self.conn.commit()

    def _check_and_reset(self):
        now = time.time()
        self.cursor.execute('SELECT count, first_request_time FROM Requests')
        row = self.cursor.fetchone()
        if row:
            first_request_time = row[1]
            time_since_first_request = now - first_request_time
            if time_since_first_request > self.DAY_IN_SECONDS:
                self._reset_counts(now)


    def _reset_counts(self, now):
        # Reset count and update first_request_time for the new 24-hour window
        try:
            # Start a transaction explicitly
            self.conn.execute('BEGIN TRANSACTION')
            self.cursor.execute('UPDATE Requests SET count = 0, first_request_time = ?', (now,))
            self.conn.commit()
            self.request_count_today = 0
            self.first_request_time = now
        except sqlite3.OperationalError as e:
            print(f"Error in reset_counts: {e}")
            self.conn.rollback()  # Rollback the transaction if an error occurs
  
#   Not making a class method
def printDailyLimitRemaining():
    now = time.time()

    for llm_size, daily_limit in [
        ('large', RequestLimiter.LLM_LARGE_DAILY_REQUEST_LIMIT),
        ('small', RequestLimiter.LLM_SMALL_DAILY_REQUEST_LIMIT)
    ]:
        db_file = getattr(RequestLimiter, f"DB_FILE_{llm_size.upper()}_LLM")
        db_path = os.path.join(RequestLimiter.DB_DIR, db_file)
        try:
            with sqlite3.connect(db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT count, first_request_time FROM Requests')
                row = cursor.fetchone()

                if row:
                    first_request_time = row[1]
                    time_since_first_request = now - first_request_time
                    remaining_requests = daily_limit - row[0]
                    time_remaining_until_reset = RequestLimiter.DAY_IN_SECONDS - time_since_first_request
                else:
                    # If no data found, assume no requests have been made yet
                    remaining_requests = daily_limit
                    time_remaining_until_reset = RequestLimiter.DAY_IN_SECONDS

                days, hours, minutes, seconds = convert_seconds(time_remaining_until_reset)
                print(f"{llm_size.capitalize()} LLM: requests remaining: {remaining_requests} with time until reset: {hours} hours, {minutes} minutes, {seconds} seconds")

        except Exception as e:
            print(f"Error connecting to {llm_size.capitalize()} LLM database: {e}")

def convert_seconds(seconds):
# Create a timedelta object from the number of seconds
    td = timedelta(seconds=seconds)
    
    # Extract days, hours, minutes, and seconds from the timedelta object
    days = td.days
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return days, hours, minutes, seconds 