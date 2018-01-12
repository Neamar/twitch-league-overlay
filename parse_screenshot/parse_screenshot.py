import cv2
import numpy as np
import imutils
import json


def parse_screenshot(screenshot_path, items):
    img_rgb = cv2.imread(screenshot_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    for item in items:
        print("Looking for %s" % item['name'])

        template = cv2.imread(item['image_path'], 0)
        w, h = template.shape[::-1]

        for scale in np.linspace(0.2, 1.0, 20)[::-1]:
            # resize the image according to the scale, and keep track
            # of the ratio of the resizing
            new_width = int(template.shape[1] * scale)
            resized = imutils.resize(template, width=new_width)
            r = float(resized.shape[1]) / float(template.shape[1])

            res = cv2.matchTemplate(img_gray, resized, cv2.TM_CCOEFF_NORMED)
            threshold = 0.7
            loc = np.where(res >= threshold)

            points = list(zip(*loc[::-1]))
            if len(points) > 0:
                print("Got %s match(es) for %s" % (len(points), item['name']))
            for pt in points:
                cv2.rectangle(img_rgb, pt, (pt[0] + int(w * r), pt[1] + int(h * r)), (0, 0, 255), 2)

    cv2.imwrite('res.png', img_rgb)

if __name__ == "__main__":
    screenshot_path = "stream1.png"
    with open('../get_items/items_simplified.json') as f:
        items = json.loads(f.read())

    parse_screenshot(screenshot_path, items)
