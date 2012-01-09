#!/bin/sh

import argparse
import codecs
import os

__doc = \
"""
This is a program to convert documents into the file format used by David
Blei's lda-c (and hlda-c) implementation. It generates the .dat and .vocab
files from given text files.

cf. http://www.cs.princeton.edu/~blei/lda-c/readme.txt
"""
__author__ = "Johannes Knopp <johannes@informatik.uni-mannheim.de>"

def init_parser():
    """
    Returns an argument parser configured with options for this program
    """
    parser = argparse.ArgumentParser(
            description="A program to convert documents to .dat and .vocab files"
            )

    #positional argument
    parser.add_argument("dirname", action="store",
        help="directory containing .txt files (files must be encoded in utf-8)")

    #options
    parser.add_argument("-o", "--output", action="store", dest="outdir",
            help="directory to store the resulting files")
    parser.add_argument("-e", "--extension", action="store", dest="extension",
            default=".txt",
            help="extension of the files you are looking for. Default: %(default)s")
    #TODO
    parser.add_argument("-m", "--minoccurrence", action="store",
            dest="minoccurrence", type=int, default=1,
            help="Minimum occurrences a word needs to be taken into account. NOT SUPPORTED YET")
    #TODO
    parser.add_argument("--mallet", action="store_true",
            help="convert data that exists in the format used by mallet. NOT SUPPORTED YET")

    return parser.parse_args()


def get_filenames(directory, extension):
    """
    Search for files in the directory ending in EXTENSION and return the full
    paths as a list.
    """
    all_fnames = []
    for dirpath,dirnames,filenames in os.walk(directory):
        all_fnames += [os.path.join(dirpath,f) for f in filenames if
                f.endswith(extension)]
    return all_fnames

if __name__=='__main__':

    parser = init_parser()
    
    dirname = parser.dirname

    outdir = parser.outdir if parser.outdir else parser.dirname
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    fnames = get_filenames(dirname, parser.extension)
    
