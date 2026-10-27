# 🚀 AI Influencer Autopilot (1-Click Generator & Poster)

Turn your Windows computer into a **fully automated, 100% free faceless influencer system**. Just double-click `RUN_AUTOPILOT.bat` — it writes the script, speaks it with realistic AI neural voiceover, adds viral TikTok/Reels style animated subtitles, renders a 9:16 vertical 1080x1920 video, and posts it directly to your Instagram and Facebook Page!

---

## ⚡ Quick Start (No Setup Required!)

1. Open this directory: `C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer`
2. Double-click:
   ```cmd
   RUN_AUTOPILOT.bat
   ```
3. Watch the terminal generate your video in ~18 seconds. Once done, your Windows File Explorer automatically opens with the completed Reel ready to watch!

---

## 📁 Project Structure

```
autopilot-influencer/
│
├── RUN_AUTOPILOT.bat        <-- ⚡ DOUBLE-CLICK THIS TO RUN EVERYTHING!
├── SETUP_CONFIG.bat         <-- Opens config wizard in Notepad
├── OPEN_OUTPUTS.bat         <-- Opens your rendered videos folder
│
├── config.env               <-- Your free Meta API tokens & optional Gemini Key
├── setup_guide.html         <-- Beautiful interactive visual guide (open in Chrome)
│
├── assets/
│   ├── backgrounds/         <-- (Optional) Drop any vertical gameplay or drone videos here!
│   └── audio/               <-- (Optional) Drop any lo-fi/cinematic background music here!
│
├── outputs/
│   └── reels/               <-- All your rendered MP4s and viral captions are saved here!
│
├── main.py                  <-- Master pipeline coordinator
├── script_generator.py      <-- AI & viral script generator (25+ built-in high hooks)
├── tts_engine.py            <-- Free Microsoft neural voiceover & ASS subtitle generator
├── video_engine.py          <-- FFmpeg 1080x1920 vertical video compositor
└── meta_publisher.py        <-- Official Meta Graph API auto-poster for IG & FB
```

---

## 🎯 High-Retention Viral Niches (Pre-Programmed)

You don't need any idea what to post. The system automatically cycles through the most lucrative faceless niches on Instagram & Facebook:
1. **Dark Psychology & Mind Hacks** (Subconscious body language tricks, detecting liars)
2. **Deep Ocean & Space Mysteries** (Unexplored abyss, rogue planets, terrifying cosmic silence)
3. **Mind-Blowing Unbelievable Facts** (Immortal jellyfish, water bears surviving space)
4. **Stoic Discipline & Sigma Wisdom** (Marcus Aurelius rules, power of moving in silence)

---

## 🔑 How to Enable 100% Free Lifetime Auto-Posting (Instagram & Facebook)

Meta provides **official, completely free** APIs to post Reels to your Facebook Pages and Instagram Professional/Creator accounts:

1. Go to [developers.facebook.com](https://developers.facebook.com) and click **My Apps** -> **Create App** (Choose **Business**).
2. Go to **Tools** -> **Graph API Explorer**.
3. Select your **Facebook Page**.
4. In permissions, check:
   - `pages_show_list`
   - `pages_read_engagement`
   - `pages_manage_posts`
   - `instagram_basic`
   - `instagram_content_publish`
5. Click **Generate Access Token**.
6. Double-click `SETUP_CONFIG.bat` and paste your IDs and token into `config.env`.

*Whenever `RUN_AUTOPILOT.bat` is pressed, it will automatically publish the video straight to your pages!*

---

## 🤖 100% Zero-Touch Automation (Run Every Day at 6:00 PM)

To make it post every single day without you ever touching your computer:
1. Press `Win + R`, type `taskschd.msc` and hit Enter (Windows Task Scheduler).
2. Click **Create Basic Task...**
3. Name: `Daily Viral Reel`
4. Trigger: **Daily at 6:00 PM**
5. Action: **Start a program** -> Browse and select `C:\Users\manik\.gemini\antigravity\scratch\autopilot-influencer\RUN_AUTOPILOT.bat`.
6. Click Finish. That's it! Your PC is now an autonomous influencer.
