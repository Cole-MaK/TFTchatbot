import google
from google import genai

from src.function_call import get_filters
from src.tactics_simple_api import get_champion_data, get_trait_data

import json
from dotenv import load_dotenv
import os

load_dotenv()

prompt = str(input("Prompt: "))

# key = get_rag_file(user_question=prompt, key_file="rag_keys.pkl", top_n=1)

# with open(f"jsoninfo_keys/{key[0]}_info.json","r") as file:
#         rag_data = json.load(file)['text']

filter_list = get_filters(prompt)
print(filter_list)
if filter_list[0][1] == 'units':

    tft_data = get_champion_data(filter_list)

    with open(f"jsoninfo_keys/champion_info.json","r") as file:
        rag_data = json.load(file)['text']

elif filter_list[0][1] == 'traits':

    tft_data = get_trait_data(filter_list)

    with open(f"jsoninfo_keys/synergy_info.json","r") as file:
        rag_data = json.load(file)['text']

llm_prompt = f"""
You are an expert in Team fight tactics Set 14 that provides concise and actionable responses. You are data-oriented so data and tables are vital to your thought process and take precident over retrieved information. Users tend to want to know what units or traits to target immediately, rather than large overviews, there is no need for explanations. No tables or explanations should be included in your response to the user. You're aim is to help players place higher either with average placement, top 4, or delta. Focus on statistics rather than your intuition. Remember even though League of Legends and TFT share champions and items, these are two distinct games. Only answer questions about TFT - Teamfight Tactics. 

User Prompt: {prompt}

Here is some extra retrieved information: {rag_data}.
Use this data as a supplement to the following table information.

This is the table with statistics tft_data: 
{tft_data}

The column "Name" is the name of the champion and the games that have been played with that champion.
The column "number of games" is how many games that champion has been played. 
The "win rate" column is the percentage of games won in decimals.
The "top 4 rate" is the pecentage of games that a player places top 4 in decimals.
The "average placement" is the average place that a player places from 1 to 8 with 1 being the best so a lower number is prefered.
The "delta" is the average place change with larger negative deltas being better since it brings the average placement closer to 0. Delta is one of the most important factors.


Again here is the question you are answering: {prompt}
"""

print(llm_prompt)
api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash", 
    contents=llm_prompt).text

print(response)