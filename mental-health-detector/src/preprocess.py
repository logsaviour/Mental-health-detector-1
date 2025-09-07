# src/preprocess.py

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import os

# Download NLTK resources (first time only)
nltk.download("stopwords")
nltk.download("punkt")
nltk.download("punkt_tab") 
nltk.download("wordnet")


INPUT_FILE = "data/raw/reddit_posts.csv"
OUTPUT_FILE = "data/processed/clean_reddit_posts.csv"

def clean_text(text):
    # 1. Lowercase
    text = text.lower()

    # 2. Remove URLs
    text = re.sub(r"http\S+|www\S+|https\S+", "", text)

    # 3. Remove punctuation, numbers, special chars
    text = re.sub(r"[^a-z\s]", "", text)

    # 4. Tokenize (split into words)
    tokens = nltk.word_tokenize(text)

    # 5. Remove stopwords (the, is, at, etc.)
    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if word not in stop_words]

    # 6. Lemmatization (better than stemming)
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    # 7. Join back into text
    return " ".join(tokens)

def main():
    if not os.path.exists(INPUT_FILE):
        print(f"⚠️ No raw data found at {INPUT_FILE}. Run scrape_reddit.py first.")
        return

    print(f"📂 Loading {INPUT_FILE} ...")
    df = pd.read_csv(INPUT_FILE)

    # Drop duplicates and empty rows
    df.drop_duplicates(subset="text", inplace=True)
    df.dropna(subset=["text"], inplace=True)

    print("✨ Cleaning text ... (this may take a minute)")
    df["clean_text"] = df["text"].astype(str).apply(clean_text)

    # Save processed file
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8")

    print(f"✅ Saved cleaned dataset to {OUTPUT_FILE}")
    print(df.head())
    

if __name__ == "__main__":
    main()
