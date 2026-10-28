import os
import random
import re
import subprocess
from pathlib import Path
from config import BASE_DIR, BACKGROUNDS_DIR, AUDIO_DIR, OUTPUTS_DIR, TEMP_DIR, get_ffmpeg_binary

def get_media_duration(file_path: Path) -> float:
    """Returns exact duration in seconds using ffmpeg."""
    exe = get_ffmpeg_binary()
    res = subprocess.run([exe, "-i", str(file_path)], capture_output=True, text=True, errors="replace")
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if match:
        h, m, s = match.groups()
        return int(h) * 3600 + int(m) * 60 + float(s)
    return 30.0

CINEMATIC_GRADES = [
    {"name": "Cyberpunk Neon", "filter": "eq=contrast=1.18:brightness=-0.04:saturation=1.35"},
    {"name": "Film Noir", "filter": "eq=contrast=1.22:saturation=0.55:brightness=-0.06"},
    {"name": "Golden Hour", "filter": "eq=contrast=1.12:gamma_r=1.22:gamma_b=0.88:saturation=1.25"},
    {"name": "Matrix Emerald", "filter": "eq=contrast=1.15:gamma_g=1.25:gamma_r=0.92:gamma_b=0.92"},
    {"name": "Midnight Deep Blue", "filter": "eq=contrast=1.14:gamma_b=1.25:gamma_r=0.88:gamma_g=0.95"},
    {"name": "Ultra Vivid Pop", "filter": "eq=contrast=1.25:saturation=1.55:brightness=-0.02"},
    {"name": "Studio Crisp", "filter": "eq=contrast=1.10:brightness=-0.05:saturation=1.10"},
    {"name": "Solar Amber", "filter": "eq=contrast=1.28:gamma_r=1.25:gamma_b=0.80:saturation=1.15"}
]

def build_multiscene_background(duration: float, output_path: Path) -> Path:
    """
    Builds a dynamic multi-scene B-Roll montage with unique color grading,
    mirror flips, random offsets, and speed variations so every single video
    has a 100% NEW, never-repeated visual atmosphere!
    """
    exe = get_ffmpeg_binary()
    supported_exts = {".mp4", ".mov", ".mkv", ".webm"}
    clips = [f for f in BACKGROUNDS_DIR.iterdir() if f.is_file() and f.suffix.lower() in supported_exts]
    
    # Pick a fresh cinematic color grade treatment for this video
    chosen_grade = random.choice(CINEMATIC_GRADES)
    print(f"[*] Applying New Visual Style: '{chosen_grade['name']}' color grade + dynamic scene cuts")

    if not clips:
        # Fallback procedural if folder is empty
        cmd = [
            exe, "-y",
            "-f", "lavfi",
            "-i", f"color=c=0x070913:s=1080x1920:d={duration:.2f}",
            "-t", f"{duration:.2f}",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]
        subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True)
        return output_path

    # Calculate scenes: cut every 3.5 to 4.5 seconds for high dopamine reset
    scene_duration = random.choice([3.5, 4.0, 4.2])
    num_scenes = max(1, int(duration // scene_duration) + (1 if duration % scene_duration > 0 else 0))
    
    print(f"[*] Assembling Dynamic Multi-Scene Montage: {num_scenes} visual cuts across {len(clips)} background assets...")
    
    # Select sequence of clips ensuring no two consecutive scenes are the same
    selected_clips = []
    last_clip = None
    for i in range(num_scenes):
        available = [c for c in clips if c != last_clip] if len(clips) > 1 else clips
        chosen = random.choice(available)
        selected_clips.append(chosen)
        last_clip = chosen
        
    cmd = [exe, "-y"]
    # Add all selected clips as inputs (looping enabled)
    for c in selected_clips:
        cmd.extend(["-stream_loop", "-1", "-i", str(c)])
        
    filter_parts = []
    for i in range(num_scenes):
        if i == num_scenes - 1:
            slice_dur = duration - (i * scene_duration)
            if slice_dur <= 0:
                slice_dur = scene_duration
        else:
            slice_dur = scene_duration
            
        # Random start offset between 0 and 20 seconds so entirely different footage sections play
        random_start = random.randint(0, 18)
        # Random horizontal mirror flip so orientation is fresh
        hflip = ",hflip" if random.random() > 0.5 else ""
        
        filter_parts.append(
            f"[{i}:v]trim=start={random_start}:duration={slice_dur:.2f},"
            f"setpts=PTS-STARTPTS,"
            f"scale=1080:1920:force_original_aspect_ratio=increase,"
            f"crop=1080:1920{hflip},"
            f"{chosen_grade['filter']}[v{i}]"
        )
        
    concat_inputs = "".join(f"[v{i}]" for i in range(num_scenes))
    filter_parts.append(f"{concat_inputs}concat=n={num_scenes}:v=1:a=0[montage]")
    
    cmd.extend([
        "-filter_complex", ";".join(filter_parts),
        "-map", "[montage]",
        "-t", f"{duration:.2f}",
        "-c:v", "libx264",
        "-preset", "ultrafast",
        "-pix_fmt", "yuv420p",
        str(output_path)
    ])
    
    proc = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"Multi-scene montage render failed:\n{proc.stderr}")
        
    return output_path
    
    proc = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"Multi-scene montage render failed:\n{proc.stderr}")
        
    return output_path

