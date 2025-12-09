import json
import os
from glob import glob

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DATA_FOLDER = os.path.join(ROOT_DIR, "data_nyheter")

data_folder = DATA_FOLDER

json_files = glob(os.path.join(data_folder, "data_*.json"))

tokens_list = []
processed_tokens = 0

for file_path in json_files:
    with open(file_path,     "r", encoding="utf-8") as f:
        data = json.load(f)

    if(processed_tokens != 0): 
        print(processed_tokens)

    for hit in data.get("kwic", []):
        for token in hit.get("tokens", []):
            processed_tokens += 1
            word = token.get("word", "")
            pos = token.get("pos", "")
            lemma = token.get("lemma", "").strip("|")  # ta bort eventuella "|"-tecken runt lemma
            
            # Skapa ett token-objekt
            token_obj = {
                "word": word,
                "pos": pos,
                "lemma": lemma
            }
            
            # Lägg till i listan
            tokens_list.append(token_obj)

# Visa exempel på första 10 token
    
for t in tokens_list[:10]:
    print(t)