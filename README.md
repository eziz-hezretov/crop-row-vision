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

The results from this 

## What Worked

Describe conditions where the simple pipeline performed reasonably well.

## Limitations

- Green weeds may be classified as crop vegetation.
- Strong lighting and shadows can affect colour segmentation.
- Curved crop rows cannot be represented well by single straight lines.
- Hough line detection can identify leaf edges or other structures.
- Parameters are manually selected rather than learned.

## What I Learned

Describe the concepts you personally understand after building the project.

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