import requests
import pprint, json

class EndpointDC:
    
    def __init__(self, postal_code):
        self.postal_code = postal_code

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

        for item in items:
            filtered_item = {
                "name" : item["name"], 
                "current_price" : item["current_price"],
                "merchant_name" : item["merchant_name"],
                "clean_image_url" : item["clean_image_url"],
                "clipping_image_url" : item["clipping_image_url"]
            }
            filtered_items.append(filtered_item)

        with open("flipp_json.json", "w") as file:
            json.dump(filtered_items, file, indent=4)
            
        pprint.pprint(filtered_items)

        return filtered_items

    def find_cheapest_item(self, items): 
        
        cheapest_items = [items[0]]
        
        for item in items:
            print(cheapest_items[0]["current_price"])
            if item["current_price"] != None and item["current_price"] < cheapest_items[0]["current_price"]:
                cheapest_items = [item]
            elif cheapest_items[0]["current_price"] == item["current_price"]:
                cheapest_items.append(item)


        print(cheapest_items)
        return cheapest_items
    
    
        

            
        

    
    

        

