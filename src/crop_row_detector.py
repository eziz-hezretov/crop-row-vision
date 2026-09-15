from pathlib import Path #makes pathfinding easier

import cv2 #for image processing
import numpy as np #for numerical operations

image_path = Path("data/raw/image_01_easy.jpg") #path to the image we want to process

image = cv2.imread(str(image_path)) #reads the image from the specified path and stores it in the variable 'image'

if image is None:
    raise FileNotFoundError(f"Image not found at {image_path}") #to handle the case where the image is not found

print("Image shape:", image.shape) #prints the dimensions of the image (height, width, channels)

cv2.imwrite("results/original.jpg", image) #saves the original image to the specified path for reference

hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV) #converts from BGR color space to HSV color space

lower_green = np.array([25, 40, 40]) #the main disadvantage, telling the program what green is rather than letting it learn
upper_green = np.array([95, 255, 255])

vegetation_mask = cv2.inRange(
    hsv_image,
    lower_green,
    upper_green) #for every pixel in the HSV image, is its color between my lower and upper limits?

cv2.imwrite("results/vegetation_mask.jpg", vegetation_mask) #saves the vegetation mask to the specified path for reference

