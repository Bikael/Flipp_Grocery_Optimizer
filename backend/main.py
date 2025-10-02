import list_handler as lh
import endpoint_dc as dc
import pprint
import os
import database as db
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()  # loads .env into environment
    postal_code = os.getenv("POSTAL_CODE")
    host = os.getenv("HOST")
    dbname = os.getenv("DBNAME")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    port = os.getenv("PORT")


    database = db.Database(postal_code,host,dbname,user,password,port)
    database.display_flyer_items('Walmart')
    





    
