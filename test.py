from sentence_transformers import SentenceTransformer
from src.functions import get_rag_keys

import pickle
import json


files = ["champion_key.json", "synergy_key.json", "item_key.json"]
get_rag_keys(files)

