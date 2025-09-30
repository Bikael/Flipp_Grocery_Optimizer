# import pprint as pp
# import urllib.request, json 
# with urllib.request.urlopen("https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code=K2T1J1&q=eggs") as url:
    # data = json.load(url)

import list_handler as lh
import endpoint_dc as dc
import pprint
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()  # loads .env into environment
    postal_code = os.getenv("POSTAL_CODE")

    try:
        with open("grocery_list.txt", "r") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print("Error: The file 'grocery_list.txt' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")



    
