# This script creates a GIF from images in a specified folder based on settings in a JSON file.
# It also provides options to delete the original images and preview the GIF in the system's default viewer.

import imageio.v3 as iio  # ImageIO v3 API for reading/writing images and GIFs
from pathlib import Path  # Object-oriented path operations
import subprocess  # To open the output file using system commands
import platform  # Detect the current operating system
import json  # Read settings from JSON file
import os  # File handling and cleanup

# Open a file in the system's default viewer (Safari on macOS)
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

# Create a GIF using settings from settings.json
def create_gif_from_settings():
    images_folder = Path("Images")

    # Find the most recently updated subfolder with a settings.json
    candidates = sorted(
        images_folder.glob("*/settings.json"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )

    if not candidates:
        print("No settings.json found in any subfolder of 'Images'.")
        return

    settings_path = candidates[0]

    # Load JSON settings
    with open(settings_path, "r") as f:
        settings = json.load(f)

    base_name = settings.get("base_name")
    frame_count = settings.get("frame_count")
    gif_duration = settings.get("gif_duration")
    output_folder = settings.get("output_folder")

    folder_path = Path(output_folder) if output_folder else settings_path.parent

    if not all([base_name, frame_count, gif_duration]):
        print("Settings file is incomplete or corrupted.")
        return

    print(f"\n🎯 Using settings from: {settings_path}")
    print(f"  Base name: {base_name}")
    print(f"  Frame count: {frame_count}")
    print(f"  GIF duration: {gif_duration} ms")

    # Load images
    image_files = []
    for i in range(1, frame_count + 1):
        image_file = folder_path / f"{base_name}{i}.png"
        if not image_file.exists():
            print(f"Missing image: {image_file.name} — skipping.")
            continue
        image_files.append(iio.imread(image_file))

    if not image_files:
        print("No valid images found. Cannot create GIF.")
        return

    output_path = folder_path / f"{base_name}.gif"
    iio.imwrite(output_path, image_files, duration=gif_duration, loop=0)

    print(f"\n✅ GIF created: {output_path}")

    # Automatically delete images and settings.json
    deleted = 0
    for i in range(1, frame_count + 1):
        image_path = folder_path / f"{base_name}{i}.png"
        if image_path.exists():
            image_path.unlink()
            deleted += 1
    settings_file = folder_path / "settings.json"
    if settings_file.exists():
        settings_file.unlink()

    print(f"🧹 Cleaned up: {deleted} images and settings.json deleted.")

    # Ask to preview the GIF
    preview = input("\n🔍 Do you want to preview the GIF now? (y/N): ").strip().lower()
    if preview == "y":
        open_file(str(output_path.resolve()))
    else:
        print("📁 GIF saved and ready.")

if __name__ == "__main__":
    create_gif_from_settings()