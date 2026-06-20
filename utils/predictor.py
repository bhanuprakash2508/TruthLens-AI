import pickle
import re

# Load model and vectorizer
model = pickle.load(open("models/model.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))


# Clean text
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# Predict news
def predict_news(news_text):

    cleaned_text = clean_text(news_text)

    transformed_text = vectorizer.transform([cleaned_text])

    prediction = model.predict(transformed_text)[0]

    confidence = model.predict_proba(transformed_text).max() * 100

    return prediction, round(confidence, 2)