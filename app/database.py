import sqlite3

database = "/Users/muhxmmadharis/Desktop/Exam_Rag_Project/test.db"

create_table = """
CREATE TABLE IF NOT EXISTS uploaded_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    original_filename TEXT NOT NULL,
    stored_filename TEXT NOT NULL UNIQUE,
    file_size_bytes INTEGER NOT NULL,
    content_type TEXT NOT NULL,
    file_data BLOB,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NULL,
    session_id TEXT NULL
)
"""

try:
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute(create_table)
    print("Database and table set up successfully!")
except sqlite3.Error as e:
    print(f"Database error: {e}")