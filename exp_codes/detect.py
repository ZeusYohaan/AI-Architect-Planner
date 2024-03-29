import cv2
import numpy as np


# Generic filters
WALL_FILTER_TRESHOLD = [0, 255]
WALL_FILTER_KERNEL_SIZE = (3, 3)
WALL_FILTER_MORPHOLOGY_ITERATIONS = 2
WALL_FILTER_DILATE_ITERATIONS = 3
WALL_FILTER_DISTANCE = 5
WALL_FILTER_DISTANCE_THRESHOLD = [0.5, 0.2]
WALL_FILTER_MAX_VALUE = 255
WALL_FILTER_THRESHOLD_TECHNIQUE = 0

# Box detection
PRECISE_BOXES_ACCURACY = 0.001
REMOVE_PRECISE_BOXES_ACCURACY = 0.001
OUTER_CONTOURS_TRESHOLD = [230, 255]
PRECISE_HARRIS_KERNEL_SIZE = (1, 1)
PRECISE_HARRIS_BLOCK_SIZE = 2
PRECISE_HARRIS_KSIZE = 3
PRECISE_HARRIS_K = 0.04
PRECISE_ERODE_ITERATIONS = 10


def wall_filter(gray):
    """
    Filter walls
    Filter out walls from a grayscale image
    @Param image
    @Return image of walls
    """
    _, thresh = cv2.threshold(
        gray,
        WALL_FILTER_TRESHOLD[0],
        WALL_FILTER_TRESHOLD[1],
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
    )
    cv2.imshow("thresh", thresh)
    cv2.waitKey(0)

    # noise removal
    kernel = np.ones(WALL_FILTER_KERNEL_SIZE, np.uint8)
    opening = cv2.morphologyEx(
        thresh,
        cv2.MORPH_OPEN,
        kernel,
        iterations=WALL_FILTER_MORPHOLOGY_ITERATIONS,
    )

    sure_bg = cv2.dilate(
        opening, kernel, iterations=WALL_FILTER_DILATE_ITERATIONS
    )

    cv2.imshow("sure_bg", sure_bg)
    cv2.waitKey(0)

    dist_transform = cv2.distanceTransform(
        opening, cv2.DIST_L2, WALL_FILTER_DISTANCE
    )
    ret, sure_fg = cv2.threshold(
        WALL_FILTER_DISTANCE_THRESHOLD[0] * dist_transform,
        WALL_FILTER_DISTANCE_THRESHOLD[1] * dist_transform.max(),
        WALL_FILTER_MAX_VALUE,
        WALL_FILTER_THRESHOLD_TECHNIQUE,
    )

    cv2.imshow("sure_fg", sure_fg)
    cv2.waitKey(0)

    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    return unknown

def precise_boxes(detect_img, output_img=None, color=[100, 100, 0]):
    """
    Detect corners with boxes in image with high precision
    @Param detect_img image to detect from @mandatory
    @Param output_img image for output
    @Param color to set on output
    @Return corners(list of boxes), output image
    @source https://stackoverflow.com/questions/50930033/drawing-lines-and-distance-to-them-on-image-opencv-python
    """
    res = []

    contours, _ = cv2.findContours(
        detect_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for cnt in contours:
        epsilon = PRECISE_BOXES_ACCURACY * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        if output_img is not None:
            output_img = cv2.drawContours(output_img, [approx], 0, color)
        res.append(approx)

    return res, output_img