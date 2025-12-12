from collections import defaultdict
import math
from Key import Key  

LETTER_BIGRAM_PROB_FILE = "letterBigram.txt"

def makeLettersProb(words_file_name):
    # Step 0: Mapping letters to indices
    letters = ".abcdefghijklmnopqrstuvwxyzåäö"
    letter_to_index = {ch: i for i, ch in enumerate(letters)}
    index_to_letter = {i: ch for ch, i in letter_to_index.items()}

    # Step 1: Count letter transitions
    transitions = defaultdict(lambda: defaultdict(int))
    total_counts = defaultdict(int)

    with open(words_file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().replace(".", "").replace(" ", ".").lower()
            if not line:
                continue
            for i in range(len(line) - 1):
                current_letter = line[i]
                next_letter = line[i + 1]
                if current_letter in letter_to_index and next_letter in letter_to_index:
                    c_idx = letter_to_index[current_letter]
                    n_idx = letter_to_index[next_letter]
                    transitions[c_idx][n_idx] += 1
                    total_counts[c_idx] += 1

    # Step 2: Compute probabilities (log probabilities)
    probabilities = {}
    for letter_idx, next_letters in transitions.items():
        probabilities[letter_idx] = {}
        for next_idx, count in next_letters.items():
            probabilities[letter_idx][next_idx] = math.log(count / total_counts[letter_idx])

    # Step 3: Write to TXT file, filling missing bigrams with -inf
    with open(LETTER_BIGRAM_PROB_FILE, "w", encoding="utf-8") as f:
        for i in range(Key.NUMBER_OF_CHARS):
            for j in range(Key.NUMBER_OF_CHARS):
                prob = probabilities.get(i, {}).get(j, float('-inf'))  # -inf if no transition
                f.write(f"{i} {j} {prob}\n")
