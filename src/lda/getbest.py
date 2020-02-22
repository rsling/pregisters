# -*- coding: utf-8 -*-

# This tool reads an MM corpus and creates a cowtop
# feature matrix using LDA.

import argparse
import os.path
import sys
import copy
from gensim import models, corpora
import logging
import re

def main():
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('model', help='pre-trained LDA model')
    parser.add_argument('corpus', help='corpus in Mm format')
    parser.add_argument('dictionary', help='serialized Gensim dictionary')
    parser.add_argument('ids', help='file with document IDs in exact same order as in matrix')
    parser.add_argument('outprefix', help='prefix for output files')
    parser.add_argument('num_docs', type=int, help='number of top documents per topic')
    parser.add_argument('--matrix', help='specifiy a matrix already transformed in COW format (ignore corpus, dictionary)')
    parser.add_argument('--erase', action='store_true', help="erase outout files if present")
    args = parser.parse_args()

    # Sanity-check num_docs.
    if args.num_docs < 1:
        sys.exit('Number of docs must be greater or equal to 1.')
    
    # Check input files.
    if args.matrix:
        infiles = [args.matrix]
    else:
        infiles = [args.model, args.dictionary, args.ids]

    for fn in infiles:
        if not os.path.exists(fn):
            sys.exit("Input file does not exist: " + fn)

    # Build output file names.
    fn_out = args.outprefix + ".csv"

    # Check (potentially erase) output files.
    outfiles = [fn_out]
    for fn in outfiles:
        if fn is not None and os.path.exists(fn):
            if args.erase:
                try:
                    os.remove(fn)
                except:
                    sys.exit("Cannot delete pre-existing output file: " + fn)
            else:
                sys.exit("Output file already exists: " + fn)

    # Open output file.
    h_out = open(fn_out, 'w')

   
    if args.matrix:
        logging.info('Trying to recreate ALREADY TRANSFORMED matrix…')
        matrix = []
        with open(args.matrix, 'r') as h_matrix:
            for l in h_matrix:
                fs = [(lambda t: (int(t[0]),float(t[1])))(tuple(tup.split(' '))) for tup in l.strip().split('\t')[1:]]
                matrix.append(fs)
    else:
        # Load model and dictionary.
        dictionary = corpora.dictionary.Dictionary.load(args.dictionary)
        corpus = corpora.MmCorpus(args.corpus)

    model = models.LdaModel.load(args.model, mmap='r')

    logging.info('Loading document IDs.')
    ids = []
    with open(args.ids, 'r') as h:
        for l in h:
            ids.append(re.sub('# ', '', l.strip()))

    if args.matrix:
        num_corp_docs = len(matrix)
    else:
        num_corp_docs = len(corpus)
    
    logging.info('Found {} corpus documents and {} document IDs.'.format(num_corp_docs, len(ids)))
    if not num_corp_docs == len(ids):
        raise Exception('Number of corpus documents and IDs doesn''t match.')

    if not args.matrix:
        # Transform corpus by LDA model and add IDs.
        logging.info('Transforming corpus using model…')
        matrix = model[corpus]


    if args.matrix:
        logging.info('Joining document IDs… Fast because of pre-transformed matrix…')
    else:
        logging.info('Joining document IDs… Takes a while because no pre-transformed matrix used…')
    
    id_matrix = zip(ids, matrix)
    # id_matrix = zip(ids[0:999], matrix[0:999])

    logging.info('Iterating over {} topics in model…'.format(model.num_topics))
    for i in range(model.num_topics):
        logging.info('TOPIC {}…'.format(i))
        tops = sorted(id_matrix, reverse=True, key=lambda d: abs(dict(d[1]).get(i, 0.0)))
        h_out.write('{}\t'.format(i))
        h_out.write('\t'.join([x+':'+str(dict(y)[i]) for x,y in tops[0:args.num_docs-1]]))
        h_out.write('\n')

    h_out.close()

if __name__ == "__main__":
    main()


