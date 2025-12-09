import math
import argparse
import codecs
from collections import defaultdict
import random
import Bokstäver

"""
This file is part of the computer assignments for the course DD1418 at KTH.
"""

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

        # The average log-probability (= the estimation of the entropy) of the test corpus.
        # Important that it is named self.logProb for the --check flag to work
        self.logProb = 0

        # The identifier of the previous word processed in the test corpus. Is -1 if the last word was unknown.
        self.last_index = -1

        # The fraction of the probability mass given to unknown words.
        self.lambda3 = 0.000001

        # The fraction of the probability mass given to unigram probabilities.
        self.lambda2 = 0.01 - self.lambda3

        # The fraction of the probability mass given to bigram probabilities.
        self.lambda1 = 0.99

        # The number of words processed in the test corpus.
        self.test_words_processed = 0


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


                return True
        except IOError:
            print("Couldn't find bigram probabilities file {}".format(filename))
            return False

    def generate(self, last_word, written):
        """
        Generates and prints n words, starting with the word w, and following the distribution
        of the language model.
        """ 

       
        ordlista = []
        viktlista = []
        m = self.index[last_word]

        a = Bokstäver.ViterbiBigramDecoder.init_a("letterBigramProb.txt")

        applicable_words = {i: w for i, w in self.word.items() if w.startswith(written)}
        print(applicable_words)
        for j in applicable_words:
            if j in self.bigram_prob[m]:        #Kolla vilka ord som finns i bigram med det inlagda ordet
                if(written == None):
                    prob = math.exp(self.bigram_prob[m][j]) 
                else: 
                    letters_list = []
                    letters_list.append(written[len(written)-1])
                    letters_list.append(j[len(written):len(j)])
                    prob = math.exp(self.bigram_prob[m][j]) 
                    for i in range(letters_list) -1:
                        prob += math.exp(a[self.index[letters_list[i]]][self.index[letters_list[i+1]]])
                if prob > 0:
                    ordlista.append(self.word[j])           #lägg in i listan över möjliga ord med sannolikheten i viktlistan
                    viktlista.append(prob)

                        
                                 #om det inte fanns några bigram-sannolikheter slumpar man mellan alla olika med samma sannolikhet
        if ordlista == []:
                print("Tough Luck")

        if len(viktlista) > 2:
            top3_indices = [i for i, v in sorted(enumerate(viktlista), key=lambda x: x[1], reverse=True)[:3]]
            nyaord = []
            for i in top3_indices:
                nyaord.append(ordlista[i])
            print(nyaord)
        elif len(viktlista) > 1:
            top2_indices = [i for i, v in sorted(enumerate(viktlista), key=lambda x: x[1], reverse=True)[:2]]
            nyaord = []
            for i in top2_indices:
                nyaord.append(ordlista[i])
            print(nyaord)
        else:
            nyaord = ordlista[0]
            print(nyaord)


        pass

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
    generator.generate(arguments.start.strip(), "ha")

if __name__ == "__main__":
    main()
