"""
This file is part of the computer assignments for the course DD1418 at KTH.
"""

class Key:

    # All the letters on our keyboard
    letter = [chr(x) for x in range(ord('a'), ord('z')+1)] + ['å', 'ä', 'ö']

    # The START_END symbol is used to represent space, as well as beginning and end of line.
    START_END = len(letter)

    # This array encodes the topology of the keyboard.
    neighbour = (
        ('q', 'w', 's', 'z'), # a
        ('v', 'g', 'h', 'n'), # b
        ('x', 'd', 'f', 'v'), # c
        ('x', 's', 'e', 'r', 'f', 'c'), # d
        ('w', 's', 'd', 'r'), # e
        ('d', 'r', 't', 'g', 'v', 'c'), # f
        ('f', 't', 'y', 'h', 'b', 'v'), # g
        ('g', 'y', 'u', 'j', 'n', 'b'), # h
        ('u', 'j', 'k', 'o'), # i
        ('h', 'u', 'i', 'k', 'm', 'n'), # j
        ('m', 'j', 'i', 'o', 'l'), # k
        ('k', 'o', 'p', 'ö'), # l
        ('n', 'j', 'k'), # m
        ('b', 'h', 'j', 'm'), # n
        ('i', 'k', 'l', 'p'), # o
        ('o', 'l', 'ö', 'å'), # p
        ('w', 'a'), # q
        ('e', 'd', 'f', 't'), # r
        ('a', 'w', 'e', 'd', 'x', 'z'), # s
        ('r', 'f', 'g', 'y'), # t
        ('y', 'h', 'j', 'i'), # u
        ('c', 'f', 'g', 'b'), # v
        ('q', 'a', 's', 'e'), # w
        ('z', 's', 'd', 'c'), # x
        ('t', 'g', 'h', 'u'), # y
        ('x', 's', 'a'), # z
        ('p', 'ä'), # å
        ('å', 'ö'), # ä
        ('l', 'p', 'å', 'ä'), # ö
        () # Blank
    )

    NUMBER_OF_CHARS = len(neighbour)

    @staticmethod
    def char_to_index(c):
        try:
            return Key.letter.index(c)
        except ValueError: # Return the START_END symbol for all symbols outside the a-ö interval.
            return Key.START_END

    @staticmethod
    def index_to_char(i):
        if i == Key.START_END:
            return ' '
        if i < Key.NUMBER_OF_CHARS - 1:
            return Key.letter[i]
        # This shouldn't happen
        return 0

    @staticmethod
    def whitespace(c):
        return c.isspace()
