import requests
import pprint, json

class EndpointDC:
    postal_code = ""

    def search_item(self, item):
        # get endpoint json data from url
        url = f"https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code={self.postal_code}&q={item}"
        response = requests.get(url)
        response.raise_for_status()

        # temporarily put json data into a file 
        data = response.json()
        with open("flipp_json.json", "w") as file:
            json.dump(data, file, indent=4)

# pprint.pprint()