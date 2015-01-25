
# Based on the stack overflow 2nd order markov chain text generator
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
        self.quads_cache = {}
        self.words = words_list
        self.word_size = len(self.words)
        self.database()
        self.DEBUG_MODE = True

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

    def quads(self):
        if len(self.words) < 4:
            return
            
        for i in range(len(self.words) - 4):
            yield (self.words[i], self.words[i+1], self.words[i+2], self.words[i+3])


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

        for w1, w2, w3, w4 in self.quads():
            key = (w1, w2, w3)
            if key in self.quads_cache:
                self.quads_cache[key].append(w4)
            else:
                self.quads_cache[key] = [w4]

    def verify_key(self, key, cache, min_values):
        # Decide whether the generator is sampled enough for the given key
        # ie the value exists and there's a good variety of values for that key
        values = cache.get(key)
        if values:
            if len(values) >= min_values:
                return True
        else:
            return False


    def generate_markov_text(self, length=25, seed_suggestion=None):
        seed = random.randint(0, self.word_size-3)
        if seed_suggestion == None:
            seed_word, next_word = self.words[seed], self.words[seed+1]
        else:
            seed_word = seed_suggestion
            next_word = random.choice(self.doubles_cache[(seed_word)])

        w1, w2 = seed_word, next_word
        if self.triples_cache.get((w1, w2)):
            w3 = random.choice(self.triples_cache[(w1, w2)])
        else:
            w3 = random.choice(self.doubles_cache[(w2)])


        gen_words = []
        quad_count = 0
        trip_count = 0
        doub_count = 0

        for i in xrange(length):
            gen_words.append(w1)

            if self.verify_key((w1, w2, w3), self.quads_cache, 1):
                w1, w2, w3 = w2, w3, random.choice(self.quads_cache[(w1, w2, w3)])
                quad_count = quad_count + 1

            elif self.verify_key((w1, w2), self.triples_cache, 1):
                # If quadruple is unavailable, try a triple
                w1, w2, w3 = w2, w3, random.choice(self.triples_cache[(w1,w2)])
                trip_count = trip_count + 1

            elif self.doubles_cache.get((w3)):
                # If triple is unavailable
                w1, w2, w3 = w2, w3, random.choice(self.doubles_cache[(w2)])
                doub_count = doub_count + 1
            else:
                # Handle case in which we have no sampling on the key 
                pass

        gen_words.append(w2)
        gen_words.append(w3)
        if self.DEBUG_MODE:
            print("Double Count: %d" % doub_count)
            print("Triple Count: %d" % trip_count)
            print("Quad Count: %d" % quad_count)
        return ' '.join(gen_words)


