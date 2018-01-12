import cv2
import numpy as np
import json


def parse_screenshot(screenshot_path, items):
    img_rgb = cv2.imread(screenshot_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    for item in items:
        print("Looking for %s" % item['name'])

        template = cv2.imread(item['image_path'], 0)
        w, h = template.shape[::-1]

        res = cv2.matchTemplate(img_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.6
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    cv2.imwrite('res.png', img_rgb)

if __name__ == "__main__":
    screenshot_path = "stream1.png"
    with open('../get_items/items_simplified.json') as f:
        items = json.loads(f.read())

    parse_screenshot(screenshot_path, items)
