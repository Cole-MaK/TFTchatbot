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
from sentence_transformers import SentenceTransformer

from functions.functions import get_rag_file

load_dotenv()

## open full master prompt
# with open("full_info.json", "r") as file:
#     qa_data = json.load(file)['text']

# open test questions
with open("testset.json", "r") as file:
    qa_test = json.load(file)

# initialize client
api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

# initialize counter for question percentage
num_correct = 0

# iterate through all questions
for i, qa_pair in enumerate(qa_test):
    # get question and answer pair from json
    question = qa_pair["question"]
    answer = qa_pair["answer"]

    print(f"**Question {i+1}**: {question}")

    # decide what document to use by obtaining key
    key = get_rag_file(user_question=question, key_file="rag_keys.pkl")

    print(f"**Proposed Key**: {key}")

    # use key to access correct document
    with open(f"jsoninfo_keys/{key}_info.json","r") as file:
        qa_data = json.load(file)['text']

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
    
    # if similarity_score > .70:
    #     num_correct += 1
    # else:
    #     print(question)
    # print(response)
    
    print(f"**Model Response**: {response}")
    print(f"**True Answer**: {answer}")
    print(f"**Judge**: {judge_response}")

    # counter for correct
    if 'yes' in judge_response.lower():
        num_correct += 1
        print('anotha one')

    
    time.sleep(20)

print(f"Percentage Correct: {num_correct/len(qa_test)}")