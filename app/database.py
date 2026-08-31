from multiprocessing import connection
import sqlite3

database = "/Users/muhxmmadharis/Desktop/Exam_Rag_Project/test.db"

create_table = """
CREATE TABLE IF NOT EXISTS uploaded_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    content_type TEXT NOT NULL,
    file_data BLOB
);
"""

def reset_db():
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS uploaded_files")
        cursor.execute(create_table)

def save_file(filename: str, content_type: str, file_data: bytes):
    query = """
    INSERT INTO uploaded_files (filename, content_type, file_data)
    VALUES (?, ?, ?)
    """
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute(query, (filename, content_type, file_data))
        connection.commit()
        return cursor.lastrowid

if __name__ == "__main__":
    init_db()
    print("Database ready for testing!")