from sentence_transformers import SentenceTransformer
import pickle
import json

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer


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
    key = max(similarities, key= similarities.get).split('_')[0]
    return key
