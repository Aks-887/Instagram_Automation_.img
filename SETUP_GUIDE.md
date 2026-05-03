# 🇮🇳 India Instagram Auto-Poster — Setup Guide

## What This Bot Does
- Automatically fetches beautiful India photos (temples, tourist spots, nature)
- Generates engaging captions + hashtags using Claude AI
- Posts to your Instagram every 4 hours (customizable)
- Logs every post for your records

---

## Step 1: Install Python
Download Python from https://python.org (version 3.8 or higher)
During install, check ✅ "Add Python to PATH"

---

## Step 2: Install Dependencies
Open Command Prompt and run:
```
pip install requests schedule
```

---

## Step 3: Get Your FREE API Keys

### 🔑 Unsplash API Key (Free — for images)
1. Go to https://unsplash.com/developers
2. Click "Register as a developer"
3. Create a new application
4. Copy your **Access Key**
5. Paste it in poster.py → `UNSPLASH_ACCESS_KEY`

### 🔑 Anthropic API Key (Free tier — for captions)
1. Go to https://console.anthropic.com
2. Sign up for free
3. Go to API Keys → Create new key
4. Copy the key
5. Paste it in poster.py → `ANTHROPIC_API_KEY`

### 🔑 Instagram Graph API (Free — for posting)
1. Go to https://developers.facebook.com
2. Create a new App → Choose "Business" type
3. Add "Instagram Graph API" product
4. Connect your Instagram Business/Creator account
5. Get your **Instagram User ID** and **Access Token**
6. Paste them in poster.py → `IG_USER_ID` and `IG_ACCESS_TOKEN`

   > ⚠️ NOTE: Instagram access tokens expire every 60 days.
   > You'll need to refresh them at developers.facebook.com

---

## Step 4: Edit poster.py
Open poster.py in Notepad and fill in your 4 keys:
```python
UNSPLASH_ACCESS_KEY = "paste_your_key_here"
ANTHROPIC_API_KEY   = "paste_your_key_here"
IG_USER_ID          = "paste_your_id_here"
IG_ACCESS_TOKEN     = "paste_your_token_here"
```

You can also change how often it posts:
```python
POST_EVERY_HOURS = 4   # Change to 6, 8, 12, etc.
```

---

## Step 5: Run the Bot
Open Command Prompt in the bot folder and run:
```
python poster.py
```

The bot will:
1. Post immediately when started
2. Then post every 4 hours automatically
3. Keep your PC on for it to keep running!

---

## Step 6: Keep It Running (Optional)
To run the bot in the background on Windows:
1. Create a file called `run_bot.bat` with this content:
   ```
   @echo off
   python C:\path\to\india_instagram_bot\poster.py
   ```
2. Press Win+R → type `shell:startup`
3. Put a shortcut to `run_bot.bat` there
4. Now it auto-starts when your PC boots!

---

## Files Explained
| File | Purpose |
|------|---------|
| `poster.py` | Main bot script |
| `requirements.txt` | Python packages needed |
| `post_log.json` | Log of every successful post |
| `error_log.txt` | Log of any errors |

---

## Troubleshooting
- **"ModuleNotFoundError"** → Run `pip install requests schedule`
- **"401 Unauthorized"** → Check your API keys are correct
- **"400 Bad Request" from Instagram** → Your image URL may have expired; try running again
- **Token expired** → Refresh your Instagram access token at developers.facebook.com

---

## 📍 India Places Covered
The bot rotates through these searches:
Taj Mahal, Rajasthan Palaces, Kerala Backwaters, Varanasi Ghats,
Golden Temple, Hampi Ruins, Rishikesh, Mysore Palace, Udaipur,
Ladakh, Goa, Darjeeling, Khajuraho, Ellora Caves, Rann of Kutch,
Jaipur, Munnar, Coorg, Sundarbans & more!
