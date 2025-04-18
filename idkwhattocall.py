import google
from google import genai

from src.functions import get_filters
from src.tactics import *

import json
from dotenv import load_dotenv
import os

load_dotenv()

prompt = str(input("Prompt: "))

filter_list = get_filters(prompt)

res = get_tactics_info(filter_list)
# res.to_csv('promptdata.csv', index=False)
table = res.to_string()

with open(f"jsoninfo_keys/champion_info.json","r") as file:
    qa_data = json.load(file)['text']
llm_prompt = f"""
    You are an expert in Team fight tactics Set 14. Remember even though League of Legends and TFT share champions and items, these are two distinct games. Only answer questions about TFT - Teamfight Tactics. You often look at League of Legends information but only consider TFT information.
    
    You are working with a pandas data frame in python. The name of the data frame is tft_data.
    This is the table tft_data:
    {table}
    Follow these instructions:
    Use the following retrieved information about TFT set 14 champions:
    {qa_data}
    as well as the data in tft_data to answer the user question

    Your response should be heavily decided by the statistics given by the table tft_data.

    User Question: {prompt}
"""
print(llm_prompt)
api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=prompt).text

print(response)