import sys

from nltk.corpus import cmudict as cmu


def has_vowel(pron):
    matches = 0
    while pron[-(matches+1):] and matches < len(pron):
        if (is_vowel(pron[-(matches+1)])):
            return True
        matches += 1
    return False

def is_vowel(syl):
    if syl[-1].isdigit():
        return True
    else:
        return False

def last_vowel(pron):
    if pron:
        index = -1
        for syl in reversed(pron):
            if is_vowel(syl):
                return pron[index]
            index -= 1
    return None

def last_syllable(pron):
    if pron:
        index = -1
        for syl in reversed(pron):
            if is_vowel(syl):
                return index
            index -= 1
    return None

def get_pron(word):
    for entry in cmu.entries():
        if entry[0] == word:
            return entry[1]
    return None

def similar_spelling( word1, word2 ):
    i = 0
    while word1[(-1-i):] == word2[(-1-i):]:
        i += 1
    return i

def rhymes(word1, word2):
    matches = 0
    word1_pron = get_pron(word1)
    word2_pron = get_pron(word2)

    # If one is not found in the CMU dictionary, check spelling for similar spelling
    if ( not( word1_pron ) or not(word2_pron) ):
        return similar_spelling( word1, word2 ) * 0.5

    # Otherwise, count the number of matching syllables
    while word1_pron[-(matches+1):] == word2_pron[-(matches+1):] and matches < len(word1_pron):
        matches += 1

    word_end = word1_pron[-(matches):]

    if ( ( matches <= 1 ) or not (has_vowel(word_end))):
        #print word1 + " does not rhyme with " + word2 + " with a rhyme strength of " + str(0)
        return 0.0
    else:
        print "Has vowel" + str(has_vowel( word_end))
        print "Matches" + str(matches)
        print str(word1_pron) + " rhymes with " + str(word2_pron) + " with a rhyme strength of " + str(matches)
        return float(matches)

if __name__ == "__main__": 
    print str(rhymes("fly","by"))
