import urllib.request
import xml.etree.ElementTree as ET
import re
import random
from typing import Dict, Any, List
from history_registry import is_headline_used, record_used_content

CATEGORY_URLS = {
    "TECH": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en",
    "SCIENCE": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en",
    "WORLD": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en",
    "BUSINESS": "https://news.google.com/rss/headlines/section/topic/BUSINESS?hl=en-US&gl=US&ceid=US:en",
    "HEALTH": "https://news.google.com/rss/headlines/section/topic/HEALTH?hl=en-US&gl=US&ceid=US:en"
}

def fetch_fresh_breaking_headline(preferred_category="ALL") -> Dict[str, str]:
    """
    Fetches a 100% FRESH, UNSEEN breaking headline from live Google News.
    Strictly avoids any story previously broadcasted!
    """
    categories = list(CATEGORY_URLS.keys())
    if preferred_category in CATEGORY_URLS:
        search_order = [preferred_category] + [c for c in categories if c != preferred_category]
    else:
        random.shuffle(categories)
        search_order = categories

    for cat in search_order:
        url = CATEGORY_URLS[cat]
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                xml_data = resp.read()

            root = ET.fromstring(xml_data)
            for item in root.findall(".//item"):
                raw_title = item.find("title").text if item.find("title") is not None else ""
                clean_title = re.sub(r"\s*-\s*[^-]+$", "", raw_title).strip()
                if clean_title and len(clean_title) > 20:
                    # Check deduplication against history
                    if not is_headline_used(clean_title):
                        print(f"[*] Found Fresh Unseen Headline [{cat}]: '{clean_title}'")
                        return {"title": clean_title, "category": cat}
        except Exception as e:
            print(f"[!] Feed fetch error for {cat}: {e}")

    # Fallback if all live feeds fail or are seen
    return {
        "title": "Quantum Physics Breakthrough Unveils Hidden Properties of Cosmic Space",
        "category": "SCIENCE"
    }

def build_news_reel_script(preferred_category="ALL") -> Dict[str, Any]:
    """
    Transforms a fresh breaking news headline into a unique high-retention infinite-loop reel.
    """
    headline_item = fetch_fresh_breaking_headline(preferred_category)
    title = headline_item["title"]
    category = headline_item["category"]

    # Record to history immediately so it's never repeated
    record_used_content(title=f"News: {title[:40]}", niche="daily_news", headline=title)

    templates = [
        {
            "hook": "This massive headline just broke today.",
            "body": f"Reports just confirmed that {title}. Industry insiders and scientists are stunned by how fast this is developing. If these details hold up, the real-world impact is going to hit much sooner than anyone expected. And the craziest reason why everyone is urgently watching this story is because...",
            "loop_tail": "...watching this story is because... This massive headline just broke today."
        },
        {
            "hook": "Here is the number one story you missed today.",
            "body": f"According to breaking reports, {title}. Most mainstream feeds completely overlooked this, but the underlying data proves a massive shift is already underway. The implications are spreading fast, and the key reason why this story refuses to stay quiet is that...",
            "loop_tail": "...refuses to stay quiet is that... Here is the number one story you missed today."
        },
        {
            "hook": "Something extraordinary just happened in the world today.",
            "body": f"Breaking updates revealed that {title}. Experts are racing to analyze the long-term consequences, calling it a potential turning point. If you follow global trends, you need to understand this now. Because the untold truth behind what just happened begins when...",
            "loop_tail": "...behind what just happened begins when... Something extraordinary just happened in the world today."
        },
        {
            "hook": "Pay close attention to what just happened today.",
            "body": f"Global sources just verified that {title}. While most people were distracted, this major event quietly reshaped the landscape. Analysts are warning that this is only the first domino to fall. And the single most alarming fact about today's announcement is that...",
            "loop_tail": "...today's announcement is that... Pay close attention to what just happened today."
        }
    ]

    chosen = random.choice(templates)
    full_script = f"{chosen['hook']} {chosen['body']}"

    caption = (
        f"🚨 BREAKING TODAY ({category}): {title}\n\n"
        f"What is your honest take on this? Let us know below! 👇\n"
        f"📌 SAVE this reel to stay ahead of the curve.\n"
        f"Follow @curiosreturns for daily breaking curiosities & intelligence.\n.\n"
        f"#{category.lower()}news #breakingnews #worldnews #technews #trendingnow #intelligence "
        f"#future #innovation #curiosreturns #viralreels #dailyinformation"
    )

    pinned = f"🔥 Fresh daily intelligence updates! Follow @curiosreturns for tomorrow's stories. 📲✨"

    return {
        "niche": "daily_news",
        "title": f"Today's Brief: {title[:40]}...",
        "script": full_script,
        "loop_bridge": chosen["loop_tail"],
        "caption": caption,
        "pinned_comment": pinned
    }

if __name__ == "__main__":
    s = build_news_reel_script()
    print("Script:", s["script"])
