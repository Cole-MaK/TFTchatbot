from google import genai
from google.genai.types import FunctionDeclaration, GenerateContentConfig, ToolConfig, Part, Tool, FunctionCallingConfig

import os
import json
from dotenv import load_dotenv

from src.tactics_simple_api import get_champion_data, get_trait_data
from src.rag_functions import *

load_dotenv()

api_key = os.getenv('API_KEY')

client = genai.Client(api_key=api_key)

def get_filters(prompt):
    '''
    input (str): a user prompt that they ask they want to ask the LLM
    return
    filters (list): a list of 1-3 filters to use to search tactics.tools

    '''

    champions = "Alistar, Annie, Aphelios, Aurora, Brand, Braum, Chogath, Darius, Draven, Dr. Mundo, Ekko, Elise, Fiddlesticks, Galio, Garen, Gragas, Graves, Illaoi, Jarvan IV, Jax, Jhin, Jinx, Kindred, Kobuko, Kogmaw, Leblanc, Leona, Mis Fortune, Mordekaiser, Morgana, Naafiri, Neeko, Nidalee, Poppy, Renekton, Rengar, Rhaast, Samira, Sejuani, Senna, Seraphine, Shaco, Shyvana, Skarner, Sylas, Twisted Fate, Urgot, Varus, Vayne, Veigar, Vex, Vi, Viego, Xayah, Yuumi, Zac, Zed, Zeri, Ziggs, Zyra"

    traits = "3 Anima Squad, 5 Anima Squad, 7 Anima Squad, 10 Anima Squad, 2 BoomBot, 4 BoomBot, 6 BoomBot, 2 Cyberboss, 3 Cyberboss, 4 Cyberboss, 3 Cypher, 4 Cypher, 5 Cypher, 1 Divinicorp, 2 Divinicorp, 3 Divinicorp, 4 Divinicorp, 5 Divinicorp, 6 Divinicorp, 7 Divinicorp, 3 Exotech, 5 Exotech, 7 Exotech, 10 Exotech, 1 God of the Net, 2 Golden Ox, 4 Golden Ox, 6 Golden Ox, 3 Nitro, 4 Nitro, 1 Overlord, 1 Soul Killer, 3 Street Demon, 5 Street Demon, 7 Street Demon, 10 Street Demon, 3 Syndicate, 5 Syndicate, 7 Syndicate, 1 Virus, 2 A.M.P., 3 A.M.P., 4 A.M.P., 5 A.M.P., 2 Bastion, 4 Bastion, 6 Bastion, 2 Bruiser, 4 Bruiser, 6 Bruiser, 2 Dynamo, 3 Dynamo, 4 Dynamo, 2 Executioner, 3 Executioner, 4 Executioner, 5 Executioner, 2 Marksman, 4 Marksman, 2 Rapidfire, 4 Rapidfire, 6 Rapidfire, 2 Slayer, 4 Slayer, 6 Slayer, 2 Strategist, 3 Strategist, 4 Strategist, 5 Strategist, 2 Techie, 4 Techie, 6 Techie, 8 Techie, 2 Vanguard, 4 Vanguard, 6 Vanguard"

    get_filters_function = {
        "name": "get_filters",
        "description": f"Gets filter words for a tft website. A prompt with context will be provided to you and you need to decide if you have enough information to answer the user prompt. If you can answer the question already there is no need to call this function. If you do not have enough information to answer the user prompt then call this function. If you choose to select some parameters then look at the section of the prompt that comes after 'User Prompt: '. This is a list of the champions: {champions} and this is a list of traits: {traits}. Champions and traits are seperated by commas. If the question is asking what is good with a champions/trait then this function will have to be called, the context alone is not enough. When asked if one champion or another champions is better with some combination of champions and traits, the filters should reflect the said combination. For example: Does Alister or Aphelios have a higher winrate with 5 anima squad. Then the filters that you pick should just be 7 anima squad. This also applies for traits, when asked if one trait or another trait is better with some combination of champions and traits, the filters you pick should reflect the said combination. For example: Is 4 techie or 4 strategist better with 7 street demon? Then you should only select 7 street demon as the only filter.",
        "parameters": {
            "type": "object",
            "properties": {
                "filter_1": {
                    "type": "string",
                    "description": f"A champion or trait in tft. The list of champions are seperated by commas and consist of: {champions}. The list of traits are seperated by commas and consist of: {traits}. A returned filter much match a champion or a trait exactly for you to return a valid filter. When asked if one champion or another is better with some combination of champions and traits, the filters should reflect the said combination. For example: Does Viego or Renekton have a higher winrate with 7 anima squad. Then the filters that you pick should just be 7 anima squad."
                },
                "champion_tier_1": {
                    "type":"string",
                    "description": f"If the previous filter_1 includes a champions from this list: {champions}, the user can include a champion's star level if a number comes before or after a champion name. Users often say the number then 'star' then the champion name too. For example, 3 star Alistar or 2 star Vayne, where Alistar and Vayne are options in the champions list. The options are 0 if nothing is specified, 1, 2, or 3."
                },
                "filter_2": {
                    "type": "string",
                    "description": f"If the user specifies another champion or trait in tft use this filter, the same champion options apply. The champions list is seperated by commas and consist of: {champions}. The list of traits are seperated by commas and consist of {traits}. Filters much match a champion or a trait exactly for you to return a valid filter. If you think of returning something that is not in the list of champions or traits DO NOT return anything. When asked if one champion or another is better with some combination of champions and traits, the filters should reflect the said combination. For example: Does Viego or Renekton have a higher winrate with 7 anima squad. Then the filters that you pick should just be 7 anima squad."
                },
                "champion_tier_2": {
                    "type":"string",
                    "description": f"If the previous filter_2 includes a champions from this list: {champions}, the user can include a champion's star level if a number comes before or after a champion name. Users sometime say the number then 'star' then the champion name too. For example, 3 star Alistar or 2 star Vayne. The options are 0 if nothing is specified, 1, 2, or 3."
                },
                "filter_3": {
                    "type": "string",
                    "description": f"If the user specifies a third champion or trait in tft use this filter, the same champion options apply. The list of champions are seperated by commas and consist of: {champions}. The list of traits are seperated by commas and consist of {traits}. Filters much match a champion or a trait exactly for you to return a valid filter. If you think of returning something that is not in the list of champions or traits DO NOT return anything When asked if one champion or another is better with some combination of champions and traits, the filters should reflect the said combination. For example: Does Viego or Renekton have a higher winrate with 7 anima squad. Then the filters that you pick should just be 7 anima squad.."
                },
                "champion_tier_3": {
                    "type":"string",
                    "description": f"If the previous filter_3 includes a champions from this list: {champions}, the user can include a champion's star level if a number comes before or after a champion name. Users sometime say the number then 'star' then the champion name too. For example, 3 star Alistar or 2 star Vayne. The options are 0 if nothing is specified, 1, 2, or 3."
                },
                "tab": {
                    "type":"string",
                    "description": 'Decide what tab of information to pull from a website. Typically when champion or champions is mentioned pick units. The options are units or traits'
                }
            },
            "required": ["filter_1", "tab"]
        }
    }


    tools = [Tool(function_declarations=[get_filters_function])]
    config = {
    "tools": tools,
    "automatic_function_calling": {"disable": False},
    # Force the model to call 'any' function, instead of chatting.
    "tool_config": {"function_calling_config": {"mode": "AUTO"}},
}

    model="gemini-2.5-flash-preview-04-17"

    chat = client.chats.create(
        model=model,
        config=config,
    )
    # total tokens is around 2.5k
    response = chat.send_message(prompt)
    print(response)
    if response.function_calls == None:
        return response.candidates[0].content.parts[0].text
    else:
        filters = []

        for filter in response.function_calls[0].args.items():
            filters.append(filter)
        
        order = {'tab':0, 'filter_1': 1, 'champion_tier_1': 2, "filter_2": 3, 'champion_tier_2':4, 'filter_3': 5, 'champion_tier_3':6}
        sorted_filters = sorted(filters, key=lambda x: order.get(x[0], float('inf')))
        return sorted_filters

def frontend_func(prompt):

    key = get_rag_file(user_question=prompt, key_file="rag_keys.pkl", top_n=1)

    with open(f"jsoninfo_keys/{key[0]}_info.json","r") as file:
            rag_data = json.load(file)['text']

    rag_prompt = f"""
        You are an expert in Team fight tactics Set 14 that provides concise and actionable responses. Remember even though League of Legends and TFT share champions and items, these are two distinct games. Only answer questions about TFT - Teamfight Tactics. 

        User Prompt: {prompt}

        Here is some retrieved information: {rag_data}

        Decide if you are able to answer the user question with this information. If so then there is no need to call a function or tool but if you can not then you also have access to function calling or tools.
    """
    filter_list = get_filters(rag_prompt)
    if isinstance(filter_list, str):
        return(filter_list)

    if isinstance(filter_list, list):
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
        
        model = "gemini-2.5-flash-preview-04-17"
        response = client.models.generate_content(
            model=model, 
            contents=llm_prompt).text

        return(response)