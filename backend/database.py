import psycopg2
import pprint
from endpoint_dc import EndpointDC
import numpy as np

class Database:
    def __init__(self, postal_code, host, dbname, user, password, port):
        self.postal_code = postal_code
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.port = port

    def create_connection(self):
        """Create and return a new database connection."""
        return psycopg2.connect(
            host=self.host,
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            port=self.port
        )

    def drop_tables(self, conn):
        """Drop all relevant tables from the database."""
        with conn.cursor() as cursor:
            cursor.execute("""
                DROP TABLE IF EXISTS flyer_items;
                DROP TABLE IF EXISTS stores;
            """)
            conn.commit()

    def create_tables(self, conn):
        """Create the stores and flyer_items tables."""
        with conn.cursor() as cursor:
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
                    cutout_image TEXT,
                    embedding VECTOR(384)
                )
            """)
            conn.commit()

    def insert_store(self, conn, name):
        """Insert a store and return its ID."""
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO stores (name)
                VALUES (%s)
                RETURNING id;
            """, (name,))
            store_id = cursor.fetchone()[0]
            conn.commit()
        return store_id

    def insert_flyer_item(self, conn, store_id, flyer_id, name, price, valid_from, valid_to, cutout_image, embedding):
        """Insert a flyer item into the database."""
        # Ensure embedding is a list (for JSON/pgvector)
        if hasattr(embedding, 'tolist'):
            embedding = embedding.tolist()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO flyer_items (store_id, flyer_id, name, price, valid_from, valid_to, cutout_image, embedding)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (store_id, flyer_id, name, price, valid_from, valid_to, cutout_image, embedding))
            conn.commit()

    def display_flyer_items(self, store):
        """Print all flyer items for a given store."""
        conn = self.create_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT * FROM flyer_items
                WHERE store_id = (SELECT id FROM stores WHERE name = %s)
            """, (store,))
            rows = cursor.fetchall()
            for row in rows:
                pprint.pprint(row)
        conn.close()

    def populate_tables(self, model, store):
        """
        Populate the flyer_items and stores tables with all the information from a single store.
        """
        conn = self.create_connection()
        dc = EndpointDC(self.postal_code)
        flyer_ids = dc.get_flyer_ids(store)
        processed_flyer_data = []
        print(f"store: {store}")
        for count, flyer_id in enumerate(flyer_ids, start=1):
            flyer_data = dc.get_flyer_data(flyer_id)
            print(f"    processing json data {count}/{len(flyer_ids)}...")
            processed_flyer_data += dc.process_json(flyer_data, model, flyer_id)

        store_id = self.insert_store(conn, store)
        for item in processed_flyer_data:
            self.insert_flyer_item(
                conn,
                store_id,
                item["flyer_id"],
                item["name"],
                item["price"],
                item["valid_from"],
                item["valid_to"],
                item["cutout_image_url"],
                item["embedding"]
            )
        conn.close()

    def get_embeddings(self, conn, stores):
        """
        Retrieve embeddings for all flyer items in the given stores.
        Returns a list of dicts with id, name, and embedding (as np.array).
        """
        data = []
        embeddings = []
        with conn.cursor() as cursor:
            for store in stores:
                cursor.execute("""
                    SELECT id, name, embedding FROM flyer_items
                    WHERE store_id = (SELECT id FROM stores WHERE name = %s)
                """, (store,))
                print(f"getting all items from {store}")
                data += cursor.fetchall()

        for item_id, name, embedding in data:
            if isinstance(embedding, list):
                vector = np.array(embedding, dtype=np.float32)
            else:
                vector = np.fromstring(str(embedding).strip('[]'), sep=',', dtype=np.float32)
            embeddings.append({
                "id": item_id,
                "name": name,
                "embedding": vector
            })
        return embeddings