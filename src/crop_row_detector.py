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

#at this point in time, the mask contains lots of small white dots and black holes, so we will clean it

kernel = np.ones((5, 5), np.uint8) #creates a 5x5 matrix of ones to be used as a kernel for morphological operations

#during morphological operations, the kernal is moved across the image, and it defines the neighbourhood size used. 

#morphological opening

opened_mask = cv2.morphologyEx(
    vegetation_mask,
    cv2.MORPH_OPEN,
    kernel
)

clean_mask = cv2.morphologyEx(
    opened_mask,
    cv2.MORPH_CLOSE,
    kernel
)

#these two morphological operations work as so:
#opening = erosion + dilation
#erosian = shrinking the white areas in the mask, which removes small white dots
#dilation = expanding the white areas in the mask, which fills in small black holes
#during dilation, the small white dots that were removed during erosion do not come back, so the mask is cleaner

cv2.imwrite("results/clean_mask.jpg", clean_mask) #saves the cleaned mask to the specified path for reference




