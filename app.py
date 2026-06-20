from flask import Flask, render_template, request, redirect
import sqlite3

from utils.predictor import predict_news
from utils.helpers import detect_suspicious_keywords
from utils.database import init_db, save_prediction

app = Flask(__name__)

# Initialize database
init_db()

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Predict route
@app.route("/predict", methods=["POST"])
def predict():

    news = request.form["news"]

    prediction, confidence = predict_news(news)

    keywords = detect_suspicious_keywords(news)

    # Save in database
    save_prediction(news, prediction, confidence)

    return render_template(
        "result.html",
        prediction=prediction,
        confidence=confidence,
        article=news,
        keywords=keywords
    )

# History page
@app.route("/history")
def history():

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    # Current page
    page = request.args.get("page", 1, type=int)

    per_page = 10
    offset = (page - 1) * per_page

    # Fetch records
    cursor.execute("""
        SELECT article, prediction, confidence, timestamp
        FROM predictions
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (per_page, offset))

    records = cursor.fetchall()

    # Total records
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]

    # Analytics
    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction='REAL'")
    real_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM predictions WHERE prediction='FAKE'")
    fake_count = cursor.fetchone()[0]

    conn.close()

    total_pages = (total + per_page - 1) // per_page

    return render_template(
        "history.html",
        records=records,
        total=total,
        real_count=real_count,
        fake_count=fake_count,
        page=page,
        total_pages=total_pages
    )

# Clear history
@app.route("/clear_history")
def clear_history():

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM predictions")

    conn.commit()
    conn.close()

    return redirect("/history")

# Run app
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)