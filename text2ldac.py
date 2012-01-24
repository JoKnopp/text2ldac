#!/bin/sh

#This file is part of text2ldac.

#text2ldac is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#text2ldac is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with text2ldac. If not, see <http://www.gnu.org/licenses/>.



import argparse
import codecs
import os
import operator
import string
import sys

__doc = \
'''
This is a program to convert documents into the file format used by David
Blei's lda-c (and hlda-c) implementation. It generates the .dat, .vocab and
.dmap files from .txt files in a given directory.

cf. http://www.cs.princeton.edu/~blei/lda-c/readme.txt
'''
__author__ = 'Johannes Knopp <johannes@informatik.uni-mannheim.de>'

def init_parser():
    '''
    Returns an argument parser configured with options for this program
    '''
    parser = argparse.ArgumentParser(
            description='A program to convert documents to .dat, .vocap and .dmap files'
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


def clean_word(word):
    '''
    returns the word in lowercase without punctuation at the start or end
    '''
    return word.rstrip(string.punctuation).lstrip(string.punctuation).lower()

def load_stopwords(stopword_filename):
    '''
    returns a set of stopwords found line by line in the stopwords file
    '''
    stopwords = set()

    with codecs.open(stopword_filename, 'r', 'utf-8') as sf:
        for line in sf:
            if len(line.split()) != 1:
                print('ignoring line with more than one stopword:\n"{0}"'.format(
                    line))
                continue
            stopwords.add(line.strip())

    return stopwords

def write_document_map_file(fnames, dmap_fname):
    """
    Save document's names in the order they were processed
    """
    with codecs.open(dmap_fname,'w','utf-8') as d_file:
        for title in fnames:
            d_file.write(title + '\n')


def generate_dat_lines_and_word_ids(fnames, config):
    dat_lines = [] #.dat file output
    word_id_dict = dict()
    used_docs = [] #needed to generate .dmap file

    for docname in fnames:
        freq_dict = dict()
        new_words = set()

        with codecs.open(docname, 'r', 'utf-8') as doc:
            for line in doc:
                for word in line.split():
                    word = clean_word(word)

                    if len(word) < config['minlength'] or word in config['stopwords']:
                        continue

                    #word occurrs for the first time
                    if not word_id_dict.has_key(word):
                        freq_dict[word] = 1
                        word_id_dict[word] = len(word_id_dict)
                        new_words.add(word)
                    #word may be in word_id_dict but not yet in freq_dict
                    else:
                        freq = freq_dict.setdefault(word, 0)
                        freq_dict[word] = freq + 1

        if len(freq_dict)==0: #did the document contribute anything?
            print('Document {0} (#{1}) seems to be empty and is ignored!'.format(
                docname,fnames.index(docname)))
            continue
        else:
            used_docs.append(docname)

        #remove words that do not reach minoccurrence
        remove_list = [word for word in freq_dict.iterkeys() if\
            freq_dict[word] < config['minoccurrence']]
        for word in remove_list:
            freq_dict.pop(word)
            #if they are new also remove them from word_id_dict
            if word in new_words:
                word_id_dict.pop(word)

        dat_line =  '' #line for the .dat file

        for word in freq_dict.iterkeys():
            dat_line += str(word_id_dict[word]) + ':' + str(freq_dict[word]) + ' '

        #last blank in dat_line is removed
        dat_lines.append(str(len(freq_dict)) + ' ' + dat_line[:-1] + '\n')

    write_document_map_file(used_docs, config['dmapname'])

    return dat_lines, word_id_dict


def generate_dat_and_vocab_files(fnames, config):

    with codecs.open(config['datname'], 'w', 'utf-8') as datfile:
        dat_lines, word_id_dict = generate_dat_lines_and_word_ids(fnames,
                config)
        datfile.writelines(dat_lines)

    #sort word_id_dict ascending by value und write the words in that
    #order to a .vocab file
    with codecs.open(config['vocabname'], 'w', 'utf-8') as vocabfile:
        for item in sorted(word_id_dict.iteritems(), key=operator.itemgetter(1)):
            vocabfile.write(item[0]+'\n')

    print('Found {0} unique words in {1} files.'.format(
        len(word_id_dict), len(fnames)))
    print('Results can be found in "{0}" and "{1}"'.format(
        config['datname'], config['vocabname']))


if __name__=='__main__':

    parser = init_parser()

    #directory with document files
    dirname = parser.dirname
    dirname = dirname + os.sep if not dirname.endswith(os.sep) else dirname
    #directory for results
    outdir_name = parser.outdir if parser.outdir else dirname
    outdir_name = outdir_name + os.sep if not outdir_name.endswith(os.sep) else outdir_name
    #prefix of the .dat and .vocab files
    basename = os.path.dirname(dirname).split('/')[-1]


    if not os.path.exists(outdir_name):
        os.mkdir(outdir_name)

    #store configuration
    config = dict()
    config['datname'] = outdir_name + basename + '.dat'
    config['vocabname'] = outdir_name + basename + '.vocab'
    config['dmapname'] = outdir_name + basename + '.dmap'
    config['minlength'] = parser.minlength
    config['minoccurrence'] = parser.minoccurrence
    if parser.stopword_file:
        config['stopwords'] = load_stopwords(parser.stopword_file)
    else:
        config['stopwords'] = set()

    fnames = get_filenames(dirname, parser.extension)
    
    try:
        generate_dat_and_vocab_files(fnames, config)
    except IOError as ioe:
        print(ioe)
        sys.exit(1)
