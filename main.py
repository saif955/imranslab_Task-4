from pathlib import Path
from moviepy.editor import VideoFileClip, concatenate_videoclips

# Output target (will be created if missing)
OUTPUT_DIR = Path("media/videos/Compiled/1080p60")
OUTPUT_FILE = OUTPUT_DIR / "Final.mp4"

# Known scene outputs to concatenate in order (edit as needed)
EXPECTED_VIDEOS = [
    Path("media/videos/opening_branding/1080p60/OpeningBranding.mp4"),
    Path("media/videos/starship_liftoff/1080p60/StarshipLiftoff.mp4"),
    Path("media/videos/starship_scene/1080p60/StarshipBuild.mp4"),
]


def main() -> None:
    clips = []
    for video_path in EXPECTED_VIDEOS:
        if not video_path.exists():
            print(f"[WARN] Skipping missing video: {video_path}")
            continue
        print(f"[INFO] Adding: {video_path}")
        clips.append(VideoFileClip(str(video_path)))

    if not clips:
        raise SystemExit("No input videos found. Render scenes first, then rerun this script.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[INFO] Concatenating {len(clips)} clip(s) → {OUTPUT_FILE}")
    final = concatenate_videoclips(clips, method="compose")
    # Use a common codec/bitrate; adjust if needed
    final.write_videofile(
        str(OUTPUT_FILE),
        codec="libx264",
        audio_codec="aac",
        fps=60,
        preset="medium",
        bitrate="8000k",
    )
    final.close()
    for c in clips:
        c.close()
    print("[DONE] Final video written.")


if __name__ == "__main__":
    main()


