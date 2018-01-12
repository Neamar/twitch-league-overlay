import requests
import json
import os
import re

PATCH = "8.1.1"
image_template = "http://ddragon.leagueoflegends.com/cdn/8.1.1/img/item/%s"
url = 'http://ddragon.leagueoflegends.com/cdn/8.1.1/data/en_US/item.json'
r = requests.get(url)


def get_items():
    items = []
    if r.status_code == 200:
        result = r.json()
        item_data = result['data']
        for item_id, item_data in item_data.items():
            image_url = image_template % item_data['image']['full']
            # # Download image
            # path = 'items/%s.png' % item_id
            # img = requests.get(image_url, stream=True)
            # if img.status_code == 200:
            #     with open(path, 'wb') as f:
            #         for chunk in img:
            #             f.write(chunk)

            stats = re.search('<stats>(.+)</stats>', item_data['description'])
            if(stats):
                stats = stats.group(1)
                stats = stats.split('<br>')
                stats = map(lambda s: '<li>%s</li>' % s, stats)
                stats = "\n".join(stats)

            description = re.sub('<stats>(.+)</stats>', '', item_data['description'])

            items.append({
                 "id": item_id,
                 "name": item_data['name'],
                 "stats": stats if stats else "",
                 "description": description,
                 "image_url": image_url,
                 "image_path": os.path.abspath('items/%s.png' % item_id)
            })

    return items

if __name__ == "__main__":
    items = get_items()
    print(items)
    with open('items.json', 'w') as f:
        f.write(json.dumps(items, indent=2))
