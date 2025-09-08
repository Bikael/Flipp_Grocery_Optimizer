from sentence_transformers import SentenceTransformer, util

class DealSelector:
    def __init__(self,flyer_data, query):
        self.flyer_data = flyer_data
        self.query = query

    def semantic_matcher(self,):
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        names = []
        for item in self.flyer_data:
            names.append(item["name"])
        
        # 3. Encode documents into embeddings
        doc_embeddings = model.encode(names, convert_to_tensor=True)

        # 4. Encode the query
        query_embedding = model.encode(self.query, convert_to_tensor=True)

        # 5. Compute cosine similarity between query and documents
        cosine_scores = util.pytorch_cos_sim(query_embedding, doc_embeddings)[0]

        # 6. Show ranked results
        results = sorted(zip(names, cosine_scores), key=lambda x: x[1], reverse=True)

        print(f"Query: {self.query}\n")
        for doc, score in results:
            print(f"{doc:30}  (score: {score:.4f})")



            


