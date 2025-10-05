import torch
from sentence_transformers import SentenceTransformer, util

class DealSelector:
    def __init__(self):
        pass

    def find_best_matches(self, conn, item_name):
        cursor = conn.cursor()
        cursor.execute("""
            SELECT name, price, store_id, similarity(name, %s) AS score
            FROM flyer_items
            WHERE name ILIKE %s
            ORDER BY score DESC
        """, (item_name, f"%{item_name}%"))

        results = cursor.fetchall()
        conn.commit()
        cursor.close()
        

        # Transform into a nice list of dicts
        matches = [
            {"name": row[0], "price": row[1], "store_id": row[2], "score": row[3]}
            for row in results
        ]
        return matches
    
    def semantic_search(self, conn, database, model, query, stores):
        items = database.get_embeddings(conn, stores)
        query_embedding = model.encode(query, convert_to_tensor=True).cpu()  # Ensure on CPU
        item_embeddings = [item["embedding"] for item in items]
        item_embeddings_tensor = torch.tensor(item_embeddings)
        cosine_scores = util.pytorch_cos_sim(query_embedding, item_embeddings_tensor)[0]
        results = sorted(zip(items, cosine_scores), key=lambda x: x[1], reverse=True)[:5]
        for item, score in results:
            print(f"{item['name']} (score: {score:.4f})")
        return results








