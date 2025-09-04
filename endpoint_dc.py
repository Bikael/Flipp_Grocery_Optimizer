import requests
import pprint, json
import spacy

class EndpointDC:
    
    def __init__(self, postal_code, grocery_list):
        self.postal_code = postal_code
        self.grocery_list = grocery_list
        

    def search_item(self, item):
        # get endpoint json data from url
        url = f"https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code={self.postal_code}&q={item}"
        response = requests.get(url)
        response.raise_for_status()

        # temporarily put json data into a file 
        webpage_data = response.json()
        return webpage_data
    
    def process_json(self, json_data):
        filtered_items = []
        items = json_data["items"]

        # Filter out neccessary fields 
        for item in items:
            filtered_item = {
                "name" : item["name"], 
                "current_price" : item["current_price"],
                "merchant_name" : item["merchant_name"],
                "clean_image_url" : item["clean_image_url"],
                "clipping_image_url" : item["clipping_image_url"]
            }
            filtered_items.append(filtered_item)

        return filtered_items

    def find_cheapest_item(self, items): 
        cheapest_items = [items[0]]
        # Find cheapest flyers for respective item
        for item in items:
            if item["current_price"] != None and item["current_price"] < cheapest_items[0]["current_price"]:
                cheapest_items = [item]
            elif cheapest_items[0]["current_price"] == item["current_price"]:
                cheapest_items.append(item)
        return cheapest_items
    

    def create_cheapest_list(self):
        final_list = []
        for item in self.grocery_list:
            data = self.search_item(item)
            items = self.process_json(data)
            cheapest_item = self.find_cheapest_item(items)
            final_list.append(cheapest_item)
        
        return final_list
  
    def store_filter(self, grocery_list, desired_stores):
        filtered_list = []
        for item in grocery_list:
            if item["merchant"] in desired_stores:
                filtered_list.append(item["merchant"])

        return filtered_list
    
    

    


            
        

    
    

        

