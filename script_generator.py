import random
import requests
import json
from config import get_config
from news_engine import build_news_reel_script, fetch_fresh_breaking_headline
from history_registry import is_title_used, record_used_content, get_last_niche

# =========================================================================
# SEAMLESS INFINITE LOOP SCRIPT VAULT (OUROBOROS ARCHITECTURE)
# The final spoken word connects grammatically and sonically to the first word!
# Viewers get trapped in an endless loop, driving Average Watch Time > 115%.
# =========================================================================

VIRAL_LIBRARY = [
    # --- 1. WEALTH SECRETS (MONEY MONDAY / SUNDAY RESET) ---
    {
        "niche": "wealth_secrets",
        "title": "The Cash Illusion Trap",
        "script": "Rich people never keep their cash in a bank account. Because inflation silently steals your purchasing power while banks lend your money out ten times over. Instead, the wealthy borrow against assets that appreciate, completely avoiding capital gains taxes. And the hidden reason why millionaires refuse to hold paper currency is because...",
        "loop_bridge": "...refuse to hold paper currency is because... Rich people never keep their cash in a bank account.",
        "caption": "Why storing cash in a savings account is making you quietly poorer. 🏦💸\n\n📌 SAVE this reel to review the 3 rules of capital velocity.\n👇 Comment 'WEALTH' to access our free passive income blueprint.\n.\n#wealthsecrets #financialfreedom #moneytok #investing #passiveincome #entrepreneurmindset #richmindset #businesshacks #reelsviral #curiosreturns",
        "pinned_comment": "🚨 Want to build automated cash flow this year? Grab our free blueprint via link in bio! 🔗📈"
    },
    {
        "niche": "wealth_secrets",
        "title": "The Forty Year Auction",
        "script": "A salaried job is an auction where you sell forty years of your life to the lowest bidder. If your income stops the second you stop working, you don't have a career, you have an hourly cage. The only real escape is building automated digital assets that make money while you sleep. And the brutal truth about why ninety-nine percent of people remain trapped is that...",
        "loop_bridge": "...remain trapped is that... A salaried job is an auction where you sell forty years of your life.",
        "caption": "Escape the 9 to 5 matrix before you run out of years. ⏳💼\n\nDrop a '💯' if you refuse to stay trapped in a cube.\nSave this as your daily wake-up reminder.\n.\n#escapethematrix #sidehustle #digitalassets #financialindependence #hustle #millionairemindset #onlinebusiness #reels #curiosreturns",
        "pinned_comment": "💡 Start building an automated income asset today. Free guide linked in bio! 🚀"
    },

    # --- 2. SECRET AI TOOLS (TECH TUESDAY) ---
    {
        "niche": "ai_glitches",
        "title": "Secret AI Tools That Feel Illegal",
        "script": "These three secret AI tools feel completely illegal to know. Number one is Gamma app, which generates full cinematic presentations in ten seconds. Number two is ElevenLabs, which clones any human voice in any language with zero recording gear. And number three is a private cheat sheet that top CEOs use in total silence, which proves that...",
        "loop_bridge": "...which proves that... These three secret AI tools feel completely illegal to know.",
        "caption": "Save this before big tech tries to hide these tools! 🤖⚡\n\nWhich of these 3 are you using first? Drop a comment below!\n🔗 Access our curated vault of 100+ Free AI shortcuts via link in bio.\n.\n#aitools #artificialintelligence #techhacks #productivitytools #secretwebsites #chatgpt #technews #lifehacks #viralreels #curiosreturns",
        "pinned_comment": "🔥 Dropping 10 new secret AI tools every week. Link in bio to access the private database! 📲"
    },
    {
        "niche": "ai_glitches",
        "title": "The Reverse ChatGPT Prompt",
        "script": "Stop using ChatGPT like a simple search engine. Most people get generic answers because they never tell the AI who it is. Always start your prompt with: 'Act as a ruthless McKinsey partner and tear apart my business idea with brutal honesty.' The sheer depth of the output will leave you speechless, proving that...",
        "loop_bridge": "...proving that... Stop using ChatGPT like a simple search engine.",
        "caption": "The prompt formula top creators and founders use in silence. 🧠📋\n\n📌 Tap SAVE so you don't lose this prompt formula.\nComment 'PROMPT' for our free cheat sheet.\n.\n#chatgptprompts #openai #ai #productivityhacks #smartwork #techtrends #digitalcreators #aitips #futureofwork #curiosreturns",
        "pinned_comment": "🚀 The complete Master Prompt Vault is linked in our bio. Free for the next 48 hours!"
    },

    # --- 3. DARK PSYCHOLOGY (PSYCHOLOGY WEDNESDAY & SATURDAY) ---
    {
        "niche": "dark_psychology",
        "title": "The Silence Weapon",
        "script": "If someone tries to insult you in public, never get angry. Just look them calmly in the eyes and ask: 'Are you okay?' Then stay completely silent. The sudden awkward vacuum forces them to feel the humiliating weight of their own words in front of everyone. And the psychology behind disarming any bully with zero effort begins when...",
        "loop_bridge": "...begins when... If someone tries to insult you in public, never get angry.",
        "caption": "How to handle disrespect like a master. 🤫♟️ Share this with someone who needs it.\n.\n#confidence #mindset #selfrespect #darkpsychology #stoic #communicationtips #powerdynamics #reelsvideo #viralreels #curiosreturns",
        "pinned_comment": "👑 True power is control over your reaction. Tap the link in bio for daily mindset tools. 🔗"
    },
    {
        "niche": "dark_psychology",
        "title": "The Subconscious Nod Trap",
        "script": "Master negotiators use a subtle hypnosis trick called physical pacing. Whenever you want someone to agree with your proposal, nod your head gently three times while delivering your key point. Their mirror neurons automatically mimic the movement, making their subconscious feel in total agreement with you. And the easiest way to test this persuasive hack is because...",
        "loop_bridge": "...is because... Master negotiators use a subtle hypnosis trick called physical pacing.",
        "caption": "The psychological body language trick that works on anyone. ♟️👁️\n\nHave you ever caught someone doing this to you? Tell us below!\nSave this mental model.\n.\n#darkpsychology #persuasion #negotiation #influence #psychologytricks #mindgames #powerdynamics #reelsviral #curiosreturns",
        "pinned_comment": "🧠 Want deeper psychological power laws? Check the reading list in our bio. 📚"
    },

    # --- 4. BIZARRE SCIENCE & SPACE (CURIOUS THURSDAY) ---
    {
        "niche": "mind_facts",
        "title": "The Ocean Abyss Paradox",
        "script": "The deepest parts of our oceans are more mysterious than outer space. Over eighty percent of Earth's ocean floor is completely unmapped and unexplored. In the pitch-black Mariana Trench, the crushing pressure would instantly collapse fifty jumbo jets stacked on your chest, yet alien creatures thrive there in complete silence, proving that...",
        "loop_bridge": "...proving that... The deepest parts of our oceans are more mysterious than outer space.",
        "caption": "The alien world right here beneath our feet. 🌊🦑\n\nWould you dare dive to the bottom of the Mariana Trench? Yes or No? 👇\nSave for daily curiosities.\n.\n#deepsea #oceanmysteries #unbelievablefacts #sciencefacts #marianatrench #nature #earth #mindblown #reels #curiosreturns",
        "pinned_comment": "🌊 Tap follow for mind-expanding discoveries every single day! 🌍✨"
    },
    {
        "niche": "mind_facts",
        "title": "The Terrifying Silence of Space",
        "script": "In outer space, sound is physically impossible. Because sound waves require a medium like air or water to travel, cosmic explosions larger than a thousand suns occur in complete, haunting, dead silence. If you stood next to a collapsing supernova, you would hear nothing at all, which is why...",
        "loop_bridge": "...which is why... In outer space, sound is physically impossible.",
        "caption": "Space is terrifyingly quiet. 🌌🚀 Would you go out into the dark void?\n.\n#space #astronomy #universe #cosmos #galaxy #spacetok #terrifyingfacts #mindblown #reelsviral #curiosreturns",
        "pinned_comment": "🪐 Follow @curiosreturns for daily cosmic chills and deep science. ✨"
    },

    # --- 5. STOIC RULES FOR THE ELITE (STOIC FRIDAY) ---
    {
        "niche": "stoic_wisdom",
        "title": "Rule of the Unseen Move",
        "script": "Moving in silence is the only way to protect your ambition. When you broadcast your goals before achieving them, your brain releases premature dopamine, tricking you into feeling like you've already won. Real monsters work in the dark and let results make the noise. Because at the highest level of mastery...",
        "loop_bridge": "...at the highest level of mastery... Moving in silence is the only way to protect your ambition.",
        "caption": "Move like a ghost until it's checkmate. 🐺♟️\n\nType 'DISCIPLINE' if you are leveling up in silence this year.\n.\n#stoicism #sigma #marcusaurelius #successmindset #discipline #darkaesthetic #innerstrength #focus #mindsetshift #curiosreturns",
        "pinned_comment": "⚡ Join 10,000+ ambitious minds leveling up daily. Free guide linked in bio! 🏛️"
    },
    {
        "niche": "stoic_wisdom",
        "title": "The Unbothered Mindset",
        "script": "Marcus Aurelius wrote that you have power over your mind, not outside events. The moment you realize this, you unlock invincible mental strength. The rude opinions of other people cannot penetrate your peace unless you give them permission to. And the foundational secret to becoming emotionally bulletproof is knowing that...",
        "loop_bridge": "...bulletproof is knowing that... Marcus Aurelius wrote that you have power over your mind, not outside events.",
        "caption": "Protect your inner peace at all costs. 🏛️⚡ Drop a 💯 if you agree.\n.\n#stoicism #marcusaurelius #stoicmindset #discipline #innerpeace #dailymotivation #wisdom #philosophy #sigma #curiosreturns",
        "pinned_comment": "🏛️ The Stoic Blueprint: Free reading list and daily laws linked in bio! 📜"
    },

    # --- 6. EXPANDED VAULT FOR 10X DAILY REACH ---
    {
        "niche": "wealth_secrets",
        "title": "The Velocity of Capital",
        "script": "Poor people hoard money, middle class people spend money, but the wealthy accelerate money. If a dollar sits idle, it loses value every minute to monetary debasement. Elite investors recycle the same dollar into multiple cash-flowing assets simultaneously. And the reason why compound interest only benefits the ultra-rich is that...",
        "loop_bridge": "...the ultra-rich is that... Poor people hoard money, middle class people spend money.",
        "caption": "Money is energy. If it doesn't move, it dies. 💸⚡ Save this financial law!\n.\n#moneyrules #investing #wealthbuilding #financialfreedom #smartmoney #curiosreturns",
        "pinned_comment": "📈 Want to understand cash flow velocity? Free guide in our bio! 🔗"
    },
    {
        "niche": "dark_psychology",
        "title": "The Triangle Gaze Technique",
        "script": "To instantly project magnetic charisma without saying a word, use the golden triangle gaze. When looking at someone, drift your eyes from their left eye, to their right eye, then down to their lips, and back up. This activates subconscious attraction and intense authority in human psychology. And the reason people feel captivated by you is because...",
        "loop_bridge": "...captivated by you is because... To instantly project magnetic charisma without saying a word, use the golden triangle gaze.",
        "caption": "Master silent magnetism in conversation. 👁️♟️ Save this technique.\n.\n#charisma #bodylanguage #darkpsychology #confidence #socialskills #curiosreturns",
        "pinned_comment": "♟️ Master the unseen laws of human magnetism. Bio link for the full list! 📚"
    },
    {
        "niche": "ai_glitches",
        "title": "The 60 Second Website Glitch",
        "script": "Web designers hate this one AI tool because it builds an entire responsive business website in sixty seconds. You simply type your business idea, and it writes the sales copy, sources full HD imagery, and wires payments automatically. It turns a ten thousand dollar project into zero dollars, proving that...",
        "loop_bridge": "...into zero dollars, proving that... Web designers hate this one AI tool because it builds an entire responsive website.",
        "caption": "Stop paying agencies thousands for simple websites. 🤖⚡ Save this before it gets taken down!\n.\n#aitools #webdesign #freelancehacks #sidehustle #digitalbusiness #curiosreturns",
        "pinned_comment": "🚀 100+ Free AI shortcuts in our bio database! Tap the link now! 📲"
    },
    {
        "niche": "mind_facts",
        "title": "The Greenland Shark Longevity",
        "script": "Deep beneath the Arctic ice swims a creature born before the American Revolution. The Greenland shark can live for over four hundred years in total darkness, with a heartbeat of just one pulse every twelve seconds. They don't even reach adulthood until they are one hundred and fifty years old, which means...",
        "loop_bridge": "...means... Deep beneath the Arctic ice swims a creature born before the American Revolution.",
        "caption": "Swimming through time since the 1600s. 🦈❄️ What would you do with 400 years?\n.\n#oceanfacts #mindblown #ancientcreatures #arctic #biology #curiosreturns",
        "pinned_comment": "🌊 Daily bizarre ocean & science curiosities. Tap follow! ✨"
    },
    {
        "niche": "stoic_wisdom",
        "title": "The Amor Fati Shield",
        "script": "Whatever burns down in your life is simply fuel for your next chapter. The ancient stoics lived by Amor Fati: loving your fate, no matter how brutal it feels. When a plan fails, you don't mourn, you adapt and attack from a higher angle. Because the only way to become truly unstoppable is knowing that...",
        "loop_bridge": "...unstoppable is knowing that... Whatever burns down in your life is simply fuel for your next chapter.",
        "caption": "Turn adversity into pure power. 🐺🏛️ Drop a 🔥 if you live by Amor Fati.\n.\n#stoicism #resilience #sigma #innerstrength #amorfati #marcusaurelius #curiosreturns",
        "pinned_comment": "🏛️ The Stoic Mastery Blueprint: Claim your free copy via bio! 📜"
    },

    # --- 7. LEGENDARY INDIAN HEROES & UNSUNG WARRIORS ---
    {
        "niche": "indian_heroes",
        "title": "The Mughal Nightmare Shivaji",
        "script": "The Mughal Empire had fifty times more soldiers, but they were terrified of one man. Chhatrapati Shivaji Maharaj mastered guerrilla warfare, striking from the mountain mist before vanishing into the Sahyadri ranges. He built India's first modern navy with over three hundred warships to guard our coastlines from foreign invaders. And the legendary reason why his name still inspires millions today is that...",
        "loop_bridge": "...inspires millions today is that... The Mughal Empire had fifty times more soldiers, but they were terrified of one man.",
        "caption": "The Father of the Indian Navy and master of guerrilla warfare. 🚩⚔️\n\nType 'JAI SHIVAJI' if you honor his timeless legacy!\n📌 SAVE and SHARE this heroic tribute.\nFollow @curiosreturns for daily epic Indian history & heroes.\n.\n#shivajimaharaj #marathaempire #indianhistory #heroesofindia #warriors #bharat #chhatrapatishivajimaharaj #historyfacts #reelsindia #curiosreturns",
        "pinned_comment": "🚩 Har Har Mahadev! Follow @curiosreturns to honor India's greatest heroes daily! 🇮🇳✨"
    },
    {
        "niche": "indian_heroes",
        "title": "Maharana Pratap and Chetak",
        "script": "Emperor Akbar offered him half the subcontinent if he would only bow his head. Maharana Pratap refused, choosing to eat bread made from grass in the Aravali jungles rather than surrender his self-respect. In the battle of Haldighati, his loyal warhorse Chetak leaped onto an armored elephant to protect him despite fatal wounds. And the reason why no empire could ever crush Mewar's spirit was that...",
        "loop_bridge": "...crush Mewar's spirit was that... Emperor Akbar offered him half the subcontinent if he would only bow his head.",
        "caption": "The warrior king who never bowed to any emperor. ⚔️🛡️\n\nDrop a 🚩 to salute the unmatched courage of Maharana Pratap & Chetak!\n.\n#maharanapratap #chetak #rajputwarriors #indianhistory #bravery #haldighati #bharatkeveer #historicalfacts #curiosreturns",
        "pinned_comment": "🇮🇳 Real heroes never bow down. Follow @curiosreturns for untold stories of Indian legends! 📜"
    },
    {
        "niche": "indian_heroes",
        "title": "The Escape of Netaji Bose",
        "script": "The British Empire considered him their single most dangerous adversary. Netaji Subhash Chandra Bose executed the greatest escape in history, slipping past British intelligence in disguise through Kabul, Moscow, and Berlin. He built the Azad Hind Fauj of forty thousand soldiers to wage open war for India's freedom. And the chilling secret why British rule finally collapsed in India was that...",
        "loop_bridge": "...finally collapsed in India was that... The British Empire considered him their single most dangerous adversary.",
        "caption": "Give me blood, and I will give you freedom! 🇮🇳🔥\n\nDrop a 'JAI HIND' in the comments to honor Netaji Subhash Chandra Bose!\n.\n#netaji #subhashchandrabose #azadhindfauj #freedomfighters #indianhistory #jaihind #patriotism #reelsviral #curiosreturns",
        "pinned_comment": "🔥 Inquilab Zindabad! Share this tribute to Netaji with every proud Indian! 🇮🇳"
    },
    {
        "niche": "indian_heroes",
        "title": "The Smiling Martyr Bhagat Singh",
        "script": "He walked to the gallows smiling with a book in his hand. Shaheed Bhagat Singh was only twenty-three years old when the British executed him in total secret before dawn. When offered a final pardon, he refused to apologize, proving that you can kill a revolutionary, but you cannot kill an idea. And the undeniable reason why his courage shook the entire empire was that...",
        "loop_bridge": "...shook the entire empire was that... He walked to the gallows smiling with a book in his hand.",
        "caption": "Executed at 23, immortal forever. 🕊️🇮🇳\n\nType 'INQUILAB' if you are inspired by Bhagat Singh's fearless soul.\n.\n#bhagatsingh #shaheedbhagatsingh #inquilabzindabad #freedomfighters #bharat #youthpower #legendsofindia #curiosreturns",
        "pinned_comment": "🇮🇳 Ideas never die. Save this reel to remember true courage. 📌"
    },
    {
        "niche": "indian_heroes",
        "title": "Captain Vikram Batra Kargil 1999",
        "script": "His radio code name struck pure terror into enemy bunkers on Point 4875. Captain Vikram Batra was nicknamed Shershah during the Kargil War of 1999. Ordered to recapture vertical peak 5140 at seventeen thousand feet, he charged through machine gun fire, roaring 'Yeh Dil Maange More'. He saved his injured junior officer before taking a fatal bullet, proving that...",
        "loop_bridge": "...taking a fatal bullet, proving that... His radio code name struck pure terror into enemy bunkers on Point 4875.",
        "caption": "Yeh Dil Maange More! 🎖️🇮🇳 Saluting Param Vir Chakra Captain Vikram Batra.\n\nDrop a ❤️ for our brave Indian Armed Forces!\n.\n#vikrambatra #shershah #kargilwar #paramvirchakra #indianarmy #indianheroes #jaihind #bharat #curiosreturns",
        "pinned_comment": "🇮🇳 The brave die never. Salute to our soldiers! Follow @curiosreturns for daily bravery reels. 🎖️"
    },
    {
        "niche": "indian_heroes",
        "title": "Rani Lakshmibai of Jhansi",
        "script": "She rode onto the battlefield with her young son tied firmly to her back. When the British ordered her to surrender Jhansi, Rani Lakshmibai drew two swords and declared 'I shall not give up my Jhansi.' She fought entire British battalions hand-to-hand on horseback until her final breath. And the legendary fire that ignited the 1857 freedom uprising began when...",
        "loop_bridge": "...freedom uprising began when... She rode onto the battlefield with her young son tied firmly to her back.",
        "caption": "Khoob Ladi Mardani Woh Toh Jhansi Wali Rani Thi! ⚔️👑\n\nSalute to the warrior queen who terrified the British Empire!\n.\n#ranilakshmibai #jhansi #warriorqueen #womenofindia #1857revolt #indianhistory #bravery #curiosreturns",
        "pinned_comment": "👑 Courage has no gender. Tap follow to honor the fierce queens of Bharat! 🇮🇳✨"
    },
    {
        "niche": "indian_heroes",
        "title": "APJ Abdul Kalam The Peoples President",
        "script": "He sold morning newspapers on the streets to pay for his school books. Dr. APJ Abdul Kalam failed his childhood dream of becoming a fighter pilot by just one rank. Instead of giving up, he built India's indigenous satellite rockets and the Agni missile defense shield with total self-reliance. And the inspiring reason why he is loved by every Indian is that...",
        "loop_bridge": "...loved by every Indian is that... He sold morning newspapers on the streets to pay for his school books.",
        "caption": "From selling newspapers to becoming the Missile Man of India. 🚀📖\n\nWhat is your favorite quote by Dr. Kalam? Drop it below!\n.\n#apjabdulkalam #missileman #inspiration #dreambig #indianheroes #scienceandtech #isro #curiosreturns",
        "pinned_comment": "✨ Dream is not that which you see while sleeping, it is something that does not let you sleep. 🇮🇳"
    },
    {
        "niche": "indian_heroes",
        "title": "Baji Prabhu The Spartan of Bharat",
        "script": "Three hundred Marathas stood firm against an advancing army of ten thousand men. In 1660, Baji Prabhu Deshpande guarded the narrow mountain pass of Ghodkhind so Shivaji Maharaj could reach safety. Struck by dozens of enemy swords, he refused to collapse until he heard five cannon shots echoing from the fort. And the reason history calls this the Indian Battle of Thermopylae is that...",
        "loop_bridge": "...Thermopylae is that... Three hundred Marathas stood firm against an advancing army of ten thousand men.",
        "caption": "The supreme sacrifice of Baji Prabhu Deshpande at Pavan Khind. ⚔️🚩\n\n300 held off 10,000. True warrior blood.\n.\n#pavankhind #marathawarriors #bajiprabhu #indianhistory #bravery #sacrifice #bharat #curiosreturns",
        "pinned_comment": "🚩 Unmatched valor. Follow @curiosreturns to discover untold Indian battle epics! 📜"
    }
]

