import math
import argparse
import codecs
from collections import defaultdict
import random
import Bokstäver

class Generator(object) :
    """
    This class generates words from a language model.
    """
    def __init__(self):
    
        # The mapping from words to identifiers.
        self.index = {}

        # The mapping from identifiers to words.
        self.word = {}

        # An array holding the unigram counts.
        self.unigram_count = {}

        # The bigram log-probabilities.
        self.bigram_prob = defaultdict(dict)

        # Number of unique words (word forms) in the training corpus.
        self.unique_words = 0

        # The total number of words in the training corpus.
        self.total_words = 0




    def read_model(self,filename):
        """
        Reads the contents of the language model file into the appropriate data structures.

        :param filename: The name of the language model file.
        :return: True if the entire file could be processed, False otherwise.
        """

        try:
            with codecs.open(filename, 'r', 'utf-8') as f:
                self.unique_words, self.total_words = map(int, f.readline().strip().split(' '))     #Läser in unika ord och antal ord
                # YOUR CODE HERE

                for i in range(self.unique_words):                          #läser in alla unika ord, dess index och antal
                    a, b, c = map(str, f.readline().strip().split(' '))
                    a = int(a)
                    c = int(c)
                    self.word[a] = b
                    self.index[b] = a
                    self.unigram_count[a] = c
                
                for rad in f:
                    rad = rad.strip()
                    if rad == "-1":         #sista raden ska skippas
                        continue
                    else:
                        delar = rad.split()     #Läser in alla bigram-sannolikheter och lägger in dessa i dictionaryt
                        x, y, z = delar
                        x = int(x)
                        y = int(y)
                        z = float(z)
                        self.bigram_prob[x][y] = z
                
                for i in range(self.unique_words):
                    self.bigram_prob[i][13] = -100000000000
                self.unigram_count[13] = 0


                return True
        except IOError:
            print("Couldn't find bigram probabilities file {}".format(filename))
            return False

    def generate(self, last_word, written):
       
        # Init
        ordlista = []
        viktlista = []
        if(last_word != None and last_word != ""):  m = self.index.get(last_word, None)
        letters = ".abcdefghijklmnopqrstuvwxyzåäö"
        letter_to_index = {ch: i for i, ch in enumerate(letters)}
        decoder = Bokstäver.ViterbiBigramDecoder(filename="letterBigram.txt")

       
        
        if(last_word == None or last_word == "" or m == None): ordlista, viktlista = self.no_lw(ordlista, viktlista, written, decoder, letter_to_index)
        else: ordlista, viktlista = self.lw_exists(ordlista, viktlista, m, written, decoder, letter_to_index)

        
        if ordlista == []:
            for char in written:
                if(char not in letters): return written
            res = decoder.viterbi(written)
            if isinstance(res, list):
                res = "".join(res)
            if(last_word != None and last_word != ""):
                ordlista, viktlista = self.lw_exists(ordlista, viktlista, m, res, decoder, letter_to_index)
            else: ordlista, viktlista = self.no_lw(ordlista, viktlista, res, decoder, letter_to_index)
            if(ordlista == []):
                return written

        if len(viktlista) > 2:
            top3_indices = [i for i, v in sorted(enumerate(viktlista), key=lambda x: x[1], reverse=True)[:3]]
            nyaord = []
            for i in top3_indices:
                nyaord.append(ordlista[i])
            return nyaord
        elif len(viktlista) > 1:
            top2_indices = [i for i, v in sorted(enumerate(viktlista), key=lambda x: x[1], reverse=True)[:2]]
            nyaord = []
            for i in top2_indices:
                nyaord.append(ordlista[i])
            return nyaord
        elif len(viktlista) > 0:
            nyaord = ordlista[0]
            return nyaord


        pass

    def lw_exists(self, ordlista, viktlista, m, written, decoder, letter_to_index):
        if(written == None or written == ""): applicable_words = self.word
        else: applicable_words = {i: w for i, w in self.word.items() if w.startswith(written)}

        for idx, w in applicable_words.items():
            if idx in self.bigram_prob[m]:  
                    #Kolla vilka ord som finns i bigram med det inlagda ordet
                if(written == None or written == ""):
                    prob = self.bigram_prob[m][idx]
                else: 
                    letters_list = []
                    letters_list.append(written[-1])      
                    letters_list.extend(list(w[len(written):]))
                    prob = self.bigram_prob[m][idx]
                    for i in range(len(letters_list) -1):
                        prob += decoder.a[letter_to_index[letters_list[i]]][letter_to_index[letters_list[i + 1]]]

                ordlista.append(w)
                viktlista.append(prob)
        return(ordlista, viktlista)
    
    def no_lw(self, ordlista, viktlista, written, decoder, letter_to_index):
        if(written == None or written == ""): applicable_words = self.word
        else: applicable_words = {i: w for i, w in self.word.items() if w.startswith(written)}

        for idx, w in applicable_words.items():
            if(written == None or written == ""):
                   prob = self.unigram_count[idx]
            else:
                prob = math.log(self.unigram_count[idx] + 1)
                letters_list = [written[-1]] + list(w[len(written):])
                for i in range(len(letters_list) -1):
                    prob += decoder.a[letter_to_index[letters_list[i]]][letter_to_index[letters_list[i + 1]]]

            ordlista.append(w)
            viktlista.append(prob) 
        return(ordlista, viktlista)
    
    def is_known_word(self, word: str) -> bool:
        return word in self.index     
     
def main_temp():
    generator = Generator()
    generator.read_model("bigrams.txt")
    ordlista = generator.generate("", "a")
    print(ordlista)
    
def main():
    """
    Parse command line arguments
    """
    parser = argparse.ArgumentParser(description='BigramTester')
    parser.add_argument('--file', '-f', type=str,  required=True, help='file with language model')
    parser.add_argument('--start', '-s', type=str, required=True, help='starting word')
    parser.add_argument('--number_of_words', '-n', type=int, default=1)

    arguments = parser.parse_args()

    generator = Generator()
    generator.read_model(arguments.file.strip())
    generator.generate(arguments.start.strip(), "hzr")

if __name__ == "__main__":
    main_temp()
