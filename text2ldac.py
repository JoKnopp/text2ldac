#!/bin/sh

import argparse
import codecs

__doc = \
"""
This is a program to convert documents into the file format used by David
Blei's lda-c (and hlda-c) implementation. It generates the .dat and .vocab
files from given text files.
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
    parser.add_argument("-o", "--output", action="store",
            dest="outdir",default=parser.dirname)
    #TODO
    parser.add_argument("-m", "--minoccurrence", action="store",
            dest="minoccurrence", type=int, default=1,
            help="Minimum occurrences a word needs to be taken into account")
    #TODO
    parser.add_argument("--mallet", action="store_true",
            help="convert data that exists in the format used by mallet")

    return parser.parse_args()

if __name__=='__main__':

    parser = init_parser()
    


    return
