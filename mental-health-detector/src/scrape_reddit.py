import praw
import os
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# 🔍 Debug print (do not share screenshots of secrets!)
print("🔎 Debugging .env loading...")
print("CLIENT_ID length:", len(CLIENT_ID) if CLIENT_ID else "MISSING")
print("CLIENT_SECRET length:", len(CLIENT_SECRET) if CLIENT_SECRET else "MISSING")
print("USER_AGENT:", USER_AGENT if USER_AGENT else "MISSING")

# Initialize Reddit API
reddit = praw.Reddit(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    user_agent=USER_AGENT
)

# --------- scraping logic continues ---------
LIMIT = 100

def scrape_subreddit(subreddit_name, label):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for post in subreddit.hot(limit=LIMIT):
        posts.append({
            "source": subreddit_name,
            "date": datetime.utcfromtimestamp(post.created_utc).strftime('%Y-%m-%d %H:%M:%S'),
            "text": post.title + " " + (post.selftext or ""),
            "label": label
        })
    return pd.DataFrame(posts)

def main():
    os.makedirs("data/raw", exist_ok=True)

    # ✅ WIDE COVERAGE of distress vs not distress
    targets = {
        # 🔴 Distress / Mental Health Struggles
        "depression": "distress",
        "mentalhealth": "distress",
        "SuicideWatch": "distress",
        "Anxiety": "distress",
        "bipolar": "distress",
        "offmychest": "distress",
        "TrueOffMyChest": "distress",
        "relationship_advice": "distress",
        "addiction": "distress",
        "traumatoolbox": "distress",
        "griefsupport": "distress",
        "lonely": "distress",
        "socialanxiety": "distress",
        "ptsd": "distress",
        "eatingdisorders": "distress",
        "OCD": "distress",
        "panicdisorder": "distress",

        # 🟢 Not Distress / Positive, Neutral
        "happy": "not_distress",
        "positivity": "not_distress",
        "CasualConversation": "not_distress",
        "GetMotivated": "not_distress",
        "UpliftingNews": "not_distress",
        "MadeMeSmile": "not_distress",
        "KindVoice": "not_distress",
        "LifeProTips": "not_distress",
        "wholesomememes": "not_distress",
        "HumansBeingBros": "not_distress",
        "DecidingToBeBetter": "not_distress",
        "selfimprovement": "not_distress",
        "productivity": "not_distress",
        "successstories": "not_distress",
        "inspiration": "not_distress",
        "GoodNews": "not_distress",
        "motivation": "not_distress"
    }

    frames = []
    for sub, label in targets.items():
        print(f"📥 Scraping r/{sub} ...")
        df = scrape_subreddit(sub, label)
        frames.append(df)

    final_df = pd.concat(frames, ignore_index=True)
    final_df.to_csv("data/raw/reddit_posts.csv", index=False, encoding="utf-8")
    print("✅ Saved to data/raw/reddit_posts.csv")


if __name__ == "__main__":
    main()
