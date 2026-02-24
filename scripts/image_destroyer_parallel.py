#Image destroyer parallel -multi-threaded script to generate degraded images for model training
from concurrent.futures import ThreadPoolExecutor
import os
from PIL import Image
import random

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

if os.path.basename(CURRENT_DIR) == "scripts":
    ROOT_DIR = os.path.dirname(CURRENT_DIR)
else:
    ROOT_DIR = CURRENT_DIR

INPUT_FOLDER = os.path.join(ROOT_DIR, "data", "raw")
OUTPUT_FOLDER = os.path.join(ROOT_DIR, "data", "processed")

# Setup output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
[os.remove(os.path.join(OUTPUT_FOLDER, f)) for f in os.listdir(OUTPUT_FOLDER)]

def process(file):
    """
    Downsample and upscale using Nearest Neighbor to simulate pixelation artifacts
    """
    if file.lower().endswith((".jpg", ".jpeg", ".png")):
        path = os.path.join(INPUT_FOLDER, file)
        img = Image.open(path)
        scale = random.uniform(0.3, 0.7)
        width, height = img.size
        small = img.resize((int(width*scale), int(height*scale)), Image.NEAREST)
        decompressed = small.resize((width, height), Image.NEAREST)
        output_path = os.path.join(OUTPUT_FOLDER, file)
        decompressed.save(output_path, "PNG", quality=random.randint(30,70))
        return output_path

# Eecute processing in parallel using multiple CPU threads
files = os.listdir(INPUT_FOLDER)
with ThreadPoolExecutor(max_workers=12) as executor:  
    results = list(executor.map(process, files))

print("Saved:", len(results), "files")

