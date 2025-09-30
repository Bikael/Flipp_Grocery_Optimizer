import psycopg2


def create_connection():
    conn = psycopg2.connect(host="localhost", dbname="postgres", user="postgres",password="hellodb",port="5433")
    return conn


def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stores (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        postal_code TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flyer_items (
        id SERIAL PRIMARY KEY,
        store_id INTEGER NOT NULL REFERENCES stores (id),
        flyer_id TEXT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        expiry_date DATE
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

def insert_store(conn, name, postal_code=None):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO stores (name, postal_code)
        VALUES (%s, %s)
        RETURNING id;
    """, (name, postal_code))
    store_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    return store_id

def insert_flyer_item(conn, store_id, flyer_id, name, price, expiry_date=None):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO flyer_items (store_id, flyer_id, name, price, expiry_date)
        VALUES (%s, %s, %s, %s, %s);
    """, (store_id, flyer_id, name, price, expiry_date))
    conn.commit()
    cursor.close()

def find_best_deals(conn, grocery_item):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT stores.name, flyer_items.name, flyer_items.price
        FROM flyer_items
        JOIN stores ON flyer_items.store_id = stores.id
        WHERE flyer_items.name ILIKE %s
        ORDER BY flyer_items.price ASC
        LIMIT 5;
    """, (f"%{grocery_item}%",))
    results = cursor.fetchall()
    cursor.close()
    return results

conn = create_connection()
create_tables(conn)

store_id = insert_store(conn, "Walmart", "K1A0B1")
insert_flyer_item(conn, store_id, "flyer123", "2% Milk 4L", 3.99, "2025-10-10")

print(find_best_deals(conn, "Milk"))
