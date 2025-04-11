from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode("Test sentence")
print(embedding.shape)

import pickle
import json

file_vectors = {

}

files = ["champion_info.json", "synergy_info.json", "item_info.json"]
for file in files:
    with open(file, "r") as file:
        qa_data = json.load(file)
    cur_data = qa_data['text']
    cur_file = qa_data['file_name']

    embedding = model.encode(cur_data)

    file_vectors[cur_file] = embedding

with open('file_vectors.pkl','wb') as file:
    pickle.dump(file_vectors, file)

