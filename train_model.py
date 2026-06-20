import pandas as pd
import pickle
import os
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report

# Clean text
def clean_text(text):
    text = str(text).lower()

    # Remove special characters
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()

# Load datasets
fake_df = pd.read_csv("dataset/Fake.csv")
true_df = pd.read_csv("dataset/True.csv")

print("Fake samples:", len(fake_df))
print("Real samples:", len(true_df))

# Create labels
fake_df["label"] = "FAKE"
true_df["label"] = "REAL"

# Merge datasets
df = pd.concat([fake_df, true_df], ignore_index=True)

# Create content column
df["title"] = df["title"].fillna("")
df["text"] = df["text"].fillna("")

df["content"] = df["title"] + " " + df["text"]

# Clean text
df["content"] = df["content"].apply(clean_text)

# Features and labels
X = df["content"]
y = df["label"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    stop_words="english",
    lowercase=True,
    max_df=0.9,
    min_df=2,
    ngram_range=(1, 2),
    sublinear_tf=True
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


# Train model
model = MultinomialNB()
model.fit(X_train_vec, y_train)


# Evaluate model
predictions = model.predict(X_test_vec)
accuracy = accuracy_score(y_test, predictions)

print("\nAccuracy:", accuracy * 100)

print("\nClassification Report:\n")
print(classification_report(y_test, predictions))

# Save model and vectorizer
os.makedirs("models", exist_ok=True)

pickle.dump(model, open("models/model.pkl", "wb"))
pickle.dump(vectorizer, open("models/vectorizer.pkl", "wb"))

print("\nTraining completed successfully.")