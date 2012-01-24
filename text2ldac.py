#!/bin/sh

import argparse
import codecs
import os
import operator
import string
import sys

__doc = \
'''
This is a program to convert documents into the file format used by David
Blei's lda-c (and hlda-c) implementation. It generates the .dat and .vocab
files from given text files.

cf. http://www.cs.princeton.edu/~blei/lda-c/readme.txt
'''
__author__ = 'Johannes Knopp <johannes@informatik.uni-mannheim.de>'

def init_parser():
    '''
    Returns an argument parser configured with options for this program
    '''
    parser = argparse.ArgumentParser(
            description='A program to convert documents to .dat and .vocab files'
            )

    #positional argument
    parser.add_argument('dirname', action='store',
        help='directory containing .txt files (files must be encoded in utf-8)')

    #options
    parser.add_argument('-o', '--output', action='store', dest='outdir',
            help='directory to store the resulting files')
    parser.add_argument('-e', '--extension', action='store', dest='extension',
            default='.txt',
            help='extension of the files you are looking for. Default: %(default)s')
    #TODO minoccurrence should work for the overall occurrence
    parser.add_argument('--minoccurrence', action='store',
            dest='minoccurrence', type=int, default=1,
            help='Minimum occurrences a word needs at least once in one document to be taken into account.')
    parser.add_argument('--minlength', action='store',
            dest='minlength', type=int, default=1,
            help='Minimum length a word needs to be taken into account.')
    #stopwords
    parser.add_argument('--stopwords', action='store', dest='stopword_file',
            help='Remove the stopwords given in the stopword file (one line per stopword).')

    #TODO
    parser.add_argument('--mallet', action='store_true',
            help='convert data that exists in the format used by mallet. NOT SUPPORTED YET')

    return parser.parse_args()


def get_filenames(directory, extension):
    '''
    Search for files in the directory ending in EXTENSION and return the full
    paths as a list.
    '''
    all_fnames = []
    for dirpath,dirnames,filenames in os.walk(directory):
        all_fnames += [os.path.join(dirpath,f) for f in filenames if
                f.endswith(extension)]
    return all_fnames

if __name__=='__main__':

    parser = init_parser()

    #directory with document files
    dirname = parser.dirname
    dirname = dirname + os.sep if not dirname.endswith(os.sep) else dirname
    #directory for results
    outdir_name = parser.outdir if parser.outdir else dirname
    #prefix of the .dat and .vocab files
    basename = os.path.dirname(dirname).split('/')[-1]


    if not os.path.exists(outdir_name):
        os.mkdir(outdir_name)

    #store configuration
    config = dict()
    config['datname'] = outdir_name + basename + '.dat'
    config['vocabname'] = outdir_name + basename + '.vocab'
    config['minlength'] = parser.minlength
    config['minoccurrence'] = parser.minoccurrence
    if parser.stopword_file:
        config['stopwords'] = load_stopwords(parser.stopword_file)
    else:
        config['stopwords'] = set()

    fnames = get_filenames(dirname, parser.extension)
    dmap_file = outdir_name + basename + '.dmap'
    
