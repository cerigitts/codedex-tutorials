# This script creates a GIF from images in a specified folder based on settings in a JSON file.
# It also provides options to delete the original images and preview the GIF in the system's default viewer.
# Updated to use PIL for GIF optimization and added error handling.
# Updated to correct resolution and aspect ratio handling.

import os
import json
import platform
import subprocess
from pathlib import Path
from PIL import Image  # For GIF optimization and resizing

def open_file(path):
    try:
        system = platform.system()
        if system == "Darwin":
            subprocess.run(["open", "-a", "Safari", path])
        elif system == "Windows":
            subprocess.run(["start", path], shell=True)
        elif system == "Linux":
            subprocess.run(["xdg-open", path])
        else:
            print("Preview not supported on this OS.")
    except Exception as e:
        print(f"Could not open the file: {e}")

def create_gif_from_settings():
    images_folder = Path("Images")

    # Find the most recent folder with a settings.json
    candidates = sorted(
        images_folder.glob("*/settings.json"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )
    if not candidates:
        print("No settings.json found in any subfolder of 'Images'.")
        return

    settings_path = candidates[0]
    with open(settings_path, "r") as f:
        settings = json.load(f)

    try:
        base_name, frame_count, gif_duration, output_folder = (
            settings["base_name"],
            settings["frame_count"],
            settings["gif_duration"],
            settings["output_folder"]
        )
    except KeyError as e:
        print(f"Settings file is missing a required value: {e}")
        return

    folder_path = Path(output_folder)

    print(f"\n🎯 Using settings from: {settings_path}")
    print(f"  Base name: {base_name}")
    print(f"  Frame count: {frame_count}")
    print(f"  GIF duration: {gif_duration} ms")

    # Load the first image to determine orientation and scaling box
    first_image_path = folder_path / f"{base_name}1.png"
    if not first_image_path.exists():
        print("❌ First frame is missing. Cannot determine aspect ratio.")
        return

    with Image.open(first_image_path) as img:
        orig_width, orig_height = img.size
        is_landscape = orig_width >= orig_height
        max_width = 640 if is_landscape else 480
        max_height = 480 if is_landscape else 640

        scale_factor = min(max_width / orig_width, max_height / orig_height)
        new_size = (int(orig_width * scale_factor), int(orig_height * scale_factor))

    print(f"🖼 Scaling all frames to fit within {max_width}x{max_height} (actual: {new_size})")

    # Load, resize, quantize
    images = []
    for i in range(1, frame_count + 1):
        image_file = folder_path / f"{base_name}{i}.png"
        if not image_file.exists():
            print(f"Missing image: {image_file.name} — skipping.")
            continue
        img = Image.open(image_file).convert("RGB")
        resized = img.resize(new_size, Image.LANCZOS)
        quantized = resized.convert("P", palette=Image.ADAPTIVE, colors=128)
        images.append(quantized)

    if not images:
        print("No valid images found. Cannot create GIF.")
        return

    # Determine FPS for filename
    fps = round(1000 / gif_duration)
    output_path = folder_path / f"{base_name}_{fps}fps.gif"

    # Save the optimized GIF
    images[0].save(
        output_path,
        save_all=True,
        append_images=images[1:],
        loop=0,
        duration=gif_duration,
        optimize=True
    )

    print(f"\n✅ GIF created: {output_path}")

    # Clean up extracted images and settings
    deleted = 0
    for i in range(1, frame_count + 1):
        img_file = folder_path / f"{base_name}{i}.png"
        if img_file.exists():
            img_file.unlink()
            deleted += 1

    settings_file = folder_path / "settings.json"
    if settings_file.exists():
        settings_file.unlink()

    print(f"🧹 Cleaned up {deleted} image(s) and settings.json")

    # Preview option
    preview = input("\n🔍 Do you want to preview the GIF now? (y/N): ").strip().lower()
    if preview == "y":
        open_file(str(output_path.resolve()))
    else:
        print("📁 GIF saved and ready.")

if __name__ == "__main__":
    create_gif_from_settings()