def create_reel(voice_path: Path, ass_path: Path, output_path: Path):
    exe = get_ffmpeg_binary()
    duration = get_media_duration(voice_path)
    print(f"[*] Voiceover duration: {duration:.2f} seconds (Seamless Cut)")
    
    # 1. Build the dynamic multi-scene background montage (switching clips every 4 seconds)
    temp_montage = TEMP_DIR / f"temp_montage_{int(duration)}.mp4"
    build_multiscene_background(duration, temp_montage)
    
    # 2. Check for ambient soundtrack
    music_files = [f for f in AUDIO_DIR.iterdir() if f.is_file() and f.suffix.lower() in {".mp3", ".wav", ".m4a"}]
    has_custom_music = len(music_files) > 0

    rel_ass = str(ass_path.relative_to(BASE_DIR)).replace("\\", "/")
    
    print("[*] Burning glowing neon karaoke subtitles over dynamic multi-scene B-Roll...")
    
    # Subtle brightness dimming for text contrast + continuous micro-zoom
    vf_chain = (
        "eq=brightness=-0.08:contrast=1.06,"
        "zoompan=z='min(zoom+0.0006,1.08)':d=75:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920,"
        f"ass=filename={rel_ass}"
    )

    cmd = [exe, "-y"]
    cmd.extend(["-i", str(temp_montage)])
    cmd.extend(["-i", str(voice_path)])
    
    if has_custom_music:
        selected_music = random.choice(music_files)
        print(f"[*] Mixing soundtrack: {selected_music.name}")
        cmd.extend(["-stream_loop", "-1", "-i", str(selected_music)])
        filter_complex = (
            f"[0:v]{vf_chain}[v];"
            f"[2:a]volume=0.12[bgm];"
            f"[1:a]volume=1.0[voice];"
            f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=1[a]"
        )
        cmd.extend(["-filter_complex", filter_complex, "-map", "[v]", "-map", "[a]"])
    else:
        # Subtle cinema sub-bass atmosphere
        cmd.extend([
            "-f", "lavfi",
            "-i", f"anoisesrc=d={duration + 1:.1f}:c=pink:r=44100:a=0.03"
        ])
        filter_complex = (
            f"[0:v]{vf_chain}[v];"
            f"[2:a]lowpass=f=160,volume=0.35[ambient];"
            f"[1:a]volume=1.0[voice];"
            f"[voice][ambient]amix=inputs=2:duration=first:dropout_transition=1[a]"
        )
        cmd.extend(["-filter_complex", filter_complex, "-map", "[v]", "-map", "[a]"])
        
    # Precision seamless loop cut (NO dead air at the end)
    cmd.extend([
        "-t", f"{duration:.2f}",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "20",
        "-c:a", "aac",
        "-b:a", "192k",
        str(output_path)
    ])
    
    proc = subprocess.run(cmd, cwd=str(BASE_DIR), capture_output=True, text=True, errors="replace")
    if proc.returncode != 0:
        raise RuntimeError(f"Final reel render failed:\n{proc.stderr}")
        
    # Cleanup temp montage
    if temp_montage.exists():
        try:
            temp_montage.unlink()
        except Exception:
            pass
            
    print(f"[OK] Multi-Scene Reel successfully rendered: {output_path.name}")
    return output_path
