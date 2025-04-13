# This script serves as the main entry point for the GIF creation process.
# It orchestrates the extraction of frames from a video and the creation of a GIF from those frames.
# It imports necessary functions from other modules and provides a simple command-line interface.

from image_extractor import extract_frames_smart  # Frame extraction logic
from gif_creator import create_gif_from_settings  # GIF creation and cleanup

# Run the full GIF creation pipeline
def run_full_pipeline():
    print("\n🎥 Starting full video-to-GIF pipeline...")
    result = extract_frames_smart()
    if not result:
        print("\n⚠️ Frame extraction failed or skipped. Aborting GIF generation.")
        return
    print("\n🎞️ Frame extraction complete. Now generating GIF...")
    create_gif_from_settings()
    print("\n🌟 Done. Your masterpiece is ready.")

if __name__ == "__main__":
    run_full_pipeline()