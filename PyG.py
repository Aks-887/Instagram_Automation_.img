import os
import time
import random
import requests
import schedule
import json
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────
UNSPLASH_ACCESS_KEY = "ZjjE-B6MBFAzDeBySDLZT5QDt0OqvWPnE37X7REpFqo"   # Free at unsplash.com/developers
ANTHROPIC_API_KEY   = "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"     # Free tier at console.anthropic.com
IG_USER_ID = "17841468929061035"     # Your IG Business account ID
IG_ACCESS_TOKEN     = "EAAVw9HvS5zkBRWPBy5eArZBWf4CqLPw80c94VzGam24rEWASXB9DyMdYOdosyRQct4mdnX6UTGJyVUGZABiDEHTnzAsflDPKFRqpi4ADSv5So2vZAeowpl8ZC97OZBQ50MDyzOlt3QdSPTRLF3T1dBAZBm3SwY8nfj1pAfulU0Adk45HCwFGp8q6yjGHNt6WA3UGmr5pIXikzyxPxrAFuw1eUg0ZC1ifZBAGiVad61sdYIgZC9lC9" # From Meta Developer portal

POST_EVERY_HOURS = 1

# Girl-focused content queries
GIRL_QUERIES = [
    "indian girl portrait",
    "indian woman saree",
    "indian model fashion",
    "indian girl traditional dress",
    "indian lifestyle photography woman",
    "indian girl outdoor portrait",
    "indian fashion photography",
    "indian street style woman",
    "indian aesthetic girl portrait",
    "bollywood style portrait woman"
]

# ─────────────────────────────────────────────
# STEP 1: Fetch Image from Unsplash
# ─────────────────────────────────────────────
def fetch_image():
    query = random.choice(GIRL_QUERIES)
    print(f"[{datetime.now()}] Searching Unsplash for: '{query}'")

    url = "https://api.unsplash.com/photos/random"

    headers = {
        "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }

    params = {
        "query": query,
        "orientation": "portrait",
        "content_filter": "high"
    }

    resp = requests.get(url, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    image_url = data["urls"]["regular"]
    photographer = data["user"]["name"]

    print(f"  ✅ Image fetched successfully")
    return image_url, photographer


# ─────────────────────────────────────────────
# STEP 2: Generate Caption (Local)
# ─────────────────────────────────────────────
def generate_caption():
    captions = [
        "✨ Beauty, confidence & culture in one frame 🇮🇳",
        "🌸 Indian elegance captured perfectly.",
        "💫 Grace and tradition blended beautifully.",
        "🔥 Confidence is the best outfit.",
        "🌿 Where tradition meets modern charm.",
        "🌺 Desi vibes, global style.",
    ]

    hashtags = """
#IndianBeauty #DesiGirl #IndianModel #SareeLove #IndianFashion
#PortraitPhotography #IndianCulture #InstaFashion #IndianStyle
#TraditionalLook #ModernIndia #PhotographyLovers
#DesiVibes #AestheticGirl #IndianPortrait
"""

    return random.choice(captions) + "\n\nWhat do you think? 👇\n" + hashtags


# ─────────────────────────────────────────────
# STEP 3: Post to Instagram
# ─────────────────────────────────────────────
def post_to_instagram(image_url, caption):
    print(f"[{datetime.now()}] Posting to Instagram...")

    # Create media container
    container_url = f"https://graph.facebook.com/v25.0/{IG_USER_ID}/media"
    container_resp = requests.post(container_url, data={
        "image_url": image_url,
        "caption": caption,
        "access_token": IG_ACCESS_TOKEN,
    }, timeout=30)

    if container_resp.status_code != 200:
        print("Instagram container error:", container_resp.text)
        raise Exception("Failed creating media container")

    container_id = container_resp.json()["id"]
    print(f"  ✅ Media container created")

    time.sleep(5)

    # Publish media
    publish_url = f"https://graph.facebook.com/v25.0/{IG_USER_ID}/media_publish"
    publish_resp = requests.post(publish_url, data={
        "creation_id": container_id,
        "access_token": IG_ACCESS_TOKEN,
    }, timeout=30)

    if publish_resp.status_code != 200:
        print("Instagram publish error:", publish_resp.text)
        raise Exception("Failed publishing post")

    post_id = publish_resp.json()["id"]
    print(f"  🎉 Successfully posted! Post ID: {post_id}")

    return post_id


# ─────────────────────────────────────────────
# MAIN PIPELINE
# ─────────────────────────────────────────────
def run_pipeline():
    print("\n" + "="*50)
    print(f"🚀 Starting Instagram Girls Bot — {datetime.now()}")
    print("="*50)

    try:
        image_url, photographer = fetch_image()
        caption = generate_caption()
        post_id = post_to_instagram(image_url, caption)

        log_entry = {
            "timestamp": str(datetime.now()),
            "post_id": post_id,
            "image_url": image_url,
            "photographer": photographer
        }

        with open("post_log.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        print("✅ Post logged successfully.")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        with open("error_log.txt", "a") as f:
            f.write(f"{datetime.now()} — {e}\n")


# ─────────────────────────────────────────────
# SCHEDULER
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("🤖 Instagram Girls Bot Starting...")
    print(f"⏰ Will post every {POST_EVERY_HOURS} hours")
    print("▶️ Running first post now...\n")

    run_pipeline()

    schedule.every(POST_EVERY_HOURS).hours.do(run_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(60)