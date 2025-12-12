import tkinter as tk
from getData import getData, WORDS_FILE, POS_FILE
from makeBigram import BigramTrainer, BIGRAM_PROB_FILE
from makeLetterProb import makeLettersProb, LETTER_BIGRAM_PROB_FILE
import Predictor

class MainApp():

    def __init__(self):

        #Welcome + file creation
        if(self.welcome() == True):self.file_creation()

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

        #3 Create Letter-bigram File
        print(f"Creating letter-bigrams")
        makeLettersProb(WORDS_FILE)
        print(f"Letter-bigrams stored to {LETTER_BIGRAM_PROB_FILE}")
        
        

    def suggest_words(self):
        current_entry = self.text_input.get()
        print(current_entry)
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


if __name__ == "__main__":
        app = MainApp()