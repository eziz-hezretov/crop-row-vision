## Output Analysis

The pipeline was tested on several agricultural field images containing plants arranged in rows.

The test images included different conditions such as shadows, weeds that should ideally be ignored, varying row visibility, curved rows, and different crop sizes.

For every input image, the program saves six processing outputs:

1. Original image - the unprocessed agricultural field image.

2. Vegetation mask - white pixels represent areas classified as vegetation, while black pixels represent everything else, such as soil.

3. Cleaned vegetation mask - morphological opening and closing, which use erosion and dilation, remove small areas of white noise and help fill small gaps or holes in the vegetation mask.

4. Edge detection - identifies the boundaries of the segmented vegetation so that line-like structures can be detected in the next stage.

5. Crop-row candidate detection - the Hough line transform detects straight line segments that may correspond to crop-row structure. The detected lines can then be filtered to remove unlikely row candidates.

## Image 1 - Clear Crop Rows

Input: `image_01_easy.jpg`

### Original Image

![Original image](results/image_01_easy_original.jpg)

### Vegetation Mask

![Vegetation mask](results/image_01_easy_vegetation_mask.jpg)

### Cleaned Vegetation Mask

![Cleaned vegetation mask](results/image_01_easy_clean_mask.jpg)

### Edge Detection

![Edge detection](results/image_01_easy_edges.jpg)

### Raw Hough Lines

![Raw Hough lines](results/image_01_easy_all_detected_lines.jpg)

### Final Crop-Row Candidates

![Final crop-row candidates](results/image_01_easy_detected.jpg)

Result: Moderate

Observation: The image contains clearly visible crop rows, but with the current filtering and grouping parameters, only one prominent row was retained as a final crop-row candidate.

---

## Image 2 - Strong Shadows

Input: `image_02_shadow.jpg`

### Original Image

![Original image](results/image_02_shadow_original.jpg)

### Vegetation Mask

![Vegetation mask](results/image_02_shadow_vegetation_mask.jpg)

### Cleaned Vegetation Mask

![Cleaned vegetation mask](results/image_02_shadow_clean_mask.jpg)

### Edge Detection

![Edge detection](results/image_02_shadow_edges.jpg)

### Raw Hough Lines

![Raw Hough lines](results/image_02_shadow_all_detected_lines.jpg)

### Final Crop-Row Candidates

![Final crop-row candidates](results/image_02_shadow_detected.jpg)

Result: Good

Observation: This was the strongest-performing example. Despite the presence of shadows, the pipeline successfully retained three visible crop-row candidates.

---

## Image 3 - Sparse Weeds

Input: `image_03_sparse_weeds.jpg`

### Original Image

![Original image](results/image_03_sparse_weeds_original.jpg)

### Vegetation Mask

![Vegetation mask](results/image_03_sparse_weeds_vegetation_mask.jpg)

### Cleaned Vegetation Mask

![Cleaned vegetation mask](results/image_03_sparse_weeds_clean_mask.jpg)

### Edge Detection

![Edge detection](results/image_03_sparse_weeds_edges.jpg)

### Raw Hough Lines

![Raw Hough lines](results/image_03_sparse_weeds_all_detected_lines.jpg)

### Final Crop-Row Candidates

![Final crop-row candidates](results/image_03_sparse_weeds_detected.jpg)

Result: Poor

Observation: Sparse weeds and irregular vegetation patterns produced line segments that did not consistently match the true crop rows. Some incorrect intersecting crop-row candidates remained after filtering and grouping.

---

## Image 4 - Dense Weeds

Input: `image_04_dense_weeds.jpg`

### Original Image

![Original image](results/image_04_dense_weeds_original.jpg)

### Vegetation Mask

![Vegetation mask](results/image_04_dense_weeds_vegetation_mask.jpg)

### Cleaned Vegetation Mask

![Cleaned vegetation mask](results/image_04_dense_weeds_clean_mask.jpg)

### Edge Detection

![Edge detection](results/image_04_dense_weeds_edges.jpg)

### Raw Hough Lines

![Raw Hough lines](results/image_04_dense_weeds_all_detected_lines.jpg)

### Final Crop-Row Candidates