def generate_script_with_ai(niche: str, api_key: str):
    """
    Generates a high-conversion viral reel script using Google Gemini API
    with strict SEAMLESS INFINITE LOOPING architecture.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt = f"""
    You are an elite short-form video copywriter specializing in 7-figure viral faceless reels (Instagram, TikTok, YouTube Shorts).
    Topic Niche: {niche}.
    
    CRITICAL SEAMLESS INFINITE LOOP REQUIREMENT:
    The script MUST be written as a continuous, endless loop.
    The very last phrase of the script MUST grammatically connect into the very first sentence so that when the video restarts automatically, the viewer hears ONE CONTINUOUS UNBROKEN SENTENCE.
    Example:
    First words: 'Most people don't know that sharks are older than trees.'
    Body: '...they have survived four global mass extinctions while trees evolved much later...'
    Last words: '...and the most terrifying fact about prehistoric biology is that...'
    (Loop: '...prehistoric biology is that... Most people don't know that sharks are older than trees.')
    
    Rules:
    1. Spoken Word Count: Exactly 50 to 70 words (~20 to 28 seconds of speech).
    2. Zero Fluff: Rapid value, high dopamine.
    3. Return ONLY a valid JSON object with keys:
    - "title": Short 3-5 word title
    - "script": Spoken voiceover text only (with the loop bridge at the end)
    - "loop_bridge": Explanation of how the end links to the start
    - "caption": Catchy caption with emoji formatting, debate question, save trigger, and 15 viral hashtags
    - "pinned_comment": High-converting marketing pinned comment driving to bio link.
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }
    
    try:
        res = requests.post(url, headers=headers, json=payload, timeout=20)
        if res.status_code == 200:
            data = res.json()
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
            parsed = json.loads(raw_text)
            parsed["niche"] = niche
            return parsed
    except Exception as e:
        print(f"[!] AI generation fallback (Error: {e}). Using viral database instead.")
    return None

