import google
from google import genai

import numpy as np
import pandas as pd

from dotenv import load_dotenv
import os
import json
import time

from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

load_dotenv()

with open("extracted_text.json", "r") as file:
    qa_data = json.load(file)

with open("testset.json", "r") as file:
    qa_test = json.load(file)

qa_data = qa_data['text']

api_key = os.getenv('API_KEY')
client = genai.Client(api_key=api_key)

model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

num_correct = 0

for i, qa_pair in enumerate(qa_test):
    question = qa_pair["question"]
    answer = qa_pair["answer"]

    prompt = f"""
    You are an expert in TFT set 14. Use the following retrieved information to answer the question accurately. You can also use any past information you have about TFT.

    {qa_data} 
    User Question: {question}
"""
    
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=prompt
    ).text

    answers = [answer, response]

    embeddings = model.encode(answers)
    similarity_score = cosine_similarity(embeddings)[0][1]
    print(i+1)
    if similarity_score > .70:
        num_correct += 1
    else:
        print(question)
    print(response)
    
    time.sleep(15)

print(f"Percentage Correct: {num_correct/len(qa_test)}")