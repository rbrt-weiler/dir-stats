#!/usr/bin/python
# vim: set sw=4 sts=4 ts=8 et ft=python fenc=utf8 ff=unix tw=74 :

#
# SYNOPSIS
# ========
# This script parses a HTML file created by dir-stats-ini2html.py and
# highlights certain lines based on keywords.
#
# REQUIREMENTS
# ============
# The file that is parsed has to be created by dir-stats-ini2html.py
# v1.2.0 or greater. It relies on the specific output format.
#
# ARGUMENTS
# =========
# Please call the script without any arguments for an usage message
# explaining all options and arguments.
#
# HISTORY
# =======
# 2011-Apr-01 rbrt-weiler
#   * Added speaking exit codes and option '-x'.
#   * Added option '--version'.
#   * Redirected error messages to stderr.
#   * Released the script as v1.0.0.
# 2011-Mar-24 rbrt-weiler
#   * Added function-specific exit codes.
#   * Released the script as v0.9.0.
# 2011-Mar-23 rbrt-weiler
#   * Created the script.
#

import getopt
import os.path
import sys
import xml.dom.minidom

#####################################################################

SCRIPT_VERSION = '1.0.0'

EX_SUCCESS = 0
EX_NOARGS = 1
EX_NOFILE = 10
EX_NOTREADABLE = 11
EX_NOTWRITEABLE = 12
EX_NOTWELLFORMED = 20

opt_parsefile = ''
opt_words = [ ]
opt_wordfile = None
opt_outfile = None

#####################################################################

def main():
    global opt_parsefile, opt_words, opt_wordfile, opt_outfile

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hxw:f:o:', [ 'help',
                'version', 'exitcodes', 'word=', 'wordfile=',
                'outfile=' ])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(EX_SUCCESS)
        if o in ('--version'):
            printVersion()
            sys.exit(EX_SUCCESS)
        if o in ('-x', '--exitcodes'):
            exitcodes()
            sys.exit(EX_SUCCESS)
        if o in ('-w', '--word'):
            opt_words.append(a)
        if o in ('-f', '--wordfile'):
            opt_wordfile = a
        if o in ('-o', '--outfile'):
            opt_outfile = a

    if 1 != len(args):
        usage()
        sys.exit(EX_NOARGS)
    else:
        opt_parsefile = args[0]
        if not os.path.isfile(opt_parsefile):
            sys.stderr.write('Error: <' + opt_parsefile \
                    + '> is no file.\n')
            sys.exit(EX_NOFILE)

    if None != opt_wordfile:
        parseWordfile(opt_wordfile)

    parseFile(opt_parsefile, opt_words, opt_outfile)

#####################################################################

def parseWordfile(filename):
    global opt_words
    try:
        f_in = open(filename, 'r')
    except:
        sys.stderr.write('Error: <' + filename + '> cannot be read.\n')
        sys.exit(EX_NOTREADABLE)
    for line in f_in.readlines():
        line = line.strip()
        if "" != line:
            opt_words.append(line)
    f_in.close()

#####################################################################

def parseFile(filename, wordlist, outfile = None):
    try:
        dom = xml.dom.minidom.parse(filename)
    except:
        sys.stderr.write('Error: <' + filename \
                + '> is not well-formed.\n')
        sys.exit(EX_NOTWELLFORMED)
    bodies = dom.getElementsByTagName('tbody')
    for body in bodies:
        rows = body.getElementsByTagName('tr')
        for row in rows:
            cells = row.getElementsByTagName('td')
            if 3 != len(cells):
                continue
            name = cells[0].firstChild.nodeValue
            size = cells[1].firstChild.nodeValue
            unit = cells[2].firstChild.nodeValue
            for word in wordlist:
                if -1 != name.lower().find(word.lower()):
                    row.setAttribute('class', \
                            row.getAttribute('class') + ' mark')
                    break
    if None == outfile:
        print dom.toxml('UTF-8')
    else:
        try:
            f_out = open(outfile, 'w')
            f_out.write(dom.toxml('UTF-8'))
        except:
            sys.stderr.write('Error: Cannot write file <' + outfile \
                    + '>.\n')
            sys.exit(EX_NOTWRITEABLE)

#####################################################################

def printVersion():
    print 'dir-stats-htmlmarker v' + SCRIPT_VERSION + ' - released ' \
            + 'under the Zlib license'

#####################################################################

def usage():
    printVersion()
    print 'Usage: ' + os.path.basename(sys.argv[0]) + ' [options] ' \
            + 'htmlfile'
    print
    print 'Options:'
    print '  -h, --help'
    print '    Display this usage message and exit.'
    print '  --version'
    print '    Display the version of the script and exit.'
    print '  -x, --exitcodes'
    print '    Display a list of possible exit codes and exit.'
    print '  -w WORD, --word=WORD'
    print '    Search for the keyword WORD. Defaults to nothing. Can ' \
            + 'be given multiple'
    print '    times.'
    print '  -f FILENAME, --wordfile=FILENAME'
    print '    Read keywords from the file FILENAME. Can be combined ' \
            + 'with \'-w\'.'
    print '  -o FILENAME, --outfile=FILENAME'
    print '    Write the output to the file FILENAME instead of ' \
            + 'stdout.'
    print
    print '"htmlfile" is the HTML file that shall be parsed.'

#####################################################################

def exitcodes():
    printVersion()
    print
    print 'Error codes:'
    print '  ' + str(EX_SUCCESS)
    print '    The script finished successfully.'
    print '  ' + str(EX_NOARGS)
    print '    No HTML file was supplied to the script.'
    print '  ' + str(EX_NOFILE)
    print '    The file supplied is no file.'
    print '  ' + str(EX_NOTREADABLE)
    print '    The file supplied is not readable.'
    print '  ' + str(EX_NOTWRITEABLE)
    print '    The file supplied is not writeable.'
    print '  ' + str(EX_NOTWELLFORMED)
    print '    The file supplied is not well-formed.'
    print
    print 'The exit message will provide more detailed information.'

#####################################################################

if '__main__' == __name__:
    main()
    sys.exit(EX_SUCCESS)

