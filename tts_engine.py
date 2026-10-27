import asyncio
import edge_tts
from pathlib import Path
from datetime import timedelta
import re
from config import get_config, TEMP_DIR

def format_ass_time(td: timedelta) -> str:
    """Format timedelta to ASS subtitle timestamp H:MM:SS.cc"""
    total_seconds = max(0.0, td.total_seconds())
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    centiseconds = int((total_seconds - int(total_seconds)) * 100)
    return f"{hours}:{minutes:02d}:{seconds:02d}.{centiseconds:02d}"

def generate_karaoke_dialogue_lines(cues, words_per_chunk=3, highlight_color="&H0024E0FB"):
    """
    Creates high-retention karaoke style lines where the CURRENT active word
    is highlighted with an enlarged pop effect (\fscx115\fscy115),
    matching the viral Alex Hormozi / MrBeast video editing style.
    """
    dialogue_lines = []
    
    for cue in cues:
        raw_text = cue.content.strip()
        words = raw_text.split()
        if not words:
            continue
            
        start_sec = cue.start.total_seconds()
        end_sec = cue.end.total_seconds()
        total_duration = max(0.4, end_sec - start_sec)
        
        chunks = []
        for i in range(0, len(words), words_per_chunk):
            chunks.append(words[i:i + words_per_chunk])
            
        chunk_duration = total_duration / len(chunks)
        
        for c_idx, chunk in enumerate(chunks):
            c_start = start_sec + c_idx * chunk_duration
            c_end = start_sec + (c_idx + 1) * chunk_duration
            num_words = len(chunk)
            word_duration = (c_end - c_start) / max(1, num_words)
            
            for w_idx in range(num_words):
                w_start = c_start + w_idx * word_duration
                w_end = c_start + (w_idx + 1) * word_duration
                
                rendered_words = []
                for idx, w in enumerate(chunk):
                    clean_w = w.upper()
                    if idx == w_idx:
                        # Highlight active word with custom day palette & bounce pop
                        rendered_words.append(f"{{\\c{highlight_color}\\fscx114\\fscy114}}{clean_w}{{\\r}}")
                    else:
                        rendered_words.append(clean_w)
                        
                line_text = " ".join(rendered_words)
                start_str = format_ass_time(timedelta(seconds=w_start))
                end_str = format_ass_time(timedelta(seconds=w_end))
                dialogue_lines.append(f"Dialogue: 0,{start_str},{end_str},ViralHormozi,,0,0,0,,{line_text}\n")
                
    return dialogue_lines

def generate_ass_subtitles(cues, output_path: Path, highlight_color="&H0024E0FB"):
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ViralHormozi,Arial,76,&H00FFFFFF,&H000000FF,&H00000000,&H90000000,-1,0,0,0,100,100,2,0,1,8,4,2,70,70,520,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    dialogues = generate_karaoke_dialogue_lines(cues, words_per_chunk=3, highlight_color=highlight_color)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(ass_header)
        f.writelines(dialogues)

async def synthesize_speech_and_subtitles(text: str, audio_path: Path, ass_path: Path, voice=None, highlight_color="&H0024E0FB"):
    selected_voice = voice or get_config("VOICE", "en-US-ChristopherNeural")
    print(f"[*] Synthesizing voiceover with voice: {selected_voice} (Accent: {highlight_color})...")
    
    comm = edge_tts.Communicate(text, selected_voice)
    submaker = edge_tts.SubMaker()
    
    with open(audio_path, "wb") as audio_file:
        async for chunk in comm.stream():
            if chunk["type"] == "audio":
                audio_file.write(chunk["data"])
            elif chunk["type"] in ("WordBoundary", "SentenceBoundary"):
                submaker.feed(chunk)
                
    generate_ass_subtitles(submaker.cues, ass_path, highlight_color=highlight_color)
    print(f"[OK] Neural audio saved: {audio_path.name}")
    print(f"[OK] Styled subtitles saved: {ass_path.name}")

def generate_voiceover(text: str, audio_path: Path, ass_path: Path, voice=None, highlight_color="&H0024E0FB"):
    asyncio.run(synthesize_speech_and_subtitles(text, audio_path, ass_path, voice=voice, highlight_color=highlight_color))

if __name__ == "__main__":
    t_audio = TEMP_DIR / "sample.mp3"
    t_ass = TEMP_DIR / "sample.ass"
    generate_voiceover("Master the unseen laws of leverage.", t_audio, t_ass, highlight_color="&H00FFFF00")
