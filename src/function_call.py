def filter_tool():
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

    return get_filters_function