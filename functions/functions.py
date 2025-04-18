from sentence_transformers import SentenceTransformer
import pickle
import json

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

from google import genai
from google.genai.types import FunctionDeclaration, GenerateContentConfig, Part, Tool

import os


def get_rag_keys(file_list):
    '''
    input:
    file_list (list): A list of file names that are meant to be used as keys for full rag documents. Keys should be in json with "file_name" and "text"

    return: None

    Output: a pkl file with vector embeddings of document keys
    '''
    model = SentenceTransformer('all-MiniLM-L6-v2')

    file_vectors = {

    }

    files = file_list
    for file in files:
        with open(f"jsoninfo_keys/{file}", "r") as file:
            qa_data = json.load(file)
        cur_data = qa_data['text']
        cur_file = qa_data['file_name']

        embedding = model.encode(cur_data)

        file_vectors[cur_file] = embedding

    with open('rag_keys.pkl','wb') as file:
        pickle.dump(file_vectors, file)

def get_rag_file(user_question, key_file):
    '''
    input:
    user_question (str): user prompt
    key_file: dictionary of vector embeddings of key documents

    output:
    return key: name to get document
    '''

    model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

    embedding = model.encode(user_question)

    with open(key_file, 'rb') as file:
        rag_vectors = pickle.load(file)

    similarities = {}

    for vector_name, vector in rag_vectors.items():
        embeddings = [vector, embedding]
        similarity_score = cosine_similarity(embeddings)[0][1]
        
        similarities[vector_name] = similarity_score
    print(similarities)
    
    top_2_keys = sorted(similarities, key=similarities.get, reverse=True)[:2]
    top_2 = [key.split('_')[0] for key in top_2_keys]
    return top_2
    # key = max(similarities, key= similarities.get).split('_')[0]
    return key

def get_filters(prompt):
    '''
    input (str): a user prompt that they ask they want to ask the LLM
    return
    filters (list): a list of 1-3 filters to use to search tactics.tools

    '''
    PROJECT_ID = "cmak-123"
    LOCATION = "us-west1"
    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

    model="gemini-2.0-flash"

    get_filters_function = {
        "name": "get_filters",
        "description": "Gets filter words for developer to use in a tft website",
        "parameters": {
            "type": "object",
            "properties": {
                "filter_1": {
                    "type": "string",
                    "description": "A champion in tft. The champions consist of: Alistar, Annie, Aphelios, Aurora, Brand, Braum, Chogath, Darius, Draven, Dr. Mundo, Ekko, Elise, Fiddlesticks, Galio, Garen, Gragas, Graves, Illaoi, Jarvan IV, Jax, Jhin, Jinx, Kindred, Kobuko, Kogmaw, Leblanc, Leona, Mis Fortune, Mordekaiser, Morgana, Naafiri, Neeko, Nidalee, Poppy, Renekton, Rengar, Rhaast, Samira, Sejuani, Senna, Seraphine, Shaco, Shyvana, Skarner, Sylas, Twisted Fate, Urgot, Varus, vayne, Veigar, Vex, Vi, Viego, Xayah, Yuumi, Zac, Zed, Zeri, Ziggs, Zyra"
                },
                "filter_2": {
                    "type": "string",
                    "description": "If the user specifies another champion in tft use this filter, the same champion options apply. The champions consist of: Alistar, Annie, Aphelios, Aurora, Brand, Braum, Chogath, Darius, Draven, Dr. Mundo, Ekko, Elise, Fiddlesticks, Galio, Garen, Gragas, Graves, Illaoi, Jarvan IV, Jax, Jhin, Jinx, Kindred, Kobuko, Kogmaw, Leblanc, Leona, Mis Fortune, Mordekaiser, Morgana, Naafiri, Neeko, Nidalee, Poppy, Renekton, Rengar, Rhaast, Samira, Sejuani, Senna, Seraphine, Shaco, Shyvana, Skarner, Sylas, Twisted Fate, Urgot, Varus, vayne, Veigar, Vex, Vi, Viego, Xayah, Yuumi, Zac, Zed, Zeri, Ziggs, Zyra"
                },
                "filter_3": {
                    "type": "string",
                    "description": "If the user specifies a third champion in tft use this filter, the same champion options apply. The champions consist of: Alistar, Annie, Aphelios, Aurora, Brand, Braum, Chogath, Darius, Draven, Dr. Mundo, Ekko, Elise, Fiddlesticks, Galio, Garen, Gragas, Graves, Illaoi, Jarvan IV, Jax, Jhin, Jinx, Kindred, Kobuko, Kogmaw, Leblanc, Leona, Mis Fortune, Mordekaiser, Morgana, Naafiri, Neeko, Nidalee, Poppy, Renekton, Rengar, Rhaast, Samira, Sejuani, Senna, Seraphine, Shaco, Shyvana, Skarner, Sylas, Twisted Fate, Urgot, Varus, vayne, Veigar, Vex, Vi, Viego, Xayah, Yuumi, Zac, Zed, Zeri, Ziggs, Zyra"
                }
            },
            "required": ["filter_1"]
        }
    }

    tools = Tool(function_declarations=[get_filters_function])
    config = GenerateContentConfig(tools = [tools])


    chat = client.chats.create(
        model=model,
        config=config,
    )

    response = chat.send_message(prompt)
    # print(response)
    if response.function_calls == None:
        return None
    else:
        filters = []

        for champion in response.function_calls[0].args.values():
            filters.append(champion)
        
        return filters