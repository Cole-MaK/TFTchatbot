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
champions = ', '.join(filter_list)
res = get_tactics_info(filter_list)
# res.to_csv('promptdata.csv', index=False)
table = res.to_string()

with open(f"jsoninfo_keys/champion_info.json","r") as file:
    qa_data = json.load(file)['text']
llm_prompt = f"""
    You are an expert in Team fight tactics Set 14. Remember even though League of Legends and TFT share champions and items, these are two distinct games. Only answer questions about TFT - Teamfight Tactics. 
    
    You are working with a pandas data frame in python. The name of the data frame is tft_data.
    This is the table tft_data:
    {table}.
    The column "games" refers to how many times the champion is played with {champions}.
    The "play_rate" refers to the percentage of games that {champions} is played with the champion in the row.
    A negative delta is better than a positive delta as place has a continuous range from 1 to 8 with 1 being the best and 8 being the worst.
    This goes for the rest of the columns.

    Here is some retrieved information on the champions that can be useful:
    {qa_data}
    
    User Question: {prompt}
"""

api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=llm_prompt).text

print(response)