def get_next_script(preferred_niche="random"):
    gemini_key = get_config("GEMINI_API_KEY", "").strip()
    last_niche = get_last_niche()
    
    available_niches = ["daily_news", "wealth_secrets", "ai_glitches", "dark_psychology", "mind_facts", "stoic_wisdom"]
    
    if preferred_niche == "random":
        # Strictly ensure consecutive videos NEVER share the same niche!
        valid_niches = [n for n in available_niches if n != last_niche]
        niche = random.choice(valid_niches) if valid_niches else random.choice(available_niches)
    else:
        niche = preferred_niche
        
    print(f"[*] Content Strategy: Rotating to niche '{niche}' (Previous: '{last_niche or 'None'}')")

    # Real-Time Daily Breaking News & Information (Guaranteed 100% Unique Stories)
    if niche.startswith("daily_news"):
        cat = "ALL"
        if "world" in niche:
            cat = "WORLD"
        elif "science" in niche:
            cat = "SCIENCE"
        elif "tech" in niche:
            cat = "TECH"
            
        print(f"[*] Sourcing fresh, unseen breaking news headline for [{cat}] News Brief...")
        news_reel = build_news_reel_script(preferred_category=cat)
        if news_reel:
            print(f"[*] Generated Real-Time News Reel: '{news_reel['title']}'")
            print(f"    [LOOP CONNECTION]: \"{news_reel['loop_bridge']}\"")
            return news_reel

    if gemini_key:
        print(f"[*] Generating seamless infinite loop AI script for '{niche}' via Gemini...")
        ai_script = generate_script_with_ai(niche, gemini_key)
        if ai_script and not is_title_used(ai_script.get("title", "")):
            record_used_content(title=ai_script["title"], niche=niche)
            return ai_script
            
    # Deduplicate against history registry
    candidates = [item for item in VIRAL_LIBRARY if item["niche"] == niche and not is_title_used(item["title"])]
    if not candidates:
        print(f"[i] All scripts in '{niche}' have been shown. Recycling unseen library scripts...")
        candidates = [item for item in VIRAL_LIBRARY if not is_title_used(item["title"])]
    if not candidates:
        candidates = VIRAL_LIBRARY
        
    chosen = random.choice(candidates).copy()
    record_used_content(title=chosen["title"], niche=chosen["niche"])
    
    # Custom epic Indian voice & Saffron palette for Indian heroes
    if chosen.get("niche") == "indian_heroes":
        chosen["voice"] = "en-IN-PrabhatNeural"
        chosen["subtitle_color"] = "&H0000A5FF"
        
    print(f"[*] Selected UNSEEN seamless loop script: '{chosen['title']}' [Niche: {chosen['niche']}]")
    if "loop_bridge" in chosen:
        print(f"    [LOOP CONNECTION]: \"{chosen['loop_bridge']}\"")
    return chosen

if __name__ == "__main__":
    s = get_next_script("indian_heroes")
    print("\n--- TEST INDIAN HEROES REEL ---")
    print("Title:", s.get("title"))
    print("Voice:", s.get("voice"))
    print("Color:", s.get("subtitle_color"))
    print("Script:", s.get("script"))
    print("Loop Bridge:", s.get("loop_bridge"))
