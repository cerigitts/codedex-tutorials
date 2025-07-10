# image_extractor.py
# Extract frames from a video file, with optional selection index control

import cv2
from pathlib import Path
import numpy as np
import os

SUPPORTED_EXTS = [".mp4", ".mov", ".avi", ".mkv", ".webm"]

def extract_frames(video_name, videos_folder=Path("Videos"), images_folder=Path("Images"),
                   max_width=640, max_height=480, selected_indices=None):
    video_path = None
    for ext in SUPPORTED_EXTS:
        candidate = videos_folder / f"{video_name}{ext}"
        if candidate.exists():
            video_path = candidate
            break

    if not video_path:
        print(f"No video found for '{video_name}' in '{videos_folder}'.")
        return None

    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print("Failed to open video.")
        return None

    orig_fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / orig_fps if orig_fps else 0

    ret, frame = cap.read()
    if not ret:
        print("Failed to read first frame.")
        return None

    orig_height, orig_width = frame.shape[:2]
    scale_factor = min(max_width / orig_width, max_height / orig_height, 1.0)
    new_width = int(orig_width * scale_factor)
    new_height = int(orig_height * scale_factor)

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    output_folder = images_folder / video_path.stem
    output_folder.mkdir(parents=True, exist_ok=True)

    frame_files = []
    frame_sizes = []

    if selected_indices is None:
        selected_indices = range(frame_count)

    for idx in selected_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        resized = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        filename = output_folder / f"frame_{idx:05d}.png"
        cv2.imwrite(str(filename), resized)
        frame_files.append(filename)
        size_bytes = filename.stat().st_size
        frame_sizes.append(size_bytes)

    cap.release()

    total_raw_size_mb = sum(frame_sizes) / (1024 * 1024)

    return {
        "output_folder": output_folder,
        "frame_files": frame_files,
        "frame_sizes": frame_sizes,
        "orig_fps": orig_fps,
        "duration": duration,
        "resolution": (new_width, new_height),
        "frame_count": len(frame_files),
        "total_raw_size_mb": total_raw_size_mb
    }