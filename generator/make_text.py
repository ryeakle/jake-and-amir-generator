#!/usr/bin/python

# make_text.py
# Generates a plausible sounding nonsense phrase for your favorite Jake and Amir
# character!
#
# Usage: make_text.py amir
# > The Amir Bloominfeld Foundation for NOT GIVING A SHIT, founded in 1986 to
# solve the Rubik's Cube.

import MarkovGenerator
import sys

if len(sys.argv) == 2:
    #file_ = open("/Users/riley/jake-and-amir-generator/data/characters/" + sys.argv[1] + ".txt")
    file_ = open("../../data/characters/" + sys.argv[1] + ".txt")
    markov = MarkovGenerator.Markov(file_)
    print markov.generate_markov_text(100)
else:
    print "Usage: make_text.py amir"
