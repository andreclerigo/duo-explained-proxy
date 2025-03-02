import sqlite3
import datetime

class UsageLoggerSQLite:
    def __init__(self, db_file):
        self.db_file = db_file
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS request_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source TEXT,
                    prompt TEXT,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS daily_usage (
                    date TEXT PRIMARY KEY,
                    request_count INTEGER
                )
            ''')
            conn.commit()

    def log_request(self, source: str, prompt: str):
        today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        with sqlite3.connect(self.db_file) as conn:
            conn.execute('INSERT INTO request_logs (source, prompt) VALUES (?, ?)', (source, prompt))
            conn.execute('''
                INSERT INTO daily_usage (date, request_count)
                VALUES (?, 1)
                ON CONFLICT(date) DO UPDATE SET request_count = request_count + 1
            ''', (today,))
            conn.commit()

    def get_daily_count(self):
        today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
        with sqlite3.connect(self.db_file) as conn:
            row = conn.execute('SELECT request_count FROM daily_usage WHERE date = ?', (today,)).fetchone()
            return row[0] if row else 0

    def is_within_limit(self, limit: int) -> bool:
        return self.get_daily_count() < limit

    def get_logs(self, limit=50):
        with sqlite3.connect(self.db_file) as conn:
            rows = conn.execute('''
                SELECT source, prompt, timestamp
                FROM request_logs
                ORDER BY timestamp DESC
                LIMIT ?
            ''', (limit,)).fetchall()
        return [{"source": r[0], "prompt": r[1], "timestamp": r[2]} for r in rows]
