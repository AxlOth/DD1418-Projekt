import tkinter as tk
from getData import getData, WORDS_FILE, POS_FILE
from makeBigram import BigramTrainer, BIGRAM_PROB_FILE
from makeLetterProb import makeLettersProb, LETTER_BIGRAM_PROB_FILE
import Predictor

class MainApp():

    def __init__(self):
        #Run startup
        self.startup()

        # Setup generator
        self.generator = Predictor.Generator()
        self.generator.read_model(BIGRAM_PROB_FILE)

        #Setup Tk
        self.root = tk.Tk()
        self.root.title("Word Predictor")

        # Input field
        self.text_input = tk.Entry(self.root, width=50)
        self.text_input.pack(padx=10, pady= 10)
        self.text_input.bind("<KeyRelease>", self.on_key_release)

        # Suggestions label
        self.suggestions_label = tk.Label(self.root, text="", fg="blue")
        self.suggestions_label.pack()

        # Start the UI
        self.root.mainloop()


    def startup(self):
        
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

        #3 Create Letter-bigram File
        print(f"Creating letter-bigrams")
        makeLettersProb(WORDS_FILE)
        print(f"Letter-bigrams stored to {LETTER_BIGRAM_PROB_FILE}")
        
        

    def suggest_words(self):
        current_entry = self.text_input.get().strip()
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

        if self.generator.is_known_word(written):
             last_word = written
             written = None
        return  self.generator.generate(last_word, written)

    def on_key_release(self, event):
        suggestions = self.suggest_words()
        self.suggestions_label.config(text=", ".join(suggestions))

if __name__ == "__main__":
        app = MainApp()