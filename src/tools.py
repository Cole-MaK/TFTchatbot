import json
import os

path_to_champion_info = os.path.join(".", "jsoninfo_keys", "champion_info_clean.json")

class Tool():
    def champion_info(champion):
        if not os.path.exists(path_to_champion_info):
            raise FileNotFoundError(f"Champion info file not found at {path_to_champion_info}")
        
        try:
            with open(path_to_champion_info, "r") as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON file: {e}")
        
        return data.get(champion)