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

        threshold=35, #minimum number of votes (intersections in Hough space) the line needs to accumulate

        minLineLength=40, #minimum number of pixels making up a line

        maxLineGap=35 #maximum gap in pixels between connectable line segments

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

    image_height = image.shape[0] #getting the height of the image
    image_width = image.shape[1] #getting the width of the image

    candidate_lines = [] #list to hold lines that pass the filtering criteria

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line

            dx = x2 - x1 #change in x
            dy = y2 - y1 #change in y

            print("dx:", dx, "dy:", dy) #printing the change in x and y for debugging
            #note this doesn't filter anything but just calculates how each detected line moves

            angle = np.degrees(np.arctan2(dy, dx)) #calculating the angle of the line in degrees

            #this is because we want to remove near-horizontal lines, which are not crop rows, and we can do that by filtering based on the angle of the line

            if angle > 90:
                angle -= 180 #this is to make the angle range from -90 to 90 degrees, instead of 0 to 180 degrees
            elif angle <= -90:
                angle += 180 #same as above, but for negative angles

            if abs(angle) < 25:
                continue #if the angle is less than 20 degrees, we skip this line because it's too horizontal

            top_y = min(y1, y2) #the top y coordinate of the line
            bottom_y = max(y1, y2) #the bottom y coordinate of the line

            vertical_span = bottom_y - top_y #the vertical span of the line

            if bottom_y < image_height * 0.45:
                continue #if the bottom of the line is above 55% of the image height, we skip this line because it's too high up

            if vertical_span < image_height * 0.08:
                continue #if the vertical span of the line is less than 12% of the image height, we skip this line because it's too short

            candidate_lines.append(
                (x1, y1, x2, y2, angle)
            ) #adding the line to the list of candidate lines that passed the filtering criteria


            cv2.line(
                filtered_image, #this is the image to modify
                (x1, y1), #starting point
                (x2, y2), #ending point
                (0, 0, 255), #BGR color
                3) #drawing the line on the image, in a red color with thickness 3 pixels


    groups = []

    for x1, y1, x2, y2, angle in candidate_lines:

        # Avoid division by zero for perfectly horizontal lines.
        if y2 == y1:
            continue

        # Estimate where this line would reach the bottom of the image.
        x_at_bottom = x1 + (
            (image_height - 1 - y1)
            * (x2 - x1)
            / (y2 - y1)
        )

        matching_group = None

        # Look through existing groups to see whether this line
        # is similar to one of them.
        for group in groups:

            close_position = abs(
                x_at_bottom - group["bottom_x"]
            ) < 50

            close_angle = abs(
                angle - group["angle"]
            ) < 12

            if close_position and close_angle:
                matching_group = group
                break

        # If no similar group exists, create a new group.
        if matching_group is None:
            groups.append({
                "bottom_x": x_at_bottom,
                "angle": angle,
                "lines": [(x1, y1, x2, y2)]
            })

        # Otherwise add this line to the existing group.
        else:
            matching_group["lines"].append(
                (x1, y1, x2, y2)
            )

            group_size = len(matching_group["lines"])

            matching_group["bottom_x"] = (
                matching_group["bottom_x"] * (group_size - 1)
                + x_at_bottom
            ) / group_size

            matching_group["angle"] = (
                matching_group["angle"] * (group_size - 1)
                + angle
            ) / group_size


    # Create a fresh image for the final grouped row estimates.
    grouped_image = image.copy()

    for group in groups:

        # Require at least two line segments before treating
        # the group as a possible crop row.
        if len(group["lines"]) < 3:
            continue

        points = []

        # Collect both endpoints from every line in this group.
        for x1, y1, x2, y2 in group["lines"]:
            points.append([x1, y1])
            points.append([x2, y2])

        points = np.array(
            points,
            dtype=np.float32
        )

        # Find one straight line that best fits all these points.
        vx, vy, x0, y0 = cv2.fitLine(
            points,
            cv2.DIST_L2,
            0,
            0.01,
            0.01
        ).flatten()

        # Avoid dividing by a value extremely close to zero.
        if abs(vy) < 0.001:
            continue

        # Decide how far vertically to draw the final row line.
        y_bottom = image_height - 1
        y_top = int(image_height * 0.25)

        # Calculate where the fitted line is at those y positions.
        x_bottom = int(
            x0 + (y_bottom - y0) * vx / vy
        )

        x_top = int(
            x0 + (y_top - y0) * vx / vy
        )

        # Approximate horizontal centre of the image.
        image_center_x = image_width / 2

        # Crop rows should generally converge inward as they move upward.
        if x_bottom < image_center_x:
            # A row on the left should move toward the right as it goes upward.
            if x_top <= x_bottom:
                continue

        elif x_bottom > image_center_x:
            # A row on the right should move toward the left as it goes upward.
            if x_top >= x_bottom:
                continue

        if abs(x_top - image_center_x) >= abs(x_bottom - image_center_x):
            continue

        # Keep the line inside the image boundaries.
        visible, point1, point2 = cv2.clipLine(
            (0, 0, image_width, image_height),
            (x_top, y_top),
            (x_bottom, y_bottom)
        )

        if visible:
            cv2.line(
                grouped_image,
                point1,
                point2,
                (0, 255, 0),
                4
            )

    filtered_image = grouped_image

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