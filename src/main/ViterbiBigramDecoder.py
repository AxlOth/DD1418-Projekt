from Key import Key
import math
import sys
import numpy as np
import codecs
import argparse

"""
This file is part of the computer assignments for the course DD1418 at KTH.
"""

class ViterbiBigramDecoder(object):
    """
    This class implements Viterbi decoding using bigram probabilities in order
    to correct keystroke errors.
    """
    def init_a(self, filename):
        """
        Reads the bigram probabilities (the 'A' matrix) from a file.
        """
        with codecs.open(filename, 'r', 'utf-8') as f:
            for line in f:
                i, j, d = [func(x) for func, x in zip([int, int, float], line.strip().split(' '))]
                self.a[i][j] = d


    # ------------------------------------------------------


    def init_b(self):
        """
        Initializes the observation probabilities (the 'B' matrix).
        """
        for i in range(Key.NUMBER_OF_CHARS):
            cs = Key.neighbour[i]

            # Initialize all log-probabilities to some small value.
            for j in range(Key.NUMBER_OF_CHARS):
                self.b[i][j] = -float("inf")

            # All neighbouring keys are assigned the probability 0.1
            for j in range(len(cs)):
                self.b[i][Key.char_to_index(cs[j])] = math.log( 0.1 )

            # The remainder of the probability mass is given to the correct key.
            self.b[i][i] = math.log((10 - len(cs))/10.0)


    # ------------------------------------------------------



    def viterbi(self, s):
        """
        Performs the Viterbi decoding and returns the most likely
        string.
        """
        # First turn chars to integers, so that 'a' is represented by 0,
        # 'b' by 1, and so on.
        index = [Key.char_to_index(x) for x in s]

        # The Viterbi matrices
        self.v = np.zeros((len(s), Key.NUMBER_OF_CHARS))
        self.v[:,:] = -float("inf")
        self.backptr = np.zeros((len(s), Key.NUMBER_OF_CHARS), dtype='int')

        # Initialization
        self.backptr[0,:] = Key.START_END
        self.v[0,:] = self.a[Key.START_END,:] + self.b[index[0],:]

        # print("b")
        # print(self.b[index[0],:])
        # print("a")
        # print(self.a[Key.START_END,:])
        # print("v")
        # print(self.v[0,:])

        # Induction step
        for i in range(1,len(s)):
            
            for j in range(0,Key.NUMBER_OF_CHARS):
                currmax = -float("inf")
            
                for k in range(0,Key.NUMBER_OF_CHARS):  
                
                    # if (self.v[i-1,j] != -float("inf")):
                    #     print(self.v[i-1,j])

                    calc_val = self.v[i-1,k] + self.a[k,j] + self.b[j,index[i]]
                    # print("v", self.v[i-1,j])
                    # print("a", self.a[k,j])
                    # print("b", self.b[j,index[i]])
                    # print("calc_val is", calc_val)
                    currmax = max(calc_val, currmax)

                    if (calc_val == currmax):
                        # print("backptr is",k)
                        self.backptr[i][j] = k
    
                self.v[i][j] = currmax
        bestpathprob = np.max(self.v[i,:])
        bestpathpointer = np.argmax(self.v[i,:])

        res = ''
        current_index = len(s)-1
        while(current_index >= 0):
            # print(Key.index_to_char(bestpathpointer))
            res = Key.index_to_char(bestpathpointer) + res
            bestpathpointer = self.backptr[current_index, bestpathpointer]
            current_index -= 1
            

        # Finally return the result

        # REPLACE THE LINE BELOW WITH YOUR CODE

        return res


    # ------------------------------------------------------



    def __init__(self, filename=None):
        """
        Constructor: Initializes the A and B matrices.
        """
        # The trellis used for Viterbi decoding. The first index is the time step.
        self.v = None

        # The bigram stats.
        self.a = np.zeros((Key.NUMBER_OF_CHARS, Key.NUMBER_OF_CHARS))

        # The observation matrix.
        self.b = np.zeros((Key.NUMBER_OF_CHARS, Key.NUMBER_OF_CHARS))

        # Pointers to retrieve the topmost hypothesis.
        backptr = None

        if filename: self.init_a(filename)
        self.init_b()

        # print(self.b)



    # ------------------------------------------------------


def main():

    parser = argparse.ArgumentParser(description='ViterbiBigramDecoder')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file', '-f', type=str, help='decode the contents of a file')
    group.add_argument('--string', '-s', type=str, help='decode a string')
    parser.add_argument('--probs', '-p', type=str,  required=True, help='bigram probabilities file')

    arguments = parser.parse_args()

    if arguments.file:
        with codecs.open(arguments.file, 'r', 'utf-8') as f:
            s1 = f.read().replace('\n', ' ')
    elif arguments.string:
        s1 = arguments.string
    s1 = s1.replace('\r', '')
    
    # Give the filename of the bigram probabilities as a command line argument
    d = ViterbiBigramDecoder(arguments.probs)

    # Append an extra "END" symbol to the input string, to indicate end of sentence. 
    result = d.viterbi(s1 + Key.index_to_char(Key.START_END))

    print(result)


if __name__ == "__main__":
    main()
