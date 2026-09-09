import sqlite3

#Database filepath
database = "/Users/muhxmmadharis/Desktop/Exam_Rag_Project/test.db"

#The tables my database will consist of
create_table = """
-- Enable foreign key enforcement in SQLite (disabled by default)
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS uploaded_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT NOT NULL,
    content_type TEXT NOT NULL,
    file_data BLOB NOT NULL
);

CREATE TABLE IF NOT EXISTS paper_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id INTEGER NOT NULL,
    image_key TEXT NOT NULL,       -- Identifies the figure (e.g., "fig_1.png")
    image_data BLOB NOT NULL,      -- Stores the raw image binary bytes
    caption TEXT,                  -- Stores the extracted figure caption
    
    -- Links file_id to uploaded_files.id
    -- ON DELETE CASCADE automatically deletes associated images if the parent file is deleted
    FOREIGN KEY (file_id) REFERENCES uploaded_files(id) ON DELETE CASCADE
);

-- Creates a composite index on file_id and image_key
-- This allows SQLite to instantly locate a specific image for a file instead of searching line-by-line
CREATE INDEX IF NOT EXISTS idx_paper_images_lookup 
ON paper_images(file_id, image_key);
"""

#Function to build connection to database and restart it everytime
def start_db():
    with sqlite3.connect(database) as connection:
        with sqlite3.connect(database) as connection:
            cursor = connection.cursor()
            cursor.executescript(create_table)
            connection.commit()

#Function to save file to the uploaded_file table
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

#Function to fetch the file binary content from uploaded_file table
def get_file_content():

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT file_data FROM uploaded_files ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()
    
    if not result:
        raise ValueError("No files found in the database.")
        
    return result[0]

#Function to fetch the filename from uploaded_file table
def get_filename():

    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT filename FROM uploaded_files ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()
        
    if not result:
        raise ValueError("No files found in the database.")
            
    return result[0]

#Function to save images
def save_image(file_id: int, image_key: str, image_bytes: bytes, caption: str) -> int:
    """Inserts an extracted image binary and its caption into paper_images."""
    query = """
    INSERT INTO paper_images (file_id, image_key, image_data, caption)
    VALUES (?, ?, ?, ?)
    """
    with sqlite3.connect(database) as conn:
        # Enforce foreign key constraints for this connection
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()
        cursor.execute(query, (file_id, image_key, image_bytes, caption))
        conn.commit()
        return cursor.lastrowid

def get_file_id():
    with sqlite3.connect(database) as connection:
        cursor = connection.cursor()
        # Correct SQL: Removed trailing comma after 'id', 'FROM' keyword, and extra commas
        cursor.execute("SELECT id FROM uploaded_files ORDER BY id DESC LIMIT 1;")
        result = cursor.fetchone()

    if not result:
        raise ValueError("No files found in the database.")

    return result[0]


#Manually allows you to reset the database if you run it directly
if __name__ == "__main__":
    start_db()