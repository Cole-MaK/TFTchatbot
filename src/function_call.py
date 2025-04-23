from dotenv import load_dotenv

from google import genai
from google.genai.types import FunctionDeclaration, GenerateContentConfig, Part, Tool

import os

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

    model="gemini-2.0-flash"

    get_filters_function = {
        "name": "get_filters",
        "description": "Gets filter words for developer to use in a tft website",
        "parameters": {
            "type": "object",
            "properties": {
                "filter_1": {
                    "type": "string",
                    "description": f"A champion or trait in tft. The champions consist of: {champions}. The traits consist of: {traits}. Filters much match a champion or a trait exactly for you to return a valid filter."
                },
                "champion_tier_1": {
                    "type":"string",
                    "description": f"If the previous filter_1 includes a champions from this list: {champions}, the user can include a champion's star level if a number comes after a champion name. The options are 0 if nothing is specified, 1, 2, or 3."
                },
                "filter_2": {
                    "type": "string",
                    "description": f"If the user specifies another champion or trait in tft use this filter, the same champion options apply. The champions consist of: {champions}. The traits consist of {traits}. Filters much match a champion or a trait exactly for you to return a valid filter."
                },
                "champion_tier_2": {
                    "type":"string",
                    "description": f"If the previous filter_2 includes a champions from this list: {champions}, the user can include a champion's star level if a number comes after a champion name. The options are 0 if nothing is specified, 1, 2, or 3."
                },
                "filter_3": {
                    "type": "string",
                    "description": f"If the user specifies a third champion or trait in tft use this filter, the same champion options apply. The champions consist of: {champions}. The traits consist of {traits}. Filters much match a champion or a trait exactly for you to return a valid filter."
                },
                "champion_tier_3": {
                    "type":"string",
                    "description": f"If the previous filter_3 includes a champions from this list: {champions}, the user can include a champion's star level if a number comes after a champion name. The options are 0 if nothing is specified, 1, 2, or 3."
                },
            },
            "required": ["filter_1"]
        }
    }

    tools = Tool(function_declarations=[get_filters_function])
    config = GenerateContentConfig(tools = [tools])


    chat = client.chats.create(
        model=model,
        config=config,
    )
    # total tokens is around 2.5k
    response = chat.send_message(prompt)
    
    # print(response)
    if response.function_calls == None:
        return None
    else:
        filters = []

        for filter in response.function_calls[0].args.items():
            filters.append(filter)
        
        order = {'filter_1': 0, 'champion_tier_1': 1, "filter_2": 2, 'champion_tier_2':3, 'filter_3': 4, 'champion_tier_3':5}
        sorted_filters = sorted(filters, key=lambda x: order.get(x[0], float('inf')))
        return sorted_filters