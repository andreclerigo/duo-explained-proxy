import os
from sqlite_web import SQLiteWeb

DB_FILE = "data/usage_logs.db"

def main():
    os.makedirs("data", exist_ok=True)
    print(f"🌐 SQLite Web Admin running for {DB_FILE}")
    SQLiteWeb(db_path=DB_FILE, host="0.0.0.0", port=5002, readonly=True).run()

if __name__ == "__main__":
    main()
