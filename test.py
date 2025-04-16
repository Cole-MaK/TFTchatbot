from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode("Test sentence")
print(embedding.shape)

import pickle
import json

file_vectors = {

}

files = ["champion_key.json", "synergy_key.json", "item_key.json"]
for file in files:
    with open(file, "r") as file:
        qa_data = json.load(file)
    cur_data = qa_data['text']
    cur_file = qa_data['file_name']

    embedding = model.encode(cur_data)

    file_vectors[cur_file] = embedding

with open('rag_keys.pkl','wb') as file:
    pickle.dump(file_vectors, file)

# import requests
# import json

# url = 'https://d3.tft.tools/explorer-data/15080/1/u-TFT14_Alistar-0/u-TFT14_Jarvan-0'
# # payload = {'key': 'value'}

# headers = {
#     "authority": "d3.tft.tools",
#     "method": "GET",
#     "path": "/explorer-data/15080/1/u-TFT14_Annie-0/i-BlueBuff-TFT14_Annie-0",
#     "scheme": "https",
#     "accept": "/",
#     "accept-encoding":"gzip, deflate, br, zstd",
#     "accept-language":"en-US,en;q=0.9",
#     "origin": "https://tactics.tools/",
#     "priority":"u=1, i",
#     "referer":"https://tactics.tools/",
#     "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
#     "sec-ch-ua-mobile": "?1",
#     "sec-ch-ua-platform": "Andriod",
#     "sec-fetch-dest": "empty",
#     "sec-fetch-mode": "cors",
#     "sec-fetch-site": "cross-site",
#     "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
# }

# response = requests.post(url, headers=headers)
# print(response.status_code)
# print(response.json())

