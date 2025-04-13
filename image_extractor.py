# This script extracts frames from a video file and saves them as images.
# It also generates a settings file for use with another script (gif_creator.py).

import cv2
from pathlib import Path
import json

# Supported video extensions
SUPPORTED_EXTS = [".mp4", ".mov", ".avi", ".mkv", ".webm"]

def extract_frames_smart():
    videos_folder = Path("Videos")
    images_folder = Path("Images")

    # Ask user for the base video name
    video_name = input("Enter the video name (without extension): ").strip()

    # Try to find the matching video file with supported extensions
    video_path = None
    for ext in SUPPORTED_EXTS:
        potential_path = videos_folder / f"{video_name}{ext}"
        if potential_path.exists():
            video_path = potential_path
            break

    if not video_path:
        print(f"No video found for '{video_name}' in '{videos_folder}'.")
        return

    # Open the video file
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print("Failed to open the video file.")
        return

    # Get video metadata
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps else 0

    print(f"\n🎥 Video loaded: {video_path.name}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Total frames: {frame_count}")
    print(f"FPS: {fps:.2f}")

    # Ask user for a base name to use for image files
    base_name = input("Enter a base name for the image files (e.g. 'anime'): ").strip()
    output_folder = images_folder / base_name
    output_folder.mkdir(parents=True, exist_ok=True)

    # Explain style options
    print("\nChoose your GIF style:")
    print("  smooth → very high frame count (~0.2s apart), ultra-fluid motion")
    print("  harsh  → fewer frames (~1.75s apart), stylised and punchy")

    # Ask user for desired style
    while True:
        style = input("Choose style - smooth or harsh: ").strip().lower()
        if style in ["smooth", "harsh"]:
            break
        print("Invalid choice. Type 'smooth' or 'harsh'.")

    # Determine capture interval and GIF speed based on style
    if style == "smooth":
        interval = 0.2
        gif_duration = 50
    else:
        interval = 1.75
        gif_duration = 200

    # Determine which frames to capture based on interval
    num_frames = int(duration / interval)
    step = int(frame_count / num_frames)
    frame_indices = [i * step for i in range(num_frames)]

    print(f"\nExtracting {num_frames} frame(s) at ~{interval:.2f}s intervals...")
    print(f"Output folder: {output_folder}")

    # Extract and save selected frames
    extracted = 0
    skipped = 0
    for i, frame_num in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if not ret:
            print(f"⚠️ Skipping unreadable frame at {frame_num}")
            skipped += 1
            continue
        filename = output_folder / f"{base_name}{i + 1}.png"
        cv2.imwrite(str(filename), frame)
        print(f"Saved: {filename.name}")
        extracted += 1

    cap.release()

    # Save settings for gif_creator.py to read
    settings = {
        "frame_count": extracted,
        "gif_duration": gif_duration,
        "base_name": base_name,
        "style": style,
        "output_folder": str(output_folder.resolve())
    }

    with open(output_folder / "settings.json", "w") as f:
        json.dump(settings, f, indent=4)

    print(f"\n✅ Done. {extracted} frames saved, {skipped} skipped.")
    print(f"🗒 settings.json written to '{output_folder}'.")

if __name__ == "__main__":
    extract_frames_smart()