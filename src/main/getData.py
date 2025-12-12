import json
import os
from glob import glob


WORDS_FILE = "words.txt"
POS_FILE = "pos.txt"

def getData(data_folder_name):
    
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.dirname(os.path.dirname(SCRIPT_DIR))
    DATA_FOLDER = os.path.join(ROOT_DIR, data_folder_name)

    letters = ".abcdefghijklmnopqrstuvwxyzåäöABCDEFGHIJKLMNOPQRSTUVWXYZÅÄÖ"
    allowed = set(letters)
    allowed_single_letter_words = {"i","å", "ö",}

    data_folder = DATA_FOLDER

    json_files = glob(os.path.join(data_folder, "*.json"))

    tokens_list = []
    processed_tokens = 0
    seen_sentences = set()

    for file_path in json_files:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if(processed_tokens != 0): 
            print(processed_tokens)

        for hit in data.get("kwic", []):

            sentence = " ".join([t.get("word", "") for t in hit.get("tokens", [])])

            if sentence in seen_sentences:
                continue

            seen_sentences.add(sentence)

            for token in hit.get("tokens", []):
                processed_tokens += 1
                raw_word = token.get("word", "")

                # Specialfall: behåll punkt exakt som ord
                if raw_word.strip() == ".":
                    clean_word = "."
                else:
                    clean_word = "".join(ch for ch in raw_word if ch in allowed)

                # Filtrera bort icke-godkända enbokstavsord (gäller inte punkt)
                if len(clean_word) == 1 and clean_word.lower() not in allowed_single_letter_words and clean_word != ".":
                    continue
                pos = token.get("pos", "")
                lemma = token.get("lemma", "").strip("|")  # ta bort eventuella "|"-tecken runt lemma
                
                # Skapa ett token-objekt
                token_obj = {
                    "word": clean_word,
                    "pos": pos,
                }
                
                # Lägg till i listan
                tokens_list.append(token_obj)


    with open(WORDS_FILE, "w", encoding="utf-8") as f:
        prev_token = ""

        for token_obj in tokens_list:
            if(token_obj["word"] != "." and prev_token != "."):
                f.write(" ")
            f.write(token_obj["word"])
            if(token_obj["word"] == "."):
                    f.write("\n")

    with open(POS_FILE, "w", encoding="utf-8") as f:
        prev_token = ""
        for token_obj in tokens_list:
            if(token_obj["word"] != "." and prev_token != "."):
                f.write(" ")
            f.write(token_obj["pos"])
            if(token_obj["word"] == "."):
                    f.write("\n")