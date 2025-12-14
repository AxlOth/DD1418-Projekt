import tkinter as tk
from getData import getData, WORDS_FILE, POS_FILE
from makeBigram import BigramTrainer, BIGRAM_PROB_FILE
import Predictor

class MainApp():

    def __init__(self):
        
        #Welcome + file creation
        if(self.welcome() == True):self.file_creation()

        # Setup generator
        self.generator = Predictor.Generator()
        self.generator.read_model(BIGRAM_PROB_FILE)

        #print(f"Evaluation score rapport: {self.evaluate('rapport_text.txt')}") 
        #Liten text
        # Med Viterbi: 0.07442748091603053, Utan Viterbi: 0.07442748091603053, 
        # Stor text
        # Med Viterbi:  0.06214915797914996, Utan Viterbi: 0.06214915797914996
        #print(f"Evaluation score rapport felstavad: {self.evaluate('rapport_text_felstavad.txt')}") 
        #Liten text
        # Med Viterbi: 0.05938697318007663, Utan Viterbi: 0.05938697318007663, 
        # Stor text
        # Med Viterbi: 0.059178743961352656, Utan Viterbi: 0.059178743961352656
        print(f"Evaluation score talspråk: {self.evaluate('nyheter_text.txt', 'nyheter_text.txt')}") 
        #Liten text
        # Med Viterbi: 0.08359133126934984, Utan Viterbi: 0.08359133126934984 
        # Stor text
        # Med Viterbi: 0.09295570079883805, Utan Viterbi: 0.09295570079883805
        #print(f"Evaluation score talspråk felstavad: {self.evaluate('talspråk_text_felstavad.txt')}")
        #Liten Text
        #Med Viterbi: 0.084375, Utan Viterbi:  0.084375, 
        # Stor text
        # 0.09336250911743253, 0.09336250911743253
        # 0.012318840579710146, 0.012318840579710146


        #Setup Tk

        self.root = tk.Tk()
        self.root.title("Word Predictor")

        # Input field
        self.text_input = tk.Entry(self.root, width=50)
        self.text_input.pack(padx=10, pady= 10)
        self.text_input.bind("<KeyRelease>", self.on_key_release)

        # Suggestions label
        self.suggestion_frame = tk.Frame(self.root)
        self.suggestion_frame.pack()

        self.suggestion_buttons = []

        for i in range(3):
            btn = tk.Button(self.suggestion_frame, text="", width=15,
                            command=lambda idx=i: self.insert_suggestion(idx))
            btn.grid(row=0, column=i, padx=5)
            self.suggestion_buttons.append(btn)

        # Start the UI
        self.root.mainloop()

    def welcome(self):
        user_input = input("Do you wish to run file creation: ")
        return user_input.strip().lower() == "yes"

    def file_creation(self):
        
        # 1 Extract and clean words from JSON files
        data_folder_name = input("Enter name of data folder:")
        if(data_folder_name == ""):
            data_folder_name = "data_nyheter"
        print(f"Begining to extract and clean words from {data_folder_name} ...")
        getData(data_folder_name)
        print(f"Saved cleaned words to {WORDS_FILE}, and POS to {POS_FILE} ")


        # 2 Create Bigram file
        print(f"Creating bigrams")
        BigramTrainer.makeBigram(WORDS_FILE)
        print(f"Bigrams stored to {BIGRAM_PROB_FILE}")
        
        

    def suggest_words(self):
        current_entry = self.text_input.get()
        if not current_entry:
            last_word = None
            written = None
        else: words = current_entry.split(" ")

        if(len(words) > 1):
            written = words[-1]
            last_word = words[-2]
        else:
             
             written = words[-1]
             last_word = None

        if current_entry == " " and current_entry[-1] == " ":  
            last_word = written
            written = None

        
        return  self.generator.generate(last_word, written)
    
    def insert_suggestion(self, index):
        """Insert selected suggestion into the input field."""
        raw_text = self.text_input.get()
        text = raw_text.rstrip()

        suggestion = self.current_suggestions[index]

        if raw_text.endswith(" "):
            if(suggestion == "."):
                new_text = text + suggestion
            else:
                new_text = raw_text + suggestion + " "
        else:
            parts = text.split(" ")
            parts[-1] = suggestion
            new_text = " ".join(parts) + " "

        # Uppdatera fältet
        self.text_input.delete(0, tk.END)
        self.text_input.insert(0, new_text)

        # Uppdatera förslag direkt
        self.on_key_release(None)

    def on_key_release(self, event):
        suggestions = self.suggest_words()
        if isinstance(suggestions, str): suggestions = [suggestions]

        self.current_suggestions = suggestions[:3]

        for i in range(3):
            if i < len(self.current_suggestions):
                self.suggestion_buttons[i].config(text=self.current_suggestions[i], state="normal")
            else:
                self.suggestion_buttons[i].config(text="", state="disabled")

    def evaluate(self, text_file_name, correctfile):

        total_chars = 0
        saved_clicks = 0

        with open(text_file_name, "r", encoding="utf-8") as f:
            text = f.read().lower()
            words = [w.strip() for w in text.split() if w.strip()]

        with open(correctfile, "r", encoding="utf-8") as m:
            textC = m.read().lower()
            wordsC = [w.strip() for w in textC.split() if w.strip()]


        last_word = None
        cache = {}
        gen = self.generator.generate  # local reference for speed

        for idx, word in enumerate(words):
            #if idx % 10 == 0 and idx > 0:
            #    print(f"Processed {idx} words...")
            correct_word = wordsC[idx]
            total_chars += len(word)
            written = ""

            for i, ch in enumerate(word):
                written += ch

                key = (last_word, written)
                if key in cache:
                    suggestions = cache[key]
                    print(suggestions)
                else:
                    suggestions = gen(last_word, written)
                    if isinstance(suggestions, str):
                        suggestions = [suggestions]
                    cache[key] = suggestions

                if correct_word in suggestions:
                    remaining = len(word) - (i + 1)
                    if remaining > 0:
                        saved_clicks += max(0, remaining - 1)
                    break
            last_word = correct_word

        if total_chars == 0:
            return 0.0

        return saved_clicks / total_chars


if __name__ == "__main__":
        app = MainApp()
        