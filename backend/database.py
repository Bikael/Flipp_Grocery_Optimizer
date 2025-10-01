import psycopg2
import pprint
from endpoint_dc import EndpointDC


def create_connection():
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",password="hellodb",port="5433")
    return conn


def drop_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
    DROP TABLE IF EXISTS grocery_lists;
    DROP TABLE IF EXISTS flyer_items;
    DROP TABLE IF EXISTS stores;              
    """)
    conn.commit()
    cursor.close()

def create_tables(conn):
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

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS grocery_lists (
        id SERIAL PRIMARY KEY,
        item_name TEXT NOT NULL
    )
    """)

    conn.commit()
    cursor.close()

def insert_store(conn, name):
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

def insert_flyer_item(conn, store_id, flyer_id, name, price, valid_from, valid_to, cutout_image):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO flyer_items (store_id, flyer_id, name, price, valid_from, valid_to, cutout_image)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """, (store_id, flyer_id, name, price, valid_from, valid_to, cutout_image))
    conn.commit()
    cursor.close()


def populate_tables():
    conn = create_connection()

    drop_tables(conn)
    create_tables(conn)

    dc = EndpointDC("K2T1J1") 
    flyer_ids = dc.get_flyer_ids("walmart")
    processed_flyer_data = []
    for id in flyer_ids:
        flyer_data = dc.get_flyer_data(id)
        processed_flyer_data += dc.process_json(flyer_data, id)

    store_id = insert_store(conn, "Walmart")
    for item in processed_flyer_data:
        insert_flyer_item(conn, store_id, item["flyer_id"], item["name"],item["price"], item["valid_from"], item["valid_to"], item["cutout_image_url"])
