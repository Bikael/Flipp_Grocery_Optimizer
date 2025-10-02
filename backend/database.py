import psycopg2
import pprint
from endpoint_dc import EndpointDC

class Database:
    def __init__(self, postal_code, host, dbname, user, password, port):
        self.postal_code = postal_code
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password 
        self.port = port


    def create_connection(self):
        conn = psycopg2.connect(host=self.host, dbname=self.dbname, user=self.user ,password=self.password,port=self.port)
        return conn


    def drop_tables(self, conn):
        cursor = conn.cursor()
        cursor.execute("""
        DROP TABLE IF EXISTS grocery_lists;
        DROP TABLE IF EXISTS flyer_items;
        DROP TABLE IF EXISTS stores;              
        """)
        conn.commit()
        cursor.close()

    def create_tables(self, conn):
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS flyer_items (
            id SERIAL PRIMARY KEY,
            store_id INTEGER NOT NULL REFERENCES stores (id),
            flyer_id TEXT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            valid_from DATE,
            valid_to DATE,
            cutout_image TEXT
        )
        """)

        conn.commit()
        cursor.close()

    def insert_store(self, conn, name):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO stores (name)
            VALUES (%s)
            RETURNING id;
        """, (name,))
        store_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        return store_id

    def insert_flyer_item(self, conn, store_id, flyer_id, name, price, valid_from, valid_to, cutout_image):
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO flyer_items (store_id, flyer_id, name, price, valid_from, valid_to, cutout_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (store_id, flyer_id, name, price, valid_from, valid_to, cutout_image))
        conn.commit()
        cursor.close()

    def display_flyer_items(self, store):
        conn = self.create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * 
            FROM flyer_items
            WHERE store_id = (SELECT id FROM stores WHERE name = %s)
        """, (store,))
        
        rows = cursor.fetchall()
        
        for row in rows:
            pprint.pprint(row)
        
        cursor.close()


    # populate the flyer_items and stores tables with all the information from a single store
    def populate_tables(self, store):
        
        conn = self.create_connection()
        dc = EndpointDC(self.postal_code) 
        flyer_ids = dc.get_flyer_ids(store)
        processed_flyer_data = []
        for id in flyer_ids:
            flyer_data = dc.get_flyer_data(id)
            processed_flyer_data += dc.process_json(flyer_data, id)

        store_id = self.insert_store(conn, store)
        for item in processed_flyer_data:
            self.insert_flyer_item(conn, store_id, item["flyer_id"], item["name"],item["price"], item["valid_from"], item["valid_to"], item["cutout_image_url"])


