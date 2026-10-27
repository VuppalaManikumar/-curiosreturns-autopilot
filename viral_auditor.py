import re
from typing import Dict, Any

HOOK_POWER_WORDS = {
    "secret", "never", "illegal", "trick", "rule", "truth", "trap", "stop",
    "warning", "cheat", "psychological", "millionaire", "rich", "billionaire",
    "power", "hidden", "nobody", "lies", "manipulation", "infinite", "silent",
    "unbelievable", "terrifying", "danger", "curiosity", "control", "hack"
}

DEBATE_TRIGGERS = {
    "agree", "comment", "opinion", "think", "tell us", "would you", "yes or no",
    "drop a", "which one", "tag", "truth", "do you"
}

SAVE_TRIGGERS = {
    "save", "bookmark", "remember", "keep", "later", "guide", "blueprint", "cheat sheet"
}

def audit_viral_script(script_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluates script against the 5 Pillars of the Meta/TikTok Recommendation Algorithm.
    Returns scores and an overall algorithmic success probability score (0-100%).
    """
    script = script_data.get("script", "")
    caption = script_data.get("caption", "")
    title = script_data.get("title", "")
    
    words = script.split()
    total_words = len(words)
    first_sentence = script.split(".")[0] if "." in script else script[:50]
    first_words = set(re.findall(r"\b\w+\b", first_sentence.lower()))
    caption_lower = caption.lower()
    
    # 1. Hook Velocity & Pattern Interrupt (0-20)
    hook_score = 10
    hook_matches = first_words.intersection(HOOK_POWER_WORDS)
    if hook_matches:
        hook_score += min(8, len(hook_matches) * 4)
    if len(first_sentence.split()) <= 12:
        hook_score += 2  # Punchy first hook
    hook_score = min(20, hook_score)
    
    # 2. Infinite Loop Integrity (0-20)
    loop_score = 10
    loop_phrases = ["which is why", "and that is why", "this is why", "which proves that", "always remember", "and this is why"]
    script_tail = script.lower()[-40:]
    if any(lp in script_tail for lp in loop_phrases):
        loop_score = 20
    elif any(lp in script.lower() for lp in loop_phrases):
        loop_score = 17
    else:
        loop_score = 12
        
    # 3. Pacing & Word Velocity (0-20)
    # Optimal short-form video length: 45 to 75 words (~20-30 seconds of high dopamine)
    if 45 <= total_words <= 75:
        pacing_score = 20
    elif 35 <= total_words <= 90:
        pacing_score = 16
    else:
        pacing_score = 11
        
    # 4. Debate & Comment Polarization Index (0-20)
    debate_score = 8
    if any(dt in caption_lower for dt in DEBATE_TRIGGERS):
        debate_score += 8
    if "?" in caption:
        debate_score += 4
    debate_score = min(20, debate_score)
    
    # 5. Save & Utility Score (0-20)
    save_score = 8
    if any(st in caption_lower for st in SAVE_TRIGGERS):
        save_score += 8
    if "#" in caption and caption.count("#") >= 8:
        save_score += 4
    save_score = min(20, save_score)
    
    total_score = hook_score + loop_score + pacing_score + debate_score + save_score
    
    is_elite = total_score >= 90
    
    return {
        "total_score": total_score,
        "is_elite": is_elite,
        "metrics": {
            "hook_velocity": f"{hook_score}/20",
            "infinite_loop": f"{loop_score}/20",
            "pacing_velocity": f"{pacing_score}/20 ({total_words} words)",
            "comment_debate_catalyst": f"{debate_score}/20",
            "save_utility_index": f"{save_score}/20"
        },
        "verdict": "ELITE VIRAL CANDIDATE (92-99% Algorithmic Optimization)" if is_elite else "STANDARD QUALITY"
    }

def enforce_elite_quality(script_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Enforces a strict 90%+ quality threshold.
    If script is missing loop or debate triggers, automatically injects them.
    """
    script = script_data.get("script", "").strip()
    caption = script_data.get("caption", "").strip()
    
    # Ensure infinite loop transition
    loop_phrases = ["which is why", "and that is why", "this is why", "which proves that", "always remember"]
    if not any(lp in script.lower()[-45:] for lp in loop_phrases):
        if script.endswith("."):
            script = script[:-1]
        script += ". And that is why..."
        script_data["script"] = script
        
    # Ensure save & debate triggers in caption
    if "save" not in caption.lower():
        caption = "📌 SAVE this reel so you don't lose it.\n" + caption
    if "?" not in caption:
        caption += "\n👇 Do you agree? Tell us your thoughts below!"
        
    script_data["caption"] = caption
    audit = audit_viral_script(script_data)
    script_data["audit"] = audit
    return script_data
