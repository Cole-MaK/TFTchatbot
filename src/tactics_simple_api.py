
import json
import requests

# Anatomy of request
# Base URL: https://d3.tft.tools/explorer-data/15080/1/

# For champ, prefix with u-
# For trait, prefix with t-

# Then add champion or trait name ie. TFT14_Alistar-0 or TFT14_AnimaSquad-4
# Finally add the level

# For champions, 0 for any, 1 for 1 star, 2 for 2 star, 3 for 3 star
# For traits, 1 for bronze, 2 for silver, 3 for gold, and 4 for prismatic (no 0)
    # Except for divinicorp, which is just the number 1-7

# For example, for 5 divinicorp and 2 star garen, the url is:
# https://d3.tft.tools/explorer-data/15080/1/u-TFT14_Garen-2/t-TFT14_Divinicorp-5/

base_url = "https://d3.tft.tools/explorer-data/15080/1/"

trait_mapping = {
    '3 Anima Squad': 'TFT14_AnimaSquad-1',
    '5 Anima Squad': 'TFT14_AnimaSquad-2',
    '7 Anima Squad': 'TFT14_AnimaSquad-3',
    '10 Anima Squad': 'TFT14_AnimaSquad-4',
    '2 BoomBot': 'TFT14_BallisTek-1',
    '4 BoomBot': 'TFT14_BallisTek-2',
    '6 BoomBot': 'TFT14_BallisTek-3',
    '2 Cyberboss': 'TFT14_Cyberboss-1',
    '3 Cyberboss': 'TFT14_Cyberboss-2',
    '4 Cyberboss': 'TFT14_Cyberboss-3',
    '3 Cypher': 'TFT14_Suits-1',
    '4 Cypher': 'TFT14_Suits-2',
    '5 Cypher': 'TFT14_Suits-3',
    '1 Divinicorp': 'TFT14_Divinicorp-1',
    '2 Divinicorp': 'TFT14_Divinicorp-2',
    '3 Divinicorp': 'TFT14_Divinicorp-3',
    '4 Divinicorp': 'TFT14_Divinicorp-4',
    '5 Divinicorp': 'TFT14_Divinicorp-5',
    '6 Divinicorp': 'TFT14_Divinicorp-6',
    '7 Divinicorp': 'TFT14_Divinicorp-7',
    '3 Exotech': 'TFT14_EdgeRunner-1',
    '5 Exotech': 'TFT14_EdgeRunner-2',
    '7 Exotech': 'TFT14_EdgeRunner-3',
    '10 Exotech': 'TFT14_EdgeRunner-4',
    '1 God of the Net': 'TFT14_Netgod-1',
    '2 Golden Ox': 'TFT14_Immortal-1',
    '4 Golden Ox': 'TFT14_Immortal-2',
    '6 Golden Ox': 'TFT14_Immortal-3',
    '3 Nitro': 'TFT14_HotRod-1',
    '4 Nitro': 'TFT14_HotRod-2',
    '1 Overlord': 'TFT14_Overlord-1',
    '1 Soul Killer': 'TFT14_ViegoUniqueTrait-1',
    '3 Street Demon': 'TFT14_StreetDemon-1',
    '5 Street Demon': 'TFT14_StreetDemon-2',
    '7 Street Demon': 'TFT14_StreetDemon-3',
    '10 Street Demon': 'TFT14_StreetDemon-4',
    '3 Syndicate': 'TFT14_Mob-1',
    '5 Syndicate': 'TFT14_Mob-2',
    '7 Syndicate': 'TFT14_Mob-3',
    '1 Virus': 'TFT14_Virus-1',
    '2 A.M.P.': 'TFT14_Supercharge-1',
    '3 A.M.P.': 'TFT14_Supercharge-2',
    '4 A.M.P.': 'TFT14_Supercharge-3',
    '5 A.M.P.': 'TFT14_Supercharge-4',
    '2 Bastion': 'TFT14_Armorclad-1',
    '4 Bastion': 'TFT14_Armorclad-2',
    '6 Bastion': 'TFT14_Armorclad-3',
    '2 Bruiser': 'TFT14_Bruiser-1',
    '4 Bruiser': 'TFT14_Bruiser-2',
    '6 Bruiser': 'TFT14_Bruiser-3',
    '2 Dynamo': 'TFT14_Thirsty-1',
    '3 Dynamo': 'TFT14_Thirsty-2',
    '4 Dynamo': 'TFT14_Thirsty-3',
    '2 Executioner': 'TFT14_Cutter-1',
    '3 Executioner': 'TFT14_Cutter-2',
    '4 Executioner': 'TFT14_Cutter-3',
    '5 Executioner': 'TFT14_Cutter-4',
    '2 Marksman': 'TFT14_Marksman-1',
    '4 Marksman': 'TFT14_Marksman-2',
    '2 Rapidfire': 'TFT14_Swift-1',
    '4 Rapidfire': 'TFT14_Swift-2',
    '6 Rapidfire': 'TFT14_Swift-3',
    '2 Slayer': 'TFT14_Strong-1',
    '4 Slayer': 'TFT14_Strong-2',
    '6 Slayer': 'TFT14_Strong-3',
    '2 Strategist': 'TFT14_Controller-1',
    '3 Strategist': 'TFT14_Controller-2',
    '4 Strategist': 'TFT14_Controller-3',
    '5 Strategist': 'TFT14_Controller-4',
    '2 Techie': 'TFT14_Techie-1',
    '4 Techie': 'TFT14_Techie-2',
    '6 Techie': 'TFT14_Techie-3',
    '8 Techie': 'TFT14_Techie-4',
    '2 Vanguard': 'TFT14_Vanguard-1',
    '4 Vanguard': 'TFT14_Vanguard-2',
    '6 Vanguard': 'TFT14_Vanguard-3'
    }
