
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

trait_mapping = {'Overlord': 'TFT14_Overlord',
 'Street Demon': 'TFT14_StreetDemon',
 'Soul Killer': 'TFT14_ViegoUniqueTrait',
 'Syndicate': 'TFT14_Mob',
 'Techie': 'TFT14_Techie',
 'Anima Squad': 'TFT14_AnimaSquad',
 'BoomBot': 'TFT14_BallisTek',
 'Virus': 'TFT14_Virus',
 'Strategist': 'TFT14_Controller',
 'Executioner': 'TFT14_Cutter',
 'Marksman': 'TFT14_Marksman',
 'Bastion': 'TFT14_Armorclad',
 'Exotech': 'TFT14_EdgeRunner',
 'A.M.P.': 'TFT14_Supercharge',
 'Nitro': 'TFT14_HotRod',
 'Cyberboss': 'TFT14_Cyberboss',
 'Vanguard': 'TFT14_Vanguard',
 'Divinicorp': 'TFT14_Divinicorp',
 'Dynamo': 'TFT14_Thirsty',
 'Rapidfire': 'TFT14_Swift',
 'Cypher': 'TFT14_Suits',
 'Slayer': 'TFT14_Strong',
 'Golden Ox': 'TFT14_Immortal',
 'God of the Net': 'TFT14_Netgod',
 'Bruiser': 'TFT14_Bruiser'}
champion_mapping = {'Varus': 'TFT14_Varus',
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
        })

    # Sort by count
    output.sort(key=lambda x: x["count"], reverse=True)
    return output[:top_n]

def _post_process_trait(data, top_n=10):
    # Sort by win rate
    output = []
    for row in data:
        # TODO: add tier to the trait
        name = row[0]
        output.append({
            "name": trait_mapping_reverse[name] + " tier " + str(row[1]),
            "count": row[2]["count"],
            "win_rate": round(row[2]["won"] / row[2]["count"], 2),
            "top_4_rate": round(row[2]["top4"] / row[2]["count"], 2),
            "average_placement": round(row[2]["place"] / row[2]["count"], 2),
        })

    # Sort by count
    output.sort(key=lambda x: x["count"], reverse=True)
    return output[:top_n]

def _to_string(data):
    # TODO: can optimize this format
    output = "Name (number of games) - win rate - top 4 rate - average placement\n"
    for item in data:
        output += f"{item['name']} ({item['count']}) - {item['win_rate']} - {item['top_4_rate']} - {item['average_placement']}\n"
    return output

def get_champion_data(filter_list):
    # Each filter is a champion or trait with a tier
    # Champions are u-<champion>-<tier>
    # Traits are t-<trait>-<tier>
    filter_string = ""
    for filter in filter_list:

        filter_name = filter["filter"]
        filter_tier = filter["tier"]
        
        if filter_name in champion_mapping:
            filter_string += f"u-{champion_mapping[filter_name]}-{filter_tier}/"
        elif filter_name in trait_mapping:
            filter_string += f"t-{trait_mapping[filter_name]}-{filter_tier}/"
    
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
    for filter in filter_list:
        
        filter_name = filter["filter"]
        filter_tier = filter["tier"]
        
        if filter_name in champion_mapping:
            filter_string += f"u-{champion_mapping[filter_name]}-{filter_tier}/"
        elif filter_name in trait_mapping:
            filter_string += f"t-{trait_mapping[filter_name]}-{filter_tier}/"
    url = (base_url + filter_string).rstrip('/')
    response = requests.get(url)
    response_json = response.json()
    filtered_list = _post_process_trait(response_json['traits'], top_n=10)
    return _to_string(filtered_list)
