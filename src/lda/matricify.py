# -*- coding: utf-8 -*-

import argparse
import os.path
import sys
import copy
from gensim import models, corpora


CORPUS = 'test.txt'
OUTNAME = 'test'

# CORPUS = 'corpusrex.txt'
# OUTNAME = 'precox'

class CorpusRexRaw(object):
    def __init__(self):
        self.counter = 0
    def __iter__(self):
        for line in open(CORPUS):
            if len(line) > 0 and not line[0] == '#':
                yield line.strip().split()
                self.counter = self.counter + 1
                if self.counter % 1000 == 0:
                    print("Documents read (CorpusRexRaw): " + str(self.counter))

class CorpusRex(object):
    def __init__(self, d):
        self.d = d
        self.counter = 0
    def __iter__(self):
        for line in open(CORPUS):
            if len(line) > 0 and not line[0] == '#':
                yield self.d.doc2bow(line.strip().split())
                self.counter = self.counter + 1
                if self.counter % 1000 == 0:
                    print("Documents read (CorpusRex): " + str(self.counter))

def main():

    # Create dictionary.
    c = CorpusRexRaw()
    d = corpora.Dictionary(doc for doc in c)
    d.save(OUTNAME + '.dict')
    d.save_as_text(OUTNAME + '.dict.txt')
    
    # Create BOW corpus.
    vc = CorpusRex(d)
    corpora.MmCorpus.serialize(OUTNAME + '.mm', vc)


if __name__ == "__main__":
    main()

