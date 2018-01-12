import cv2
import numpy as np
import imutils
import json


def parse_screenshot(screenshot_path, items):
    img_rgb = cv2.imread(screenshot_path)
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    for item in items:
        print(" Looking for %s" % item['name'])

        # Dictionary of x,y, ratio, value
        points = []
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

            potential_points = list(zip(*loc[::-1]))
            if len(points) > 0:
                print("Got %s potential match(es) for %s" % (len(points), item['name']))
            for potential_point in potential_points:
                already_exists = False
                for point in points:
                    if abs(point['x'] - potential_point[0]) < point['ratio'] * w and abs(point['y'] - potential_point[1]) < point['ratio'] * h:
                        print("Existing match.")
                        # We already know about this match, potentially update value
                        point['value'] = max(point['value'], res[potential_point[0], potential_point[1]])
                    else:
                        print("New match")
                        points.append({
                            "x": potential_point[0],
                            "y": potential_point[1],
                            "ratio": r,
                            "value": res[potential_point[0]][potential_point[1]]
                        })

        for pt in potential_points:
            cv2.rectangle(img_rgb, pt, (pt[0] + int(w * r), pt[1] + int(h * r)), (0, 0, 255), 2)

    cv2.imwrite('res.png', img_rgb)

if __name__ == "__main__":
    screenshot_path = "stream1.png"
    with open('../get_items/items_simplified.json') as f:
        items = json.loads(f.read())

    parse_screenshot(screenshot_path, items)