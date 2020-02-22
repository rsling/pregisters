# -*- coding: utf-8 -*-

import argparse
import os.path
import sys
import copy
from gensim import models, corpora

FEATS = 1631

def n_times(v,n):
    for i in range(n):
        yield v

def main():

    # Read dict.

    d = []
    with open ("colnames.txt", "r") as h:
        for l in h:
            d.append(l.strip())
    if not len(d) == FEATS:
        raise Exception('Headers wrong length: ' + str(len(d)))
    else:
        print("Headers loaded.")

    # Create corpus.
    h_out = open("corpusrex.txt", "w")

    # Read corpus = a list of lists of tuples.
    c = []
    i = 0
    with open ("ft_selection.csv", "r") as h:
        for l in h:
            fs = l.strip().split('\t')
            if not len(fs) == FEATS + 1:
                raise Exception('Array has wrong length: ' + str(len(fs)) + ' in ' + fs[0] )

            # Write doc id as comment.
            h_out.write("# " + fs[0] + "\n")
            
            # Write the raw features n times.
            doc = [[e] * int(t) for e, t in zip(d, fs[1:])]
            h_out.write(" ".join([e for sl in doc for e in sl] + ["\n"]))

            i = i + 1
            if i % 1000 == 0:
                print(" ".join(["Documents read:", str(i)]))

    h_out.close()


if __name__ == "__main__":
    main()

