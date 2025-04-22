from src.tactics_simple_api import get_champion_data, get_trait_data

print(get_champion_data([{"filter": "Garen", "tier": 2}, {"filter": "Divinicorp", "tier": 5}]))
print("--------------------------------")
print(get_trait_data([{"filter": "Garen", "tier": 2}, {"filter": "Divinicorp", "tier": 5}]))
