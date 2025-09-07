import importlib

packages = ["pandas","sklearn","transformers","torch","streamlit","snscrape","praw","spacy"]

for p in packages:
    try:
        importlib.import_module(p)
        print(p, "OK")
    except Exception as e:
        print(p, "ERROR:", e)
 