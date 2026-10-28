import urllib.request
import xml.etree.ElementTree as ET
import re
import random
from typing import Dict, Any, List

def fetch_trending_headlines(category="ALL") -> List[Dict[str, str]]:
    """
    Fetches real-time, live breaking headlines from Google News RSS.
    100% Free, Zero API keys required.
    """
    category_map = {
        "TECH": "https://news.google.com/rss/headlines/section/topic/TECHNOLOGY?hl=en-US&gl=US&ceid=US:en",
        "SCIENCE": "https://news.google.com/rss/headlines/section/topic/SCIENCE?hl=en-US&gl=US&ceid=US:en",
        "WORLD": "https://news.google.com/rss/headlines/section/topic/WORLD?hl=en-US&gl=US&ceid=US:en"
    }
    
    selected_topic = category if category in category_map else random.choice(["TECH", "SCIENCE", "WORLD"])
    url = category_map[selected_topic]
    
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            xml_data = resp.read()
            
        root = ET.fromstring(xml_data)
        items = []
        for item in root.findall(".//item")[:10]:
            raw_title = item.find("title").text if item.find("title") is not None else ""
            clean_title = re.sub(r"\s*-\s*[^-]+$", "", raw_title).strip()
            if clean_title and len(clean_title) > 15:
                items.append({
                    "title": clean_title,
                    "topic": selected_topic
                })
        return items
    except Exception as e:
        print(f"[!] Live news fetch notice: {e}")
        return []

def build_news_reel_script(headline_item: Dict[str, str] = None) -> Dict[str, Any]:
    """
    Converts a breaking news headline into a high-retention infinite-loop news reel.
    """
    if not headline_item:
        headlines = fetch_trending_headlines()
        headline_item = random.choice(headlines) if headlines else {
            "title": "Breakthrough Artificial Intelligence Lab Releases Superhuman Reasoning Model",
            "topic": "TECH"
        }
        
    title = headline_item["title"]
    topic = headline_item["topic"]
    
    templates = [
        {
            "hook": "This massive headline just broke today.",
            "body": f"Reports just confirmed that {title}. Industry insiders and scientists are stunned by the sheer speed of this development. If these details hold up, the real-world impact is going to hit much sooner than anyone expected. And the craziest reason why everyone is urgently watching this story is because...",
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
        }
    ]
    
    chosen = random.choice(templates)
    full_script = f"{chosen['hook']} {chosen['body']}"
    
    # Format high-converting caption with hashtags
    caption = (
        f"🚨 BREAKING TODAY: {title}\n\n"
        f"What are your thoughts on this development? Drop your take below! 👇\n"
        f"📌 SAVE this reel for today's briefing.\n"
        f"Follow @curiosreturns for daily breaking curiosities & tech intelligence.\n.\n"
        f"#dailynews #technews #breakingnews #worldnews #sciencenews #currentaffairs #trendingnews "
        f"#innovation #futuretech #newsupdate #curiosreturns #viralreels #dailyinformation"
    )
    
    pinned = "🔥 Follow @curiosreturns for daily mind-expanding news & intelligence! 📲✨"
    
    return {
        "niche": "daily_news",
        "title": f"Today's Brief: {title[:40]}...",
        "script": full_script,
        "loop_bridge": chosen["loop_tail"],
        "caption": caption,
        "pinned_comment": pinned
    }

if __name__ == "__main__":
    reel = build_news_reel_script()
    print("Generated News Reel:")
    print("Title:", reel["title"])
    print("Script:", reel["script"])
    print("Loop Bridge:", reel["loop_bridge"])
