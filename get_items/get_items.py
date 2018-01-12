import requests

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
            # Download image
            path = 'items/%s.png' % item_id
            img = requests.get(image_url, stream=True)
            if img.status_code == 200:
                with open(path, 'wb') as f:
                    for chunk in img:
                        f.write(chunk)

            items.append({
                 "id": item_id,
                 "name": item_data['name'],
                 "description": 'TBD',  # item_data['description'],
                 "image_url": image_template % item_data['image']['full']
              })


    return items

if __name__ == "__main__":
    print(get_items())
