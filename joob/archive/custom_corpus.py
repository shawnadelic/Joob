# Make sure that custom corpora are included in directory
import os
import os.path

import nltk.data
from nltk.corpus import PlaintextCorpusReader

path = os.path.expanduser('~/nltk_data')
if not os.path.exists(path):
    os.mkdir(path)
os.path.exists(path)

home_root = os.path.expanduser('~')
corpus_directory = '/nltk_data/corpora/beatles/'
numbers = range(1, 300)

if path not in nltk.data.path:
    print "Corpus path not found"
else:
    beatles_corpus = PlaintextCorpusReader( home_root + corpus_directory , '.*' )

'''def beatles_corpus.sents(self, fileids=None):
    """
    :return: the given file(s) as a list of
        sentences or utterances, each encoded as a list of word
        strings.
    :rtype: list(list(str))
    """
    if self._sent_tokenizer is None:
        raise ValueError('No sentence tokenizer for this corpus')

    return concat([self.CorpusView(path, self._read_sent_block, encoding=enc)
                 for (path, enc, fileid)
                 in self.abspaths(fileids, True, True)])
'''
k = 0
custom_corpus = nltk.Text(beatles_corpus.words())
for i in beatles_corpus.paras():
    # Iterate through songs, printing out contents
    #print "Song # " + str( k )
    k += 1
    l = 0
    while l < len(i):
        #print "Line " + str(l)
        #print i[l]
        l += 1
    #for j in i:
        #print j[0]

#new_song = custom_corpus.generate(100)
