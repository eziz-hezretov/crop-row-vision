from pathlib import Path #makes pathfinding easier

import time #for timing how long the program takes to run
import cv2 #for image processing
import numpy as np #for numerical operations

def process_image(image_path):
    start_time = time.perf_counter() #record the start time

    image = cv2.imread(str(image_path)) #reads the image from the specified path and stores it in the variable 'image'

    if image is None:
        raise FileNotFoundError(
            f"Image not found at {image_path}"

        ) #to handle the case where the image is not found

    name = image_path.stem #gets the name of the image file without the extension

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
    #closing = expanding the white areas in the mask, which fills in small black holes
    #during closing, the small white dots that were removed during erosion do not come back, so the mask is cleaner

    cv2.imwrite("results/clean_mask.jpg", clean_mask) #saving the cleaned mask

    edges = cv2.Canny(clean_mask, 50, 150) #using Canny edge detection to find edges in our cleaned mask

    #so now the thresholds control which intensity changes count strongly enough as edges, we're creating outlines/boundaries

    #canny highlights boundaries in cleaned mask so next algorithm can search for line structures

    cv2.imwrite("results/edges.jpg", edges) #saving the edges image

    #note, we intentionally didn't run Hough on the original image, because an original photo contains too much information
    #information like color, texture, or other features that aren't relevant to the task
    #so, we simplified the photo to green vegetation, the cleaned it, then found the boundaries, and Hough now has a simpler image to inspect

    lines = cv2.HoughLinesP(

        edges,

        rho=1, #search line positions using approximately one-pixel resolution

        theta=np.pi / 180, #angle resolution of one degree, in radians

        threshold=40, #minimum number of votes (intersections in Hough space) the line needs to accumulate

        minLineLength=50, #minimum number of pixels making up a line

        maxLineGap=30 #maximum gap in pixels between connectable line segments

        #the idea is that it searches the edge image for groups of edge pixels that line up approximately straight
        #HoughLinesP is the probabilistic Hough line transform, giving actual enpoints
    )


    all_lines_image = image.copy() #copying the original image to draw all detected lines on it

    #we dont want to impact the original image so we'll use .copy()

    if lines is not None: #did Hough actually even find a line? Sometimes it doesn't and returns None
        for line in lines:
            x1, y1, x2, y2 = line #unpacking coords
            cv2.line(
                all_lines_image, #this is the image to modify
                (x1, y1), #starting point
                (x2, y2), #ending point
                (0, 0, 255), #BGR color
                2) #drawing the line on the image, in a red color with thickness 2 pixels

    cv2.imwrite(
        "results/all_detected_lines.jpg", #path to save the image with all detected lines
        all_lines_image
    )

    #right now the red lines are really bad, we should filter

    filtered_image = image.copy() #copying the original image to draw filtered lines on it

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line

            dx = x2 - x1 #change in x
            dy = y2 - y1 #change in y

            print("dx:", dx, "dy:", dy) #printing the change in x and y for debugging
            #note this doesn't filter anything but just calculates how each detected line moves

            angle = np.degrees(np.arctan2(dy, dx)) #calculating the angle of the line in degrees

            #this is because we want to remove near-horizontal lines, which are not crop rows, and we can do that by filtering based on the angle of the line

            if abs(angle) < 20 or abs(angle) > 160: #if the line is near-horizontal
                continue #skip this line

            cv2.line(
                filtered_image, #this is the image to modify
                (x1, y1), #starting point
                (x2, y2), #ending point
                (0, 0, 255), #BGR color
                3) #drawing the line on the image, in a red color with thickness 3 pixels

    output_path = Path("results") / f"{name}_detected.jpg" #creates a path for the output image in the results folder
            
    cv2.imwrite(
        str(output_path), #path to save the image with filtered lines
        filtered_image)

    elapsed = time.perf_counter() - start_time #calculate the elapsed time
    print(
        f"{image_path.name}: "
        f"{elapsed * 1000:.1f} ms") #print the elapsed time for processing the image

input_directory = Path("data/raw") #represents input folder

for image_path in input_directory.glob("*.jpg"): #find all files whose name ends in .jpg
    process_image(image_path) #loop through them one at a time, calling the function for each