champion_mapping = {
    'Varus': 'TFT14_Varus',
    'Jarvan IV': 'TFT14_Jarvan',
    'Dr. Mundo': 'TFT14_DrMundo',
    'Mordekaiser': 'TFT14_Mordekaiser',
    'Kobuko': 'TFT14_Kobuko',
    'Shyvana': 'TFT14_Shyvana',
    'Elise': 'TFT14_Elise',
    'Illaoi': 'TFT14_Illaoi',
    'Fiddlesticks': 'TFT14_Fiddlesticks',
    'Naafiri': 'TFT14_Naafiri',
    'Tibbers': 'TFT14_AnnieTibbers',
    'Shaco': 'TFT14_Shaco',
    'Sejuani': 'TFT14_Sejuani',
    'T-43X': 'TFT14_SummonLevel4',
    'Twisted Fate': 'TFT14_TwistedFate',
    'R-080T': 'TFT14_SummonLevel2',
    'Zeri': 'TFT14_Zeri',
    'Skarner': 'TFT14_Skarner',
    'Vex': 'TFT14_Vex',
    'Neeko': 'TFT14_Neeko',
    'Zac': 'TFT14_Zac',
    'Brand': 'TFT14_Brand',
    'Vayne': 'TFT14_Vayne',
    'Senna': 'TFT14_Senna',
    'Galio': 'TFT14_Galio',
    'Samira': 'TFT14_Samira',
    'Xayah': 'TFT14_Xayah',
    'Ziggs': 'TFT14_Ziggs',
    'Zed': 'TFT14_Zed',
    'Annie': 'TFT14_Annie',
    'Zyra': 'TFT14_Zyra',
    'Yuumi': 'TFT14_Yuumi',
    'Jhin': 'TFT14_Jhin',
    'Graves': 'TFT14_Graves',
    'Viego': 'TFT14_Viego',
    'Braum': 'TFT14_Braum',
    'Leona': 'TFT14_Leona',
    "Cho'Gath": 'TFT14_Chogath',
    'Ekko': 'TFT14_Ekko',
    'Sylas': 'TFT14_Sylas',
    'Draven': 'TFT14_Draven',
    'Kindred': 'TFT14_Kindred',
    'Miss Fortune': 'TFT14_MissFortune',
    'Urgot': 'TFT14_Urgot',
    'Jax': 'TFT14_Jax',
    'Rengar': 'TFT14_Rengar',
    'Aurora': 'TFT14_Aurora',
    'Nidalee': 'TFT14_NidaleeCougar',
    'Poppy': 'TFT14_Poppy',
    'LeBlanc': 'TFT14_LeBlanc',
    'Vi': 'TFT14_Vi',
    'Darius': 'TFT14_Darius',
    'Morgana': 'TFT14_Morgana',
    'Garen': 'TFT14_Garen',
    'Gragas': 'TFT14_Gragas',
    'Seraphine': 'TFT14_Seraphine',
    'Jinx': 'TFT14_Jinx',
    'Alistar': 'TFT14_Alistar',
    'Renekton': 'TFT14_Renekton',
    'Veigar': 'TFT14_Veigar',
    "Kog'Maw": 'TFT14_KogMaw',
    'Aphelios': 'TFT14_Aphelios',
    'Rhaast': 'TFT14_Rhaast'}


