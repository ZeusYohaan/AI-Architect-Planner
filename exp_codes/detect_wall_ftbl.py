import cv2
import numpy as np
import os
import sys
import detect as detect


def main():
    example_image_path = "example.png"
    # Read floorplan image
    img = cv2.imread(example_image_path)
    image = img
    # grayscale image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resulting image
    height, width, channels = img.shape
    blank_image = np.zeros(
        (height, width, 3), np.uint8
    )  # output image same size as original

    # create wall image (filter out small objects from image)
    wall_img = detect.wall_filter(gray)
    wall_temp = wall_img
    """
    Detect Wall
    """
    # detect walls
    boxes, img = detect.precise_boxes(wall_img, blank_image)

    cv2.imshow("origin", image)
    cv2.imshow("res", img)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
