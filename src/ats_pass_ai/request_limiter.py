# Author: Saif Mahmud
# Date: 2024-05-20

# Purpose: This module is used to limit the number of requests made to the LLM API to avoid hitting the free tier limits. At the moment of writing this, I am only using 2 llms in my main program, one with a large limit and one with a small limit. If more llm is needed, then just follow the init(str) method and add more limits. 

import datetime
import os
import time
import sqlite3

class RequestLimiter:

    # gemini 1.5 pro free tier limits
    LLM_LARGE_RPM_LIMIT = 2
    LLM_LARGE_DAILY_REQUEST_LIMIT = 50
    
    # gemini 1.0 free tier limits
    LLM_SMALL_RPM_LIMIT = 15
    LLM_SMALL_DAILY_REQUEST_LIMIT = 1500
    
    SECONDS = 60
    DAY_IN_SECONDS = 86400
    
    DB_DIR = 'custom_db'
    DB_FILE_LARGE_LLM = 'request_limiter_large_llm.db'
    DB_FILE_SMALL_LLM = 'request_limiter_small_llm.db'

    def __init__(self, llm_size: str):
        self.last_request_time = time.time()
        self.request_count = 0

        self.setLimits(llm_size)
        self.configDB(llm_size)
        self.request_count_today, self.first_request_time = self.get_todays_count()
        
        if not self.first_request_time or (time.time() - self.first_request_time) > self.DAY_IN_SECONDS:  # 86400 seconds in 24 hours
            self.reset_counts()

    def setLimits(self, llm_size: str):
        if(llm_size == 'large'):
            self.llm_rpm_limit = self.LLM_LARGE_RPM_LIMIT
            self.llm_daily_request_limit = self.LLM_LARGE_DAILY_REQUEST_LIMIT
        elif (llm_size == 'small'):
            self.llm_rpm_limit = self.LLM_SMALL_RPM_LIMIT
            self.llm_daily_request_limit = self.LLM_SMALL_DAILY_REQUEST_LIMIT
        else:
            raise ValueError("Invalid LLM size. Must be either 'large' or 'small'")

    def configDB(self, llm_size: str):
        # create_db_dir if not os.path.exists(self.DB_DIR)
        if not os.path.exists(self.DB_DIR):
            os.makedirs(self.DB_DIR)

        if(llm_size == 'large'):
            self.conn = sqlite3.connect(os.path.join(self.DB_DIR, self.DB_FILE_LARGE_LLM))
        elif (llm_size == 'small'):
            self.conn = sqlite3.connect(os.path.join(self.DB_DIR, self.DB_FILE_SMALL_LLM))
        else:
            raise ValueError("Invalid LLM size. Must be either 'large' or 'small'")
        
        try:
            self.cursor = self.conn.cursor()
            self.setup_database()
        except Exception as e:
            print("Error: ", e)
            raise
        return False
    # Destructor
    def __del__(self):
        self.conn.close()

    def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS Requests (
                date TEXT PRIMARY KEY,
                count INTEGER DEFAULT 0,
                first_request_time REAL
            )
        ''')
        self.conn.commit()

    def get_todays_count(self):
        now = time.time()
        today_str = datetime.date.today().strftime('%Y-%m-%d')
        self.cursor.execute('SELECT count, first_request_time FROM Requests WHERE date = ?', (today_str,))
        row = self.cursor.fetchone()
        if row:
            return row[0], row[1]
        else:
            self.cursor.execute('INSERT INTO Requests (date, count, first_request_time) VALUES (?, 0, ?)', (today_str, now))
            self.conn.commit()
            return 0, now

    def update_count(self, new_count):
        today_str = datetime.date.today().strftime('%Y-%m-%d')
        self.cursor.execute('UPDATE Requests SET count = ? WHERE date = ?', (new_count, today_str))
        self.conn.commit()

    def reset_counts(self):
        now = time.time()
        today_str = datetime.date.today().strftime('%Y-%m-%d')
        self.cursor.execute('UPDATE Requests SET count = 0, first_request_time = ? WHERE date = ?', (now, today_str))
        self.conn.commit()
        self.request_count_today = 0
        self.first_request_time = now  # Update the start of the new 24-hour period

    def run(self, output):
        now = time.time()
        # First check if the daily limit has been reached
        if not self.check_rpd(self.llm_daily_request_limit, self.request_count_today, now):
            # Means the daily limit has been reached
            # ask the user if they want to proceed or stop the execution
            read = input("Do you want to proceed anyway? (yes/no): ")
            if read.lower() != 'yes':
                print("Stopping execution.")
                return False

        # Check for per-minute limit
        if self.request_count >= self.llm_rpm_limit and (now - self.last_request_time < self.SECONDS):
            # If the per-minute limit has been reached, sleep for the remaining time then reset the count
            time_to_sleep = self.SECONDS - (now - self.last_request_time)
            print(f"Sleeping for {time_to_sleep:.2f} seconds")
            time.sleep(time_to_sleep)
            self.request_count = 0

        self.request_count += 1
        self.request_count_today += 1
        self.update_count(self.request_count_today)
        self.last_request_time = now
        return True

    def check_rpd(self, rpd_limit, request_count_today, now) -> bool:

        # Check if it passed 24 hours since the first request 
        if (now - self.first_request_time) > self.DAY_IN_SECONDS:
            self.reset_counts()
            self.first_request_time = now  # Update the start of the new 24-hour period
        if request_count_today >= rpd_limit:
            print("Daily request limit reached.")
            return False
        return True
    