champion_mapping_reverse = {v: k for k, v in champion_mapping.items()}
trait_mapping_reverse = {v: k for k, v in trait_mapping.items()}

def _post_process_champion(data, top_n=10):
    # Sort by win rate
    output = []
    for row in data:
        name = row[0]
        output.append({
            "name": champion_mapping_reverse[name],
            "count": row[1]["count"],
            "win_rate": round(row[1]["won"] / row[1]["count"], 2),
            "top_4_rate": round(row[1]["top4"] / row[1]["count"], 2),
            "average_placement": round(row[1]["place"] / row[1]["count"], 2),
            "delta": round(row[1]['delta'], 2)
        })

    # Sort by count
    output.sort(key=lambda x: x["count"], reverse=True)
    return output[:top_n]

def _post_process_trait(data, top_n=10):
    # Sort by win rate
    output = []
    for row in data:
        # TODO: add tier to the trait
        name = row[0] + f"-{str(row[1])}"
        output.append({
            "name": trait_mapping_reverse[name],
            "count": row[2]["count"],
            "win_rate": round(row[2]["won"] / row[2]["count"], 2),
            "top_4_rate": round(row[2]["top4"] / row[2]["count"], 2),
            "average_placement": round(row[2]["place"] / row[2]["count"], 2),
            "delta": round(row[2]['delta'], 2)
        })

    # Sort by count
    output.sort(key=lambda x: x["count"], reverse=True)
    return output[:top_n]

def _to_string(data):
    # TODO: can optimize this format
    output = "Name, number of games, win rate, top 4 rate, average placement, delta\n"
    for item in data:
        output += f"{item['name']}, {item['count']}, {item['win_rate']}, {item['top_4_rate']}, {item['average_placement']}, {item['delta']}\n"
    return output

def get_champion_data(filter_list):
    # Each filter is a champion or trait with a tier
    # Champions are u-<champion>-<tier>
    # Traits are t-<trait>-<tier>
    filter_string = ""

    for i in range(1, len(filter_list)):
        if filter_list[i][1] in champion_mapping:
            champion = filter_list[i][1]
            filter_string += f"u-{champion_mapping[champion]}"
            if i + 1 < len(filter_list) and 'champion_tier' not in filter_list[i+1][0]:
                filter_string += f"-0/"
            if i + 1 == len(filter_list):
                filter_string += f"-0/"
        elif 'champion_tier' in filter_list[i][0]:
            champion_tier = filter_list[i][1]
            filter_string += f"-{champion_tier}/"
        else:
            filter_name = filter_list[i][1]
            filter_string += f"t-{trait_mapping[filter_name]}"

    url = (base_url + filter_string).rstrip('/')
    response = requests.get(url)
    response_json = response.json()
    filtered_list = _post_process_champion(response_json['units'], top_n=10)
    return _to_string(filtered_list)

def get_trait_data(filter_list):
    # Each filter is a champion or trait with a tier
    # Champions are u-<champion>-<tier>
    # Traits are t-<trait>-<tier>
    filter_string = ""
    for i in range(1, len(filter_list)):
        
        if filter_list[i][1] in champion_mapping:
            champion = filter_list[i][1]
            filter_string += f"u-{champion_mapping[champion]}"
        elif 'champion_tier' in filter_list[i][0]:
            champion_tier = filter_list[i][1]
            filter_string += f"-{champion_tier}/"
        else:
            filter_name = filter_list[i][1]
            filter_string += f"t-{trait_mapping[filter_name]}/"

    url = (base_url + filter_string).rstrip('/')
    response = requests.get(url)
    response_json = response.json()
    filtered_list = _post_process_trait(response_json['traits'], top_n=10)
    return _to_string(filtered_list)
