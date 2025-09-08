import requests
import pprint, json
import spacy

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
                "price" : item["price"]
            }
            filtered_items.append(filtered_item)

        return filtered_items
    
    def search_flyers(self, store):
        # get endpoint json data from url
        url = f"https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code={self.postal_code}&q={store}"
        response = requests.get(url)
        response.raise_for_status()

        # temporarily put json data into a file 
        webpage_data = response.json()
        flyers = webpage_data["flyers"]

        return flyers
    
    def get_flyer_ids(self, flyers):
        ids = []
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

    def get_flyer_items(self, stores:list):
        all_items = []
        for store in stores:
            flyers = self.search_flyers(store)
            flyer_ids = self.get_flyer_ids(flyers)
            flyer_data = self.get_flyer_data(flyer_ids)
            parsed_flyer_data = self.process_json(flyer_data)
            all_items += parsed_flyer_data

        return parsed_flyer_data