from datetime import datetime
from typing import Dict, Any

# 7 Distinct Themed Content Styles (1 for each day of the week)
DAILY_STYLES: Dict[int, Dict[str, Any]] = {
    0: {  # MONDAY
        "day_name": "Monday",
        "theme_title": "Wealth Secrets & Financial Glitches",
        "primary_niche": "wealth_secrets",
        "voice": "en-US-AndrewMultilingualNeural",  # Energetic, modern high-stakes tone
        "subtitle_color": "&H0000D7FF",            # Glowing Cyber Gold
        "style_tag": "MONEY_MONDAY",
        "emoji": "🏦💸",
        "marketing_hook": "Ready to build your digital cash flow asset this week? Free guide in bio! 📈"
    },
    1: {  # TUESDAY
        "day_name": "Tuesday",
        "theme_title": "Secret AI Tools That Feel Illegal",
        "primary_niche": "ai_glitches",
        "voice": "en-US-AvaNeural",                 # Crisp, tech-savvy, fast-paced
        "subtitle_color": "&H00FFFF00",             # Neon Cyan / Electric Blue
        "style_tag": "TECH_TUESDAY",
        "emoji": "🤖⚡",
        "marketing_hook": "Access our private database of 100+ Free AI shortcuts via link in bio! 📲"
    },
    2: {  # WEDNESDAY
        "day_name": "Wednesday",
        "theme_title": "Dark Psychology & Power Laws",
        "primary_niche": "dark_psychology",
        "voice": "en-US-ChristopherNeural",         # Deep, authoritative, documentary hypnotic
        "subtitle_color": "&H0024E0FB",             # Vivid Amber Gold
        "style_tag": "PSYCHOLOGY_WEDNESDAY",
        "emoji": "♟️👁️",
        "marketing_hook": "Master the hidden laws of human persuasion. Reading list in bio. 📚"
    },
    3: {  # THURSDAY
        "day_name": "Thursday",
        "theme_title": "Bizarre Science & Cosmic Mysteries",
        "primary_niche": "mind_facts",
        "voice": "en-US-GuyNeural",                 # Engaging, wonder-filled narrative
        "subtitle_color": "&H00E0FF24",             # Emerald / Teal Glow
        "style_tag": "CURIOUS_THURSDAY",
        "emoji": "🌊🪐",
        "marketing_hook": "Tap follow for mind-expanding discoveries every single day! 🌍✨"
    },
    4: {  # FRIDAY
        "day_name": "Friday",
        "theme_title": "The Stoic Blueprint & Sigma Discipline",
        "primary_niche": "stoic_wisdom",
        "voice": "en-US-BrianNeural",               # Heavy baritone, timeless warrior stoic
        "subtitle_color": "&H00FFFFFF",             # Diamond White with Heavy Shadow
        "style_tag": "STOIC_FRIDAY",
        "emoji": "🏛️🐺",
        "marketing_hook": "Move like a ghost until it's checkmate. Free mindset guide in bio. 👑"
    },
    5: {  # SATURDAY
        "day_name": "Saturday",
        "theme_title": "Mind Hacks & Subconscious Secrets",
        "primary_niche": "dark_psychology",
        "voice": "en-US-ChristopherNeural",         # Deep baritone
        "subtitle_color": "&H0000FFFF",             # Neon Yellow Accent
        "style_tag": "MIND_SATURDAY",
        "emoji": "🧠⚡",
        "marketing_hook": "Unlock the cheat codes to human nature. Link in bio! 🔗"
    },
    6: {  # SUNDAY
        "day_name": "Sunday",
        "theme_title": "Mastery & The 1% Reset",
        "primary_niche": "wealth_secrets",
        "voice": "en-US-AndrewMultilingualNeural",  # Inspiring weekly reset
        "subtitle_color": "&H0033CCFF",             # Sunburst Gold
        "style_tag": "RESET_SUNDAY",
        "emoji": "🚀💼",
        "marketing_hook": "Start your week ahead of 99% of people. Claim your free tools in bio! 🔥"
    }
}

def get_today_style() -> Dict[str, Any]:
    weekday = datetime.now().weekday()
    return DAILY_STYLES.get(weekday, DAILY_STYLES[0])

# 4 Daily Posting Slots (Engineered for Global Peak Traffic Waves)
DAILY_SLOTS = [
    {
        "slot_id": "slot_1",
        "target_time": "08:30",
        "name": "Morning Commute Launchpad",
        "niche_bias": "stoic_wisdom"  # Morning discipline/motivation
    },
    {
        "slot_id": "slot_2",
        "target_time": "12:30",
        "name": "Midday Viral Drop",
        "niche_bias": "ai_glitches"    # Lunchtime tech tools & shortcuts
    },
    {
        "slot_id": "slot_3",
        "target_time": "17:30",
        "name": "Evening Curiosity Peak",
        "niche_bias": "mind_facts"     # Evening mind-blowing facts
    },
    {
        "slot_id": "slot_4",
        "target_time": "21:00",
        "name": "Late Night Deep Binge",
        "niche_bias": "wealth_secrets" # Late night money & dark psychology
    }
]
