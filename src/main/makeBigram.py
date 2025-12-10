#  -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
import argparse
import re
import os
from collections import defaultdict
import codecs

"""
This file is part of the computer assignments for the course DD1418 at KTH. 
"""
BIGRAM_PROB_FILE = "bigrams.txt"

class BigramTrainer(object):
    """
    This class constructs a bigram language model from a corpus.
    """

    def process_files(self, filename):
        with codecs.open(filename, 'r', 'utf-8') as f:
            text = f.read().encode('utf-8').decode().lower()
        self.tokens = re.findall(r"[\w'-]+|[\".,!?;]", text)
        print( len(self.tokens) )
        for token in self.tokens:
            self.process_token(token)


    def process_token(self, token):
        """
        Processes one word in the training corpus, and adjusts the unigram and
        bigram counts.

        :param token: The current word to be processed.
        """

        token = str(token)

        if not token in self.index:
            token_index = len(self.word)
            self.index[token] = token_index
            self.word[token_index] = token
            self.unique_words += 1
        else:
            token_index = self.index[token]
        
        self.unigram_count[token_index] += 1
        self.total_words += 1
        
        if self.last_index != -1:
            self.bigram_count[self.last_index][token_index] += 1

        self.last_index = token_index



    def stats(self):
        """
        Creates a list of rows to print of the language model.
        """
        rows_to_print = []

        rows_to_print.append(f"{self.unique_words} {self.total_words}")
        for word, i in self.index.items():
            rows_to_print.append(f"{i} {word} {self.unigram_count[i]}")

        for i, words in self.bigram_count.items():
            for j, count in words.items():

                # print("i,j: ",i,j)

                rows_to_print.append(f"{i} {j} {math.log(count / self.unigram_count[i]):.15f}")

        rows_to_print.append('-1')

        return rows_to_print

    def __init__(self):
        """
        Constructor. Processes the file f and builds a language model
        from it.

        :param f: The training file.
        """

        # The mapping from words to identifiers.
        self.index = {}

        # The mapping from identifiers to words.
        self.word = {}

        # An array holding the unigram counts.
        self.unigram_count = defaultdict(int)

        """
        The bigram counts. Since most of these are zero (why?), we store these
        in a hashmap rather than an array to save space (and since it is impossible
        to create such a big array anyway).
        """
        self.bigram_count = defaultdict(lambda: defaultdict(int))

        # The identifier of the previous word processed.
        self.last_index = -1

        # Number of unique words (word forms) in the training corpus.
        self.unique_words = 0

        # The total number of words in the training corpus.
        self.total_words = 0


    def makeBigram(words_file_name):
        bigram_trainer = BigramTrainer()

        bigram_trainer.process_files(words_file_name)

        stats = bigram_trainer.stats()
        with codecs.open(BIGRAM_PROB_FILE, 'w', 'utf-8' ) as f:
            for row in stats:
                f.write(row + '\n')
