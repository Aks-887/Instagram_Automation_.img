import os
import time
import random
import requests
import schedule
import json
from datetime import datetime

# ─────────────────────────────────────────────
# CONFIGURATION — Fill these in!
# ─────────────────────────────────────────────
UNSPLASH_ACCESS_KEY = "ZjjE-B6MBFAzDeBySDLZT5QDt0OqvWPnE37X7REpFqo"   # Free at unsplash.com/developers
ANTHROPIC_API_KEY   = "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"     # Free tier at console.anthropic.com
IG_USER_ID = "17841468929061035"     # Your IG Business account ID
IG_ACCESS_TOKEN     = "EAAVw9HvS5zkBRWPBy5eArZBWf4CqLPw80c94VzGam24rEWASXB9DyMdYOdosyRQct4mdnX6UTGJyVUGZABiDEHTnzAsflDPKFRqpi4ADSv5So2vZAeowpl8ZC97OZBQ50MDyzOlt3QdSPTRLF3T1dBAZBm3SwY8nfj1pAfulU0Adk45HCwFGp8q6yjGHNt6WA3UGmr5pIXikzyxPxrAFuw1eUg0ZC1ifZBAGiVad61sdYIgZC9lC9" # From Meta Developer portal

# How often to post (in hours)
POST_EVERY_HOURS = 4

# India-focused search queries — rotated randomly each post
INDIA_QUERIES = [
    "india temple",
    "taj mahal india",
    "rajasthan palace",
    "kerala backwaters",
    "varanasi ghat",
    "jaipur india",
    "golden temple amritsar",
    "hampi ruins india",
    "rishikesh india",
    "mysore palace india",
    "udaipur lake palace",
    "ladakh india landscape",
    "goa beach india",
    "darjeeling tea garden",
    "khajuraho temple india",
    "ellora caves india",
    "sundarbans india",
    "coorg india",
    "munnar kerala",
    "rann of kutch india",
]

# ─────────────────────────────────────────────
# STEP 1: Fetch a beautiful India image
# ─────────────────────────────────────────────

def fetch_india_image():
    query = random.choice(INDIA_QUERIES)
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

    image_url   = data["urls"]["regular"]
    location    = data.get("location", {}).get("name") or query.replace(" india", "").title()
    description = data.get("description") or data.get("alt_description") or query
    photographer = data["user"]["name"]

    print(f"  ✅ Got image: {image_url[:60]}...")
    return image_url, location, description, photographer, query


# ─────────────────────────────────────────────
# STEP 2: Generate caption using Claude AI
# ─────────────────────────────────────────────
def generate_caption(location, description, query):
    print(f"[{datetime.now()}] Generating caption with Claude AI...")

    prompt = f"""You are an Instagram travel content creator specializing in India travel.

Image details:
- Location hint: {location}
- Query used: {query}
- Photo description: {description}

Write an engaging Instagram post with:
1. A catchy opening line (emoji + hook)
2. 3-4 sentences about this place — history, beauty, why visit
3. A call-to-action (e.g. "Would you visit? 👇")
4. A line break then 20-25 relevant hashtags (mix of popular + niche India travel hashtags)

Keep the tone warm, inspiring, and adventurous.
Return ONLY the caption text, nothing else."""

def generate_caption(location, description, query):
    print(f"[{datetime.now()}] Generating caption locally...")

    captions = [
        f"✨ Discover the magic of {location}, one of India's most breathtaking destinations! 🇮🇳",
        f"🌿 {location} — where history, culture and beauty meet.",
        f"📍 Exploring {location}, a true hidden gem of India.",
        f"🏞️ The beauty of {location} will leave you speechless.",
    ]

    hashtags = """
#IncredibleIndia #IndiaTravel #TravelIndia #ExploreIndia #IndianCulture
#WanderlustIndia #DesiDiaries #IndianPhotography #TravelGram
#DiscoverIndia #BeautifulIndia #IndianHeritage #IndiaTourism
#TravelAddict #TravelGoals #InstaTravel #TravelInspiration
#IndianLandscapes #VisitIndia #NatureLovers #TravelPhotography
"""

    caption = random.choice(captions) + "\n\nWould you visit this place? 👇\n" + hashtags
    return caption

# ─────────────────────────────────────────────
# STEP 3: Post to Instagram via Graph API
# ─────────────────────────────────────────────
def post_to_instagram(image_url, caption):
    print(f"[{datetime.now()}] Posting to Instagram...")

    # Step 3a: Create media container
    container_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media"
    container_resp = requests.post(container_url, data={
        "image_url": image_url,
        "caption": caption,
        "access_token": IG_ACCESS_TOKEN,
    }, timeout=30)
    container_resp.raise_for_status()
    container_id = container_resp.json()["id"]
    print(f"  ✅ Media container created: {container_id}")

    # Wait a moment for Instagram to process
    time.sleep(5)

    # Step 3b: Publish the container
    publish_url = f"https://graph.facebook.com/v19.0/{IG_USER_ID}/media_publish"
    publish_resp = requests.post(publish_url, data={
        "creation_id": container_id,
        "access_token": IG_ACCESS_TOKEN,
    }, timeout=30)
    publish_resp.raise_for_status()
    post_id = publish_resp.json()["id"]
    print(f"  ✅ Posted! Instagram Post ID: {post_id}")
    return post_id


# ─────────────────────────────────────────────
# MAIN: Full pipeline
# ─────────────────────────────────────────────
def run_pipeline():
    print("\n" + "="*50)
    print(f"🚀 Starting India Instagram Bot — {datetime.now()}")
    print("="*50)

    try:
        # 1. Get image
        image_url, location, description, photographer, query = fetch_india_image()

        # 2. Generate caption
        caption = generate_caption(location, description, query)

        # 3. Post to Instagram
        post_id = post_to_instagram(image_url, caption)

        # 4. Log success
        log_entry = {
            "timestamp": str(datetime.now()),
            "post_id": post_id,
            "image_url": image_url,
            "query": query,
            "location": location,
            "photographer": photographer,
        }
        with open("post_log.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        print(f"\n🎉 SUCCESS! Posted about: {location}")
        print(f"📸 Photo by: {photographer} (Unsplash)")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        with open("error_log.txt", "a") as f:
            f.write(f"{datetime.now()} — {e}\n")


# ─────────────────────────────────────────────
# SCHEDULER
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print(f"🤖 India Instagram Bot starting...")
    print(f"⏰ Will post every {POST_EVERY_HOURS} hours")
    print(f"▶️  Running first post now...\n")

    # Run immediately on start
    run_pipeline()

    # Then schedule repeating posts
    schedule.every(POST_EVERY_HOURS).hours.do(run_pipeline)

    while True:
        schedule.run_pending()
        time.sleep(60)