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
qa_data = qa_data['text']

with open("testset.json", "r") as file:
    qa_test = json.load(file)

api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

num_correct = 0

for i, qa_pair in enumerate(qa_test):
    question = qa_pair["question"]
    answer = qa_pair["answer"]

    prompt = f"""
    You are an expert in TFT. Use the following retrieved information to answer the question accurately.

    A few things to keep in mind: When asked about traits, do not include the cost of a champion. Shield and Durability are not the same thing. Do not use champion trait information from previous TFT sets, only use the provided context for traits

    {qa_data} 

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
    # completion = openai_client.chat.completions.create(
    #     model="nvidia/llama-3.1-nemotron-nano-8b-v1:free",
    #     messages=[{"role": "user",
    #     "content": open_ai_prompt}]
    # )

    judge_response = client.models.generate_content(
        model="gemini-2.0-flash", contents=judge_prompt
    ).text

    # open_ai_response = completion.choices[0].message.content


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