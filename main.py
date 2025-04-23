import google
from google import genai

from src.functions import get_filters, get_rag_file
from src.tactics_simple_api import get_champion_data, get_trait_data

import json
from dotenv import load_dotenv
import os

load_dotenv()

prompt = str(input("Prompt: "))

# key = get_rag_file(user_question=prompt, key_file="rag_keys.pkl", top_n=1)

# with open(f"jsoninfo_keys/{key[0]}_info.json","r") as file:
#         rag_data = json.load(file)['text']

with open(f"jsoninfo_keys/champion_info.json","r") as file:
        rag_data = json.load(file)['text']

filter_list = get_filters(prompt)
print(filter_list)
tft_data = get_champion_data(filter_list)

# print(get_trait_data(filter_list))

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



#----------------------
# champions = ', '.join(filter_list)
# res = get_tactics_info(filter_list)
# table = res.to_string()

# llm_prompt = f"""
#     You are an expert in Team fight tactics Set 14. Remember even though League of Legends and TFT share champions and items, these are two distinct games. Only answer questions about TFT - Teamfight Tactics. 
    
#     You are working with a pandas data frame in python. The name of the data frame is tft_data.
#     This is the table tft_data:
#     {table}.
#     The column "games" refers to how many times the champion is played with {champions}.
#     The "play_rate" refers to the percentage of games that {champions} is played with the champion in the row.
#     A negative delta is better than a positive delta as place has a continuous range from 1 to 8 with 1 being the best and 8 being the worst.
#     This goes for the rest of the columns.

#     Here is some retrieved information on the champions that can be useful:
#     {rag_data}
    
#     User Question: {prompt}
# """

# api_key = os.getenv('API_KEY')

# client = genai.Client(api_key=api_key)

# response = client.models.generate_content(
#     model="gemini-2.0-flash", 
#     contents=llm_prompt).text

# print(response)