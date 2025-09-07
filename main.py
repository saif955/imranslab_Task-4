#!/usr/bin/env python3
"""
One-command render of the whole film.
Renders all Manim scenes and compiles them into a single video.
"""
import subprocess
import sys
from pathlib import Path
from moviepy import VideoFileClip, concatenate_videoclips

# Scene files to render (in order)
SCENES = [
    ("intro.py", "LogoIntro"),
    ("starship_liftoff.py", "StarshipLiftoff"), 
    ("starship_scene.py", "StarshipBuild"),
    ("starship_mars_landing.py", "StarshipMarsLanding"),
    ("outro.py", "LogoOutro"),
]

# Output paths
OUTPUT_DIR = Path("media/videos/Compiled/1080p60")
FINAL_VIDEO = OUTPUT_DIR / "Complete_Film.mp4"

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🎬 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Success")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        print(f"stdout: {e.stdout}")
        print(f"stderr: {e.stderr}")
        return False

def main():
    print("🚀 Starting complete film render...")
    
    # Check if Manim is available
    try:
        subprocess.run(["manim", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Manim not found. Install with: pip install manim")
        sys.exit(1)
    
    # Render each scene
    rendered_videos = []
    for scene_file, scene_class in SCENES:
        if not Path(scene_file).exists():
            print(f"⚠️  Scene file not found: {scene_file}")
            continue
            
        # Expected output path
        video_path = Path(f"media/videos/{scene_file.replace('.py', '')}/1080p60/{scene_class}.mp4")
        
        # Render scene
        cmd = ["manim", "-pqh", scene_file, scene_class]
        if run_command(cmd, f"Rendering {scene_file} -> {scene_class}"):
            if video_path.exists():
                rendered_videos.append(video_path)
                print(f"✅ Rendered: {video_path}")
            else:
                print(f"⚠️  Video not found at expected path: {video_path}")
    
    if not rendered_videos:
        print("❌ No videos were rendered successfully.")
        sys.exit(1)
    
    # Compile all videos
    print(f"\n🎞️  Compiling {len(rendered_videos)} videos...")
    
    try:
        clips = []
        for video_path in rendered_videos:
            print(f"Adding: {video_path}")
            clips.append(VideoFileClip(str(video_path)))
        
        # Create output directory
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Concatenate videos
        print(f"Creating final video: {FINAL_VIDEO}")
        final = concatenate_videoclips(clips, method="compose")
        
        # Write final video
        final.write_videofile(
            str(FINAL_VIDEO),
            codec="libx264",
            audio_codec="aac", 
            fps=60,
            preset="medium",
            bitrate="8000k",
        )
        
        # Cleanup
        final.close()
        for clip in clips:
            clip.close()
            
        print(f"\n🎉 Complete film rendered: {FINAL_VIDEO}")
        print(f"📁 File size: {FINAL_VIDEO.stat().st_size / (1024*1024):.1f} MB")
        
    except Exception as e:
        print(f"❌ Error compiling videos: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()