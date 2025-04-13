# This script extracts frames from a video file and saves them as images.
# It also generates a settings file for use with another script (gif_creator.py).
# Updated to creat image based on video name.
# Updated the frame extraction logic to use numpy for accurate frame index distribution.
# Updated to synchronize the frame extraction with the video FPS.

import cv2
from pathlib import Path
import json
import numpy as np  # For accurate frame index distribution

SUPPORTED_EXTS = [".mp4", ".mov", ".avi", ".mkv", ".webm"]

def extract_frames_smart():
    videos_folder = Path("Videos")
    images_folder = Path("Images")

    video_name = input("Enter the video name (without extension): ").strip()

    video_path = None
    for ext in SUPPORTED_EXTS:
        potential_path = videos_folder / f"{video_name}{ext}"
        if potential_path.exists():
            video_path = potential_path
            break

    if not video_path:
        print(f"No video found for '{video_name}' in '{videos_folder}'.")
        return None

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print("Failed to open the video file.")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps else 0

    base_name = video_path.stem  # Use video filename (no extension)
    output_folder = images_folder / base_name
    output_folder.mkdir(parents=True, exist_ok=True)

    print(f"\n🎥 Video loaded: {video_path.name}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Total frames: {frame_count}")
    print(f"Original FPS: {fps:.2f}")

    # Define limits for frame rate input
    min_fps = 15
    max_fps = min(50, int(fps))  # Cap at 50 FPS or the video's original FPS

    print(f"\nChoose your target GIF frame rate:")
    print(f"  {min_fps} = stylised and harsh")
    print(f"  {max_fps} = ultra smooth (based on source FPS)")

    while True:
        fps_input = input(f"Enter target frame rate ({min_fps}–{max_fps}): ").strip()
        if fps_input.isdigit():
            target_fps = int(fps_input)
            if min_fps <= target_fps <= max_fps:
                break
        print(f"❌ Please enter a number between {min_fps} and {max_fps}.")

    num_frames = max(10, min(int(duration * target_fps), frame_count))
    frame_indices = np.linspace(0, frame_count - 1, num_frames, dtype=int)
    gif_duration = round((duration / num_frames) * 1000)

    print(f"\nExtracting {num_frames} frame(s)...")
    print(f"Output folder: {output_folder}")

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

    if extracted == 0:
        print("\n❌ No frames extracted. GIF creation will be skipped.")
        return None

    settings = {
        "frame_count": extracted,
        "gif_duration": gif_duration,
        "base_name": base_name,
        "style": f"{target_fps} fps",
        "output_folder": str(output_folder.resolve())
    }

    with open(output_folder / "settings.json", "w") as f:
        json.dump(settings, f, indent=4)

    print(f"\n✅ Done. {extracted} frames saved, {skipped} skipped.")
    print(f"🗒 settings.json written to '{output_folder}'.")
    return True

if __name__ == "__main__":
    extract_frames_smart()