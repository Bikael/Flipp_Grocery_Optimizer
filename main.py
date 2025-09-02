# import pprint as pp
# import urllib.request, json 
# with urllib.request.urlopen("https://backflipp.wishabi.com/flipp/items/search?locale=en-ca&postal_code=K2T1J1&q=eggs") as url:
    # data = json.load(url)

import list_handler as lh

if __name__ == "__main__":

    try:
        with open("grocery_list.txt", "r") as file:
            content = file.read()
            print(content)
    except FileNotFoundError:
        print("Error: The file 'my_text_file.txt' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    parsed_gl = lh.parse_grocery_list(content)
    print(parsed_gl)
    

    
