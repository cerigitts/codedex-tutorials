# gif_creator.py
# Create a GIF from a sequence of frames with precise frame timing

from pathlib import Path
from PIL import Image

def create_gif_from_frames(folder_path: Path, base_name: str, frame_files, target_fps: float, delete_frames=True):
    frame_duration = round(1000 / target_fps)

    frames = []
    for f in frame_files:
        if f.exists():
            frames.append(Image.open(f).convert("P", palette=Image.ADAPTIVE, colors=128))

    if not frames:
        print("No frames found to create GIF.")
        return None

    output_path = folder_path / f"{base_name}_{int(target_fps)}fps.gif"
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=frame_duration,
        optimize=True
    )
    print(f"\n✅ GIF created: {output_path}")

    if delete_frames:
        for f in frame_files:
            f.unlink()
        print("🧹 Cleaned up extracted frames.")

    return output_path