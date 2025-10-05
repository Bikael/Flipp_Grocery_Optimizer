import requests
import json
import pprint


class EndpointDC:
    
    def __init__(self, postal_code, grocery_list=[]):
        self.postal_code = postal_code
        self.grocery_list = grocery_list
    
    def process_json(self, json_data, model, flyer_id):
        filtered_items = []
        # Filter out neccessary fields, Subject to change depending on what fields are required
        for item in json_data:
            if item["price"] == '':
                continue
            else:
                
                filtered_item = {
                    "name" : item["name"],
                    "price" : item["price"],
                    "cutout_image_url" : item["cutout_image_url"],
                    "valid_from": item["valid_from"],
                    "valid_to": item["valid_to"],
                    "flyer_id": flyer_id,
                    "embedding" : model.encode(item['name']).tolist()
                }
                filtered_items.append(filtered_item)
        return filtered_items
    
    def get_flyer_ids(self, store):
        ids = []
        # get endpoint json data from url
        url = f"https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code={self.postal_code}&q={store}"
        response = requests.get(url)
        response.raise_for_status()

        # temporarily put json data into a file 
        webpage_data = response.json()
        flyers = webpage_data["flyers"]

        for flyer in flyers:
            ids.append(flyer["id"])
        return ids

    
    def get_flyer_data(self, flyer_id):
        flyer_data = []
        url = f"https://backflipp.wishabi.com/flipp/flyers/{flyer_id}?locale=en-ca"
        response = requests.get(url)
        response.raise_for_status()
        webpage_data = response.json()
        
        json.dumps(webpage_data, indent=4)
        flyer_data = webpage_data["items"]
        return flyer_data  