# Detect suspicious keywords
def detect_suspicious_keywords(news_text):

    suspicious_words = [
        "secretly",
        "shocking",
        "miracle cure",
        "hidden truth",
        "government hiding",
        "confidential leak",
        "breaking discovery",
        "alien",
        "teleport",
        "magic fruit"
    ]

    found = []

    text = news_text.lower()

    for word in suspicious_words:
        if word in text:
            found.append(word)

    return found