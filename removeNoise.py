import cv2
import matplotlib.pyplot as plt
import json
import numpy as np


class RemoveNoise:
    def __init__(self, config):
        self.image_paths = config["image_paths"]
        self.thresholds = config["thresholds"]

    def remove_main_noise(self, image_path, threshold):
        img = cv2.imread(image_path)
        img_bw = 255 * (cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) > threshold).astype("uint8")
        se1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        se2 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        mask = cv2.morphologyEx(img_bw, cv2.MORPH_CLOSE, se1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, se2)
        mask = np.dstack([mask, mask, mask]) / 255
        out = img * mask
        img_bw_inverted = 255 - img_bw
        contours, _ = cv2.findContours(img_bw_inverted, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cv2.imshow( 'image', out)
        return out, contours

    def get_undesired_objects(self, contours):
        ls = []
        for idx, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            if w > h:
                if w / h < 1:
                    ls.append(idx)
            if w < h:
                if h / w < 1:
                    ls.append(idx)
            if area <= 45:
                ls.append(idx)
            if radius < 10:
                ls.append(idx)
        return list(set(ls))

    def remove_fine_noise(self, data_tuple):
        out = data_tuple[0]
        contours = data_tuple[1]

        contour_details = []
        contour_ids_to_remove = list(set([] + self.get_undesired_objects(contours)))
        print("contour_id", contour_ids_to_remove)

        for idx, contour in enumerate(contours):
            x, y, w, h = cv2.boundingRect(contour)
            area = cv2.contourArea(contour)
            (x, y), radius = cv2.minEnclosingCircle(contour)
            contour_details.append(
                {'id': idx, 'x': x, 'y': y, 'width': w, 'height': h, 'area': area, 'radius': radius, })
            if idx in contour_ids_to_remove:
                cv2.drawContours(out, [contour], -1, (255, 255, 255), thickness=cv2.FILLED)
            else:
                cv2.drawContours(out, [contour], -1, (0, 255, 0), 2)
                # Label the contour ID at the centroid
                centroid_x = x + w // 2
                centroid_y = y + h // 2
                plt.text(centroid_x, centroid_y, str(idx), color='red', fontsize=8, ha='center', va='center')
        for details in contour_details:
            print("Contour {}: x={}, y={}, width={}, height={}, area={}, radius={}".format(
                details['id'], details['x'], details['y'], details['width'], details['height'], details['area'],
                details['radius']))
        plt.imshow(out)
        plt.title("Image with Contours on Black Parts".format(contour_ids_to_remove))
        plt.show()
        plt.close()

    def automate_all_plans(self):
        for image_path, threshold in zip(self.image_paths.values(), self.thresholds.values()):
            self.remove_fine_noise(self.remove_main_noise(image_path, threshold))


if __name__ == "__main__":
    with open('config.json', 'r') as f:
        config = json.load(f)
        obj = RemoveNoise(config)
        obj.automate_all_plans()
