from datetime import datetime, timedelta
import os
import sqlite3

class RequestLimiter:
    # Constants for rate limits
    LLM_LARGE_RPM_LIMIT = 2
    LLM_LARGE_DAILY_REQUEST_LIMIT = 50
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
        now = datetime.now()
        if self._count_requests_in_last_period('minute') >= self.llm_rpm_limit:
            return False  # RPM limit exceeded
        if self._count_requests_in_last_period('day') >= self.llm_daily_request_limit:
            return False  # Daily limit exceeded
        
        self._record_request(now)
        return True  # Request processed successfully

    def _set_limits(self, llm_size: str):
        if llm_size == 'large':
            self.llm_rpm_limit = self.LLM_LARGE_RPM_LIMIT
            self.llm_daily_request_limit = self.LLM_LARGE_DAILY_REQUEST_LIMIT
        elif llm_size == 'small':
            self.llm_rpm_limit = self.LLM_SMALL_RPM_LIMIT
            self.llm_daily_request_limit = self.LLM_SMALL_DAILY_REQUEST_LIMIT
        else:
            raise ValueError("Invalid LLM size. Must be either 'large' or 'small'")

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

    def _record_request(self, request_time):
        self.cursor.execute('INSERT INTO Requests (request_time, llm_size) VALUES (?, ?)', (request_time.isoformat(), self.llm_size))
        self.conn.commit()

    def _count_requests_in_last_period(self, period):
        now = datetime.now()
        if period == 'minute':
            period_start = now - timedelta(seconds=self.SECONDS_IN_MINUTE)
        elif period == 'day':
            period_start = now - timedelta(seconds=self.SECONDS_IN_DAY)
        else:
            raise ValueError("Invalid period specified. Must be 'minute' or 'day'")

        self.cursor.execute('SELECT COUNT(*) FROM Requests WHERE request_time >= ? AND llm_size = ?', (period_start.isoformat(), self.llm_size))
        return self.cursor.fetchone()[0]

def printRemainingRequestsPerDay():
    limiter = RequestLimiter('small')
    rpd_remaining = limiter.LLM_SMALL_DAILY_REQUEST_LIMIT - limiter._count_requests_in_last_period('day')
    print(f"Small LLM Remaining RPD: {rpd_remaining}")

    limiter = RequestLimiter('large')
    rpd_remaining = limiter.LLM_LARGE_DAILY_REQUEST_LIMIT - limiter._count_requests_in_last_period('day')
    print(f"Large LLM Remaining RPD: {rpd_remaining}")
