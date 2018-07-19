"""This module contains a code example related to

Think Python, 2nd Edition
by Allen Downey
http://thinkpython2.com

Copyright 2015 Allen Downey

License: http://creativecommons.org/licenses/by/4.0/
"""

from __future__ import print_function, division

import sys
import string
import random

class Markov:
  
  def __init__(self):
    self.suffix_map = {}  # map from prefixes to a list of suffixes
    self.prefix = ()      # current tuple of words

  def process_file(self, filename, order=2):
    """Reads a file and performs Markov analysis.

    filename: string
    order: integer number of words in the prefix

    returns: map from prefix to list of possible suffixes.
    """
    fp = open(filename)
    self.skip_gutenberg_header(fp)

    for line in fp:
      for word in line.rstrip().split():
        self.process_word(word, order)

    #print(">>>DEBUG the suffix map")
    #i = 0
    #for k,v in self.suffix_map.items():
    #  print("key is {}, value is {}".format(k, v))
    #  i += 1
    #  if i > 10:
    #    break

  def skip_gutenberg_header(self, fp):
    """Reads from fp until it finds the line that ends the header.

    fp: open file object
    """
    for line in fp:
      if line.startswith('*END*THE SMALL PRINT!'):
        break

  def process_word(self, word, order=2):
    """Processes each word.

    word: string
    order: integer

    During the first few iterations, all we do is store up the words; 
    after that we start adding entries to the dictionary.
    """
    if len(self.prefix) < order:
      self.prefix += (word,)
      return

    try:
      self.suffix_map[self.prefix].append(word)
    except KeyError:
      # if there is no entry for this prefix, make one
      self.suffix_map[self.prefix] = [word]

    self.prefix = self.shift(self.prefix, word)

  def random_text(self, n=100):
    """Generates random wordsfrom the analyzed text.

    Starts with a random prefix from the dictionary.

    n: number of words to generate
    """
    # choose a random prefix (not weighted by frequency)
    start = random.choice(list(self.suffix_map.keys()))
    #print(">>DEBUG | start is", start)
    
    for i in range(n):
      #print(">> DEBUG | i is", n)
      suffixes = self.suffix_map.get(start, None)
      #print(">> DEBUG | suffixes is", suffixes)
      if suffixes == None:
        # if the start isn't in map, we got to the end of the
        # original text, so we have to start again.
        #print(">> DEBUG | start isn't in map")
        random_text(n-i)
        return

      # choose a random suffix
      word = random.choice(suffixes)
      #print(">> DEBUG | word is", word)
      print(word, end=' ')
      start = self.shift(start, word)


  def shift(self, t, word):
    """Forms a new tuple by removing the head and adding word to the tail.

    t: tuple of strings
    word: string

    Returns: tuple of strings
    """
    return t[1:] + (word,)

if __name__ == '__main__':
  filename = 'emma.txt'
  n = 10
  markov = Markov()

  markov.process_file(filename)
  markov.random_text(n)
  print()