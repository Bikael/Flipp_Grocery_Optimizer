import list_handler as lh
import endpoint_dc as dc
import pprint
import os
import database as db
import deal_selector as ds
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer, util

if __name__ == "__main__":
    load_dotenv()  # loads .env into environment
    postal_code = os.getenv("POSTAL_CODE")
    host = os.getenv("HOST")
    dbname = os.getenv("DBNAME")
    user = os.getenv("USER")
    password = os.getenv("PASSWORD")
    port = os.getenv("PORT")

    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    stores = ["loblaws","shoppers"]
    database = db.Database(postal_code,host,dbname,user,password,port)
    database.drop_tables(database.create_connection())
    database.create_tables(database.create_connection())
    for store in stores:  
        database.populate_tables(model, store)

    # database.get_embeddings(database.create_connection(),stores)

    deal_selector = ds.DealSelector()
    best_results = deal_selector.semantic_search(database.create_connection(),database, model, "milk", stores)

    # pprint.pprint(best_results)


    





    
