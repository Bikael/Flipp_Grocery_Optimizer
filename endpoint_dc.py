import requests
import json


class EndpointDC:
    
    def __init__(self, postal_code, grocery_list):
        self.postal_code = postal_code
        self.grocery_list = grocery_list
    
    def process_json(self, json_data):
        filtered_items = []

        # Filter out neccessary fields, Subject to change depending on what fields are required
        for item in json_data:
            filtered_item = {
                "name" : item["name"],
                "price" : item["price"],
                "cutout_image_url" : item["cutout_image_url"],
                "valid_from": item["valid_from"],
                "valid_to": item["valid_to"]
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

    
    def get_flyer_data(self, flyer_ids):
        flyer_data = []
        for id in flyer_ids:
            url = f"https://backflipp.wishabi.com/flipp/flyers/{id}?locale=en-ca"
            response = requests.get(url)
            response.raise_for_status()
            webpage_data = response.json()
            flyer_data += webpage_data["items"]
        
        json.dumps(flyer_data, indent=4)
        return flyer_data    