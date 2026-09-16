# Crop Row Vision Baseline

A classical computer-vision project exploring crop-row perception using Python, OpenCV, and NumPy.

## Motivation

I built this project to learn how a simple classical computer-vision pipeline can extract vegetation

and estimate crop-row structure from agricultural field images.

This is an independent learning project.

## Pipeline

1. Load an agricultural field image
2. Convert BGR to HSV
3. Threshold likely green vegetation
4. Clean the vegetation mask using morphology
5. Detect boundaries using Canny edge detection
6. Detect line segments using the probabilistic Hough transform
7. Remove near-horizontal line candidates
8. Overlay remaining crop-row candidates on the source image

## Technologies

- Python
- OpenCV
- NumPy
- Git and GitHub

## Results

## Results

The pipeline was able to identify likely crop-row candidates in several test images, although the results varied depending on field conditions. Because the angle filter was intentionally strict, many line segments were rejected if they were too horizontal. This reduced false detections, but it also meant that some real crop-row structure was not captured.

Image 2 produced the strongest result. Its crop rows were sufficiently vertical and well defined for the Hough line detection and angle filtering stages to follow the visible row structure successfully.

A major limitation was that the vegetation mask only determines whether a pixel falls within the selected green HSV range. It does not understand whether that vegetation is a crop or a weed. Vegetation growing between rows could therefore create additional edges and sometimes produce line candidates that connected across the crop rows rather than following them.

A possible next step would be to investigate semantic segmentation, such as a U-Net-based approach, that could learn to distinguish crop plants from weeds rather than treating all green vegetation as the same class. A cleaner crop-only segmentation could provide better input for detecting the actual row structure.

## What Worked

The HSV vegetation threshold worked well at separating much of the green vegetation from the soil and background. Morphological opening and closing helped clean the resulting binary mask by removing small isolated regions and filling small gaps.

Canny edge detection then converted the cleaned vegetation regions into boundaries that could be analyzed by the probabilistic Hough transform. Filtering detected lines by their angle was particularly useful because it removed many nearly horizontal segments that were unlikely to represent crop-row direction.

The approach worked best when the crop rows were clearly visible, relatively straight, and oriented vertically or diagonally through the image. Image 2 was the clearest example of these stages working together successfully.

## Limitations

- Green weeds may be classified as crop vegetation.
- Strong lighting and shadows can affect colour segmentation.
- Curved crop rows cannot be represented well by single straight lines.
- Hough line detection can identify leaf edges or other structures.
- Parameters are manually selected rather than learned.

## What I Learned

This project helped me understand how a raw camera image can be transformed step by step into a much simpler representation that is useful for computer vision.

The pipeline begins with the original BGR image and converts it to HSV. HSV makes it easier to define a range of colours that represents likely green vegetation. `cv2.inRange()` then converts the image into a binary vegetation mask, where likely vegetation is white and other pixels are black.

I learned that the first segmentation does not have to be perfect. Morphological opening can remove small isolated areas of noise, while morphological closing can fill small gaps in vegetation regions. Canny edge detection can then reduce those regions to their boundaries, and `HoughLinesP()` can search those boundaries for straight line segments.

I also learned that detecting a line is not the same as understanding what that line represents. The Hough transform can find line-like structures, but it does not know whether they are actual crop rows. I therefore calculated each detected segment's angle and rejected lines that were too horizontal, leaving the remaining segments as crop-row candidates.

Most importantly, I learned the limitation of using colour alone for vegetation segmentation. The current pipeline can approximately distinguish green vegetation from the background, but it cannot distinguish crops from weeds because both can fall inside the same HSV range. For a future version, I would investigate a segmentation method that identifies different vegetation classes so that row detection can operate on crop plants specifically rather than all vegetation.

## Next Steps

- Quantitatively compare detections against labelled ground truth
- Investigate alternative vegetation segmentation methods
- Group multiple line segments into row-level estimates
- Investigate semantic segmentation
- Compare the classical baseline with a learned model such as U-Net

## Running Locally

Install dependencies:

```bash
pip install -r requirements.txt