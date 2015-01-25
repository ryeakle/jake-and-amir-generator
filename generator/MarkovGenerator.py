

import random

def file_to_words(file_path):
    """
    Given a path to a file, return the words in that file.
    """
    file_handle = open(file_path)
    data = file_handle.read()
    words = data.split()
    return words


class Markov(object):

    def __init__(self, words_list):
        self.triples_cache = {}
        self.doubles_cache = {}
        self.words = words_list
        self.word_size = len(self.words)
        self.database()

    def triples(self):
        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i+1], self.words[i+2])

    def doubles(self):
        if len(self.words) < 2:
            return
            
        for i in range(len(self.words) - 1):
            yield (self.words[i], self.words[i+1])


    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.triples_cache:
                self.triples_cache[key].append(w3)
            else:
                self.triples_cache[key] = [w3]

        for w1, w2 in self.doubles():
            key = (w1)
            if key in self.doubles_cache:
                self.doubles_cache[key].append(w2)
            else:
                self.doubles_cache[key] = [w2]

    def generate_markov_text(self, length=25, seed_suggestion=None):
        seed = random.randint(0, self.word_size-3)
        if seed_suggestion == None:
            seed_word, next_word = self.words[seed], self.words[seed+1]
        else:
            seed_word = seed_suggestion
            next_word = random.choice(self.doubles_cache[(seed_word)])

        w1, w2 = seed_word, next_word
        gen_words = []
        for i in xrange(length):
            gen_words.append(w1)

            if self.triples_cache[(w1, w2)]:
                w1, w2 = w2, random.choice(self.triples_cache[(w1,w2)])
            else:
                # If triple is unavailable
                w1, w2 = w2, random.choice(self.doubles_cache[(w2)])

        gen_words.append(w2)
        return ' '.join(gen_words)


