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
        self.cache = {}
        self.words = words_list
        self.word_size = len(self.words)
        self.database()

    def triples(self):
        if len(self.words) < 3:
            return

        for i in range(len(self.words) - 2):
            yield (self.words[i], self.words[i+1], self.words[i+2])

    def database(self):
        for w1, w2, w3 in self.triples():
            key = (w1, w2)
            if key in self.cache:
                self.cache[key].append(w3)
            else:
                self.cache[key] = [w3]

    def generate_markov_text(self, length=25):
        seed = random.randint(0, self.word_size-3)
        seed_word, next_word = self.words[seed], self.words[seed+1]
        w1, w2 = seed_word, next_word
        gen_words = []
        for i in xrange(length):
            gen_words.append(w1)
            w1, w2 = w2, random.choice(self.cache[(w1,w2)])
        gen_words.append(w2)
        return ' '.join(gen_words)


