import rhyming
import math
import collections
from nltk.corpus import cmudict

class LWord:
    def get_word(self):
        return self.l_word
    def get_pron(self):
        return self.l_pron
    def check_rhyme(self,word):
        if self.l_word:
            strength = rhyming.rhymes(self.l_word,word)
            strength = int(strength)
            if strength:
                print str(self.l_word) + " rhymes with " + str(word)
                self.rhyme_list[strength].append(word)
                return True
        return False
    def rhyming_words(self):
        return self.rhyme_list
    def print_rhyming_words(self):
        print "Rhymes for word " + str(self.l_word) + " :"
        for r in self.rhyme_list:
            print r
            print self.rhyme_list[r]
    def __init__(self,word):
        self.rhyme_list = collections.defaultdict(list)
        self.l_word = word
        self.l_pron = rhyming.get_pron(word)
        self.last_syl = rhyming.last_syllable(self.l_pron)
    def last_syllable(self):
        return self.l_pron[self.last_syl:]

test1 = LWord("bash")
test2 = LWord("ababa")
test3 = LWord("sale")
test4 = LWord("blare")
#print "Rhymes with"
count = 0
for i in cmudict.entries()[1:200]:
    count = count + 1
    print count
    print i[0]
    test1.check_rhyme(i[0])
    test2.check_rhyme(i[0])
    test3.check_rhyme(i[0])
    test4.check_rhyme(i[0])

test4.print_rhyming_words()
