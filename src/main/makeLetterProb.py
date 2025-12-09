from collections import defaultdict


transitions = defaultdict(lambda: defaultdict(int))
total_counts = defaultdict(int)

with open("words.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        
        line = line.replace(" ", "").lower()

        for i in range(len(line) - 1):
            current_letter = line[i]
            next_letter = line[i + 1]

            transitions[current_letter][next_letter] += 1
            total_counts[current_letter] += 1