![Final crop-row candidates](results/image_04_dense_weeds_detected.jpg)

Result: Poor

Observation: Dense weeds were difficult for the pipeline because the HSV vegetation mask classifies both crops and weeds as green vegetation. This produced irregular boundaries and line structures that made reliable crop-row estimation difficult.

---

## Image 5 - Curved Rows

Input: `image_05_curve.jpg`

### Original Image

![Original image](results/image_05_curve_original.jpg)

### Vegetation Mask

![Vegetation mask](results/image_05_curve_vegetation_mask.jpg)

### Cleaned Vegetation Mask

![Cleaned vegetation mask](results/image_05_curve_clean_mask.jpg)

### Edge Detection

![Edge detection](results/image_05_curve_edges.jpg)

### Raw Hough Lines

![Raw Hough lines](results/image_05_curve_all_detected_lines.jpg)

### Final Crop-Row Candidates

![Final crop-row candidates](results/image_05_curve_detected.jpg)

Result: Moderate

Observation: The pipeline identified three crop-row candidates correctly, but also retained one incorrect intersecting line. Because the current method ultimately represents each row using a straight fitted line, curved crop rows are more difficult to model accurately.

---

## Image 6 - Larger Crops

Input: `image_06_large_crop.jpg`

### Original Image

![Original image](results/image_06_large_crop_original.jpg)

### Vegetation Mask

![Vegetation mask](results/image_06_large_crop_vegetation_mask.jpg)

### Cleaned Vegetation Mask

![Cleaned vegetation mask](results/image_06_large_crop_clean_mask.jpg)

### Edge Detection

![Edge detection](results/image_06_large_crop_edges.jpg)

### Raw Hough Lines

![Raw Hough lines](results/image_06_large_crop_all_detected_lines.jpg)

### Final Crop-Row Candidates

![Final crop-row candidates](results/image_06_large_crop_detected.jpg)

Result: Moderate

Observation: The general crop-row structure was identified, but larger and overlapping vegetation created additional boundaries and Hough line detections, making row estimation less precise.

### Results Summary

| Image                               | Condition       | Result   | Main Issue                                                                                              |
|-------------------------------------|-----------------|----------|---------------------------------------------------------------------------------------------------------|
| `image_01_easy_detected.jpg`        | Clear crop rows | Moderate | With the current filtering parameters, only one prominent row was detected                              |
| `image_02_shadow_detected.jpg`      | Strong shadows  | Good     | Best-performing example; the program successfully detected three visible rows                           |
| `image_03_sparse_weeds_detected.jpg`| Sparse weeds    | Poor     | Irregular vegetation patterns caused intersecting line candidates                                       |
| `image_04_dense_weeds_detected.jpg` | Dense weeds     | Poor     | Dense weeds made it difficult to distinguish crop-row structure, producing intersecting line candidates |
| `image_05_curve_detected.jpg`       | Curved rows     | Moderate | Three row segments were detected correctly, but one incorrect intersecting line was also detected       |
| `image_06_large_crop_detected.jpg`  | Larger plants   | Moderate | Row structure was identified, but overlapping vegetation created additional line detections             |

### Key Observations

- HSV thresholding works reasonably well when green vegetation is clearly separated from the soil.
- Morphological filtering helps remove isolated noise and fill small gaps in the vegetation mask.
- Dense weeds are difficult because the current method cannot distinguish crop plants from other green vegetation.
- Straight-line detection works better on clearly visible, relatively straight rows than on curved or irregular rows.
- Lighting and shadows can affect segmentation quality.
- One of the largest limitations is sensitivity to irregular crop alignment. When vegetation does not form clear parallel rows, the Hough transform may detect diagonal or intersecting line candidates.

### Limitations

This project uses a classical computer-vision baseline rather than a trained machine-learning model. The vegetation thresholds and line-detection parameters are manually selected, so performance varies across lighting conditions, vegetation density, crop alignment, and field structure.

The current method also detects geometric line patterns rather than understanding whether a particular plant belongs to a crop or a weed. This makes dense weeds and irregular vegetation especially challenging.

A future improvement would be to compare this classical computer-vision baseline with a semantic segmentation approach such as U-Net.