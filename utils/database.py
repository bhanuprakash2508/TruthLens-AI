import sqlite3
from datetime import datetime


# Create database
def init_db():

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            article TEXT,
            prediction TEXT,
            confidence REAL,
            timestamp TEXT
        )
    """)

    conn.commit()
    conn.close()


# Save prediction
def save_prediction(article, prediction, confidence):

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions(article, prediction, confidence, timestamp)
        VALUES (?, ?, ?, ?)
    """, (
        article,
        prediction,
        confidence,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()