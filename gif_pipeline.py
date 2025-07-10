# gif_pipeline.py
# Full GIF creation pipeline with frame-accurate selection using np.arange

import os
import numpy as np
from pathlib import Path
from image_extractor import extract_frames
from gif_creator import create_gif_from_frames

def estimate_compression_ratio(fps):
    return max(0.05, -0.0029 * fps + 0.3851)

def run_pipeline():
    video_name = input("🎥 Enter video name (without extension): ").strip()
    temp_info = extract_frames(video_name)
    if not temp_info:
        return

    print(f"\nVideo duration: {temp_info['duration']:.2f}s, original FPS: {temp_info['orig_fps']:.2f}")
    print(f"Resolution scaled to: {temp_info['resolution'][0]}×{temp_info['resolution'][1]}")
    print(f"Extracted {temp_info['frame_count']} frames.")
    print(f"Total size of extracted frames: {temp_info['total_raw_size_mb']:.2f} MB")

    # Delete all temp frames after estimation
    for f in temp_info['frame_files']:
        os.remove(f)

    max_fps = min(50, int(round(temp_info['orig_fps'])))
    print(f"\n⚠️ Max supported FPS for GIF: {max_fps}")
    target_fps = int(input(f"Enter target GIF FPS (max {max_fps}): "))

    frame_ratio = target_fps / temp_info["orig_fps"]
    effective_raw_size = temp_info["total_raw_size_mb"] * frame_ratio
    compression_ratio = estimate_compression_ratio(target_fps)
    estimated_size = round(effective_raw_size * compression_ratio, 2)

    print(f"\nEstimated compression ratio at {target_fps} FPS: {compression_ratio:.3f}")
    print(f"Estimated GIF size at {target_fps} FPS: {estimated_size} MB")

    proceed = input("Proceed with GIF creation? (Y/n): ").strip().lower()
    if proceed not in ["", "y", "yes"]:
        print("GIF creation aborted.")
        return

    step = temp_info["orig_fps"] / target_fps
    selected_indices = np.arange(0, temp_info["frame_count"], step).astype(int)

    print("\n🎞️ Re-extracting selected frames...")
    final_info = extract_frames(video_name, selected_indices=selected_indices)

    print("✨ Creating final GIF...")
    create_gif_from_frames(final_info["output_folder"], video_name,
                           final_info["frame_files"], target_fps)

if __name__ == "__main__":
    run_pipeline()
