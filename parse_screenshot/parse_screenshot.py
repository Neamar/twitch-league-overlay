import cv2
import numpy as np
import imutils
import json


def find_item_in_screenshot(screenshot_cv2_data, item):
    """
    Find all occurrences of item in screenshot_cv2_data,
    Returns an array of dictionary(x, y, w, h, value)
    """
    points = []
    template = cv2.imread(item['image_path'])
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    w, h = template.shape[::-1]

    for scale in np.linspace(0.4, 0.8, 10)[::-1]:
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing
        new_width = int(template.shape[1] * scale)
        resized = imutils.resize(template, width=new_width)
        r = float(resized.shape[1]) / float(template.shape[1])

        res = cv2.matchTemplate(screenshot_cv2_data, resized, cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where(res >= threshold)

        potential_points = zip(*loc[::-1])
        for potential_point in potential_points:
            already_exists = False
            for point in points:
                if abs(point['x'] - potential_point[0]) < point['w'] and abs(point['y'] - potential_point[1]) < point['h']:
                    # We already know about this match, potentially update value
                    point['value'] = max(point['value'], res[potential_point[1], potential_point[0]])
                    already_exists = True
                    break
            if not already_exists:
                value = res[potential_point[1]][potential_point[0]]
                points.append({
                    "x": potential_point[0],
                    "y": potential_point[1],
                    "w": w * r,
                    "h": h * r,
                    "value": value,
                })
    for point in points:
        print("Found %s at (%s, %s, %s, %s), value %s" % (item['name'], point['x'], point['y'], point['w'], point['h'], point['value']))
    return points


def parse_screenshot(screenshot_path, items):
    img_rgb = cv2.imread(screenshot_path)
    original = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

    items_position = []
    for item in items:
        print(" Looking for %s" % item['name'])

        # Dictionary of x, y, w, h, value
        points = find_item_in_screenshot(original, item)
        items_position.append(points)

        for pt in points:
            cv2.rectangle(img_rgb, (pt['x'], pt['y']), (pt['x'] + int(pt['w']), pt['y'] + int(pt['h'])), (0, 0, 255), 2)

    cv2.imwrite('res.png', img_rgb)

if __name__ == "__main__":
    screenshot_path = "stream1.png"
    with open('../get_items/items_simplified.json') as f:
        items = json.loads(f.read())

    parse_screenshot(screenshot_path, items)
