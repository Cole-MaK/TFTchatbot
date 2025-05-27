from google import genai
from google.genai.types import FunctionDeclaration, GenerateContentConfig, ToolConfig, Part, Tool, FunctionCallingConfig

import json

from src.client import GenerateContent
from src.tactics_simple_api import get_champion_data, get_trait_data
from src.rag_functions import *

def frontend_func(contents, client_model):

    # obtains user question from content list
    prompt = contents[-1]["parts"][0]['text']

    key = get_rag_file(user_question=prompt, key_file="rag_keys.pkl", top_n=1)

    with open(f"jsoninfo_keys/{key[0]}_info.json","r") as file:
            rag_data = json.load(file)['text']

    rag_prompt = f"""
        You are an expert in Team fight tactics Set 14 that provides concise and actionable responses. Remember even though League of Legends and TFT share champions and items, these are two distinct games. Only answer questions about TFT - Teamfight Tactics. 

        User Prompt: {prompt}

        Here is some retrieved information: {rag_data}

        Decide if you are able to answer the user question with this information. If so then there is no need to call a function or tool but if you can not then you also have access to function calling or tools.
    """

    contents.append({"parts": [{"text":rag_prompt}], "role":"user"})
    
    response = client_model.generate(contents)

    # first case if the model is able to answer user question with rag information
    if response.function_calls == None:
        return response.candidates[0].content.parts[0].text
    
    # second case if the model decided to function call to get filters for tactics | this 'else' case creates a sorted filter list 
    else:
        filters = []

        for filter in response.function_calls[0].args.items():
            filters.append(filter)
        
        order = {'tab': 0, 'filter_1': 1, 'champion_tier_1': 2, "filter_2": 3, 'champion_tier_2': 4, 'filter_3': 5, 'champion_tier_3': 6}
        filter_list = sorted(filters, key=lambda x: order.get(x[0], float('inf')))
    
    # based on function call, get unit or trait information
    if isinstance(filter_list, list):
        if filter_list[0][1] == 'units':

            tft_data = get_champion_data(filter_list)

            with open(f"jsoninfo_keys/champion_info.json","r") as file:
                rag_data = json.load(file)['text']

        elif filter_list[0][1] == 'traits':

            tft_data = get_trait_data(filter_list)

            with open(f"jsoninfo_keys/synergy_info.json","r") as file:
                rag_data = json.load(file)['text']
        
        # creating string to provide context for the table obtained from tactics.tools
        table_string = "This is the table, tft_data, with the aggregated statistics for the "
        for item in filter_list:
            if item[0] == 'tab':
                table_string += f"{item[1]} when playing "
            elif 'filter' in item[0]:
                table_string += f"{item[1]}, "
        table_string = table_string[:-2]

        llm_prompt = f"""
Use the information provided to answer the following user question: {prompt}

Here is some extra retrieved information: {rag_data}.
Use this data as a supplement to the following table information.

{table_string}: 
{tft_data}

The column "Name" is the name of the champion and the games that have been played with that champion.
The column "number of games" is how many games that champion has been played. 
The "win rate" column is the percentage of games won in decimals.
The "top 4 rate" is the pecentage of games that a player places top 4 in decimals.
The "average placement" is the average place that a player places from 1 to 8 with 1 being the best so a lower number is prefered.
The "delta" is the average place change with larger negative deltas being better since it brings the average placement closer to 0. Delta is one of the most important factors.


Again here is the question you are answering: {prompt}
Do not start your response with "Based on the data" or anything similar. Do not mention anything to do with the fact that you have access to data since the user can not see the results of the function call so do not reference it. Your response should seem like you already have knowledge of the statistics.
        """

        contents.append({"parts": [{"text":llm_prompt}], "role":"user"})
        
        response = client_model.generate(contents)

        return response.candidates[0].content.parts[0].text