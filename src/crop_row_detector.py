from pathlib import Path

import cv2
import numpy as np

image_path = Path("data/raw/image_01_easy.jpg")

image = cv2.imread(str(image_path))

if image is None:
    raise FileNotFoundError(f"Image not found at {image_path}")

print("Image shape:", image.shape)

cv2.imwrite("results/original.jpg", image)

