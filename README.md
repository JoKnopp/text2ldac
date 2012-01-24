text2ldac
=========

txt2ldac is a python command line tool that takes a directory containing .txt
files as input and generates three output files that can be used by the ldac or
hlda implementations by David Blei (cf. [1] and [2]):

1. .dat – each line has the form:
    *uniqueTerms term1:count term2:count … termN:count*
2. .vocab – contains all unique words. The line number corresponds to the number
    used in the .dat file to represent the word
3. .dmap – lists all filenames. Line one lists the name of the document
    that is represented on line one in the .dat file. Used by David Blei's
    python script for tree generation for hlda results

run 'python text2ldac --help' for information about its usage.

[1] http://www.cs.princeton.edu/~blei/lda-c/

[2] http://www.cs.princeton.edu/~blei/downloads/hlda-c.tgz (starts download)

Licensing
---------

This file is part of text2ldac.

text2ldac is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

text2ldac is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with text2ldac. If not, see <http://www.gnu.org/licenses/>.
