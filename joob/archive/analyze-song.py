# Import NLTK and relevant corpora
import sys

import nltk
from nltk.corpus import cmudict as cmu
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize, wordpunct_tokenize

import custom_corpus
from rhymes import rhymes


def tag_rhyme( line1, line2 ):
    print "Rhyme score for \"" + line1 + "\" and \"" + line2 + "\" is " + str(rhymes(line1,line2))

def read_song( song_file ):
    song = open( song_file )
    title = song.readline().rstrip()
    song_line = []
    all_lyrics = ""

    for line in song:
        song_line.append( line.rstrip() )
        all_lyrics = all_lyrics + line.rstrip() + " "

    tokens = [wordpunct_tokenize(s.lower()) for s in song_line]
    #for t in tokens:
    #    print t
    punct = set(['.',',','!','?',':',';','(',')'])
    filtered = [[w for w in t if w not in punct] for t in tokens]
    print "Filtered"
    print filtered
    last = [ line [ len(line) - 1 ] for line in filtered ]

    '''for row in last:
        print "Word: " + str(row)
        for col in last:
            if rhymes(row,col):
                print "Yes, " + row + " and " + col + " rhyme. Rhyme score:" + str(rhymes(row,col))
        print ("\n")'''

    print "wordpunct_tokenize"
    #print type(wordpunct_tokenize(all_lyrics))[0]
    
    tokenized_lyrics = nltk.Text(filtered)

    #freq_dist = nltk.FreqDist(last)

    print tokenized_lyrics

    return

combined_lyrics = []

for x in range (1, 20):
    file_name = "/home/shawn/nltk_data/corpora/beatles/" + str(x).zfill(3) + ".txt"
    read_song( file_name )
    #combined_lyrics = combined_lyrics + read_song( file_name )

#print combined_lyrics

tokenized_lyrics = nltk.Text( combined_lyrics )

#print tokenized_lyrics.tokens()

#print tokenized_lyrics.generate(100)
