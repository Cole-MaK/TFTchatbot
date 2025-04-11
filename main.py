import google
from google import genai

import numpy as np
import pandas as pd
import pickle

from dotenv import load_dotenv
import os
import json
import time

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

load_dotenv()

# model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

# user_question = input(str("Question: "))

# embedding = model.encode(user_question)

# with open("file_vectors.pkl", 'rb') as file:
#     rag_vectors = pickle.load(file)

# similarities = {}

# for vector_name, vector in rag_vectors.items():
#     embeddings = [vector, embedding]
#     similarity_score = cosine_similarity(embeddings)#[0][1]
#     print(similarity_score)
    
#     similarities[vector_name] = similarity_score

# print(similarities)

with open("full_info.json", "r") as file:
    qa_data = json.load(file)
qa_data = qa_data['text']

with open("testset.json", "r") as file:
    qa_test = json.load(file)

api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

num_correct = 0

for i, qa_pair in enumerate(qa_test):
    question = qa_pair["question"]
    answer = qa_pair["answer"]

    prompt = f"""
    You are an expert in TFT Set 14. Use the following retrieved information to answer the question accurately.

    {qa_data} 
    
    Make sure to think before answering the user question.

    User Question: {question}
"""

    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    ).text

    judge_prompt = f"""
    Your job is to decide if two answers are similar with a simple yes or no. Also include a short sentence as to why you chose your answer. Write your response in the format:
    Yes or No because:

    These are the two answers: 
    {answer}
    and
    {response}    
"""

    judge_response = client.models.generate_content(
        model="gemini-2.0-flash", contents=judge_prompt
    ).text

    ## Cosine Similarity
    # answers = [answer, response]
    # embeddings = model.encode(answers)
    # similarity_score = cosine_similarity(embeddings)[0][1]
    
    print(i+1)
    if 'yes' in judge_response.lower():
        num_correct += 1
        print('anotha one')

    print(response)
    print(answer)
    print(judge_response)
    # if similarity_score > .70:
    #     num_correct += 1
    # else:
    #     print(question)
    # print(response)
    
    time.sleep(20)

print(f"Percentage Correct: {num_correct/len(qa_test)}")