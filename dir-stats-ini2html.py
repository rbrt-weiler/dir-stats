#!/usr/bin/python
# vim: set sw=4 sts=4 ts=8 et ft=python fenc=utf8 ff=unix tw=74 :

#
# SYNOPSIS
# ========
# This script parses an INI file created by dir-stats.py and creates a
# HTML file.
#
# ARGUMENTS
# =========
# Please call the script without any arguments for an usage message
# explaining all options and arguments.
#
# HISTORY
# =======
# 2011-Apr-01 rbrt-weiler
#   * Improved the code for marking a table row.
#   * Added option '--version'.
#   * Released the script as v1.2.0.
# 2011-Mar-29 rbrt-weiler
#   * Once again modifications to the HTML output, added <colgroup>s.
# 2011-Mar-24 rbrt-weiler
#   * Added an XML declaration to the HTML output.
# 2011-Mar-23 rbrt-weiler
#   * More modifications of the HTML output. Now XHTML 1.0 Transitional.
#   * Added option '-w' to highlight lines based on keywords.
# 2011-Mar-18 rbrt-weiler
#   * Minor modification of the HTML output to save some bytes.
#   * Released the script as v1.0.2.
# 2007-Dec-21 rbrt-weiler
#   * Started the implementation of an own ConfigParser.
#   * Released the script as v1.0.1.
# 2007-Dec-19 rbrt-weiler
#   * Created the script.
#   * Released the script as v1.0.0.
#

import getopt
import os
import sys
import time
import ConfigParser

from xml.sax.saxutils import escape

#####################################################################

SCRIPT_VERSION = '1.2.0'

opt_prefix = ''
opt_suffix = ''
opt_extension = 'html'
opt_title = None
opt_words = [ ]

#####################################################################

class MyRawConfigParser(ConfigParser.RawConfigParser):
    def optionxform(self, optionstr):
        return str(optionstr)

#####################################################################

def main():
    global opt_prefix, opt_suffix, opt_extension, opt_title, opt_words

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:s:e:t:w:', [ 'help',
                'version', 'prefix=', 'suffix=', 'extension=', 'title=',
                'word=' ])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)
        if o in ('--version'):
            printVersion()
            sys.exit(0)
        if o in ('-p', '--prefix'):
            opt_prefix = a
        if o in ('-s', '--suffix'):
            opt_suffix = a
        if o in ('-e', '--extension'):
            opt_extension = a
        if o in ('-t', '--title'):
            opt_title = a
        if o in ('-w', '--word'):
            opt_words.append(a)

    if 0 == len(args):
        usage()
        sys.exit(2)
    else:
        for arg in args:
            if not os.path.isfile(arg):
                print 'Error: "' + arg + '" is no file.'
                sys.exit(3)

    createHtml(args)

#####################################################################

def createHtml(filenames):
    for infile in filenames:
        cfg_parser = MyRawConfigParser()
        try:
            f_in = open(infile, 'r')
        except:
            print 'Error: Cannot read file "' + infile + '".'
            sys.exit(4)
        cfg_parser.readfp(f_in)
        f_in.close()

        html_title = os.path.basename(infile)
        if None != opt_title:
            html_title = str(opt_title)

        outfile = opt_prefix + os.path.basename(infile) + opt_suffix \
                + '.' + opt_extension
        try:
            f_out = open(outfile, 'w')
        except:
            print 'Error: Cannot write file "' + outfile + '".'
            sys.exit(6)
        writeHtmlLeader(f_out, html_title)

        sections = cfg_parser.sections()
        sections.sort()
        for section in sections:
            files_total = 0
            size_total = 0
            f_out.write('<hr />\n')
            f_out.write('<table width="100%">\n')
            f_out.write('<caption>' + escape(section) + '</caption>\n')
            f_out.write('<colgroup>\n')
            f_out.write('<col width="88%" />\n')
            f_out.write('<col width="10%" />\n')
            f_out.write('<col width="2%" />\n')
            f_out.write('</colgroup>\n')
            f_out.write('<thead>\n')
            f_out.write('<tr><th>File</th><th>Size</th><th>Unit</th></tr>\n')
            f_out.write('</thead>\n')
            b_out = ''
            options = cfg_parser.options(section)
            options.sort()
            if 0 < len(options):
                for option in options:
                    try:
                        fsize = cfg_parser.getint(section, option)
                    except ValueError:
                        fsize = -1
                        option = option + ' {{ERROR}}'
                    if 0 == (files_total % 2):
                        colo = 'teven'
                    else:
                        colo = 'todd'
                    if 0 < len(opt_words):
                        for word in opt_words:
                            if -1 != option.lower().find(word.lower()):
                                colo += ' mark'
                                break
                    size, unit = computeSizeAndUnit(fsize)
                    b_out += '<tr class="' + colo + '"><td>' \
                            + escape(option) + '</td>' \
                            + '<td align="right">' \
                            + size + '</td><td>' \
                            + unit + '</td></tr>\n'
                    files_total = files_total + 1
                    size_total = size_total + fsize
                size, unit = computeSizeAndUnit(size_total)
            else:
                size = str(0)
                unit = 'B'
                b_out += '<tr><td colspan="3" align="center">No ' \
                        + 'matching files found.</td></tr>\n'
            f_out.write('<tfoot>\n')
            f_out.write('<tr><td colspan="3">' + escape(section) \
                    + ': ' + str(files_total) + ' objects, ' + size \
                    + ' ' + unit + '</td></tr>\n')
            f_out.write('</tfoot>\n')
            f_out.write('<tbody>\n')
            f_out.write(b_out)
            f_out.write('</tbody>\n')
            f_out.write('</table>\n')

        writeHtmlTrailer(f_out)
        f_out.close()
 
#####################################################################

def writeHtmlLeader(f, title):
    if not isinstance(f, file):
        print 'Error: writeHtmlLeader: Parameter is no file object.'
        sys.exit(7)

    title = escape(title)
    
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 ' \
            + 'Transitional//EN" ' \
            + '"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n')
    f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
    f.write('<head>\n')
    f.write('<meta http-equiv="Content-Type" content="' \
            + 'text/html; charset=UTF-8" />\n')
    f.write('<title>' + title + '</title>\n')
    f.write('<style type="text/css">\n')
    f.write('html, body { background-color: #fff; color: #000; }\n')
    f.write('caption { text-align: center; font-size: 150%; ' \
            + 'font-weight: bold }\n')
    f.write('th { text-align: center; font-weight: bold; }\n')
    f.write('tr.teven td { background-color: #eee; color: #000; }\n')
    f.write('tr.todd td { }\n')
    f.write('tr.mark td { background-color: #ff0; color: #000; }\n')
    f.write('tfoot td { text-align: center; }\n')
    f.write('</style>\n')
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<h1>' + title + '</h1>\n')

#####################################################################

def writeHtmlTrailer(f):
    if not isinstance(f, file):
        print 'Error: writeHtmlTrailer: Parameter is no file object.'
        sys.exit(7)

    f.write('<hr />\n')
    f.write('<div align="right"><em>Created ' \
            + escape(time.asctime()) + ' by dir-stats-ini2html v' \
            + SCRIPT_VERSION + '</em></div>\n')
    f.write('</body>\n')
    f.write('</html>')

#####################################################################

def computeSizeAndUnit(fsize):
    if not isinstance(fsize, int):
        fsize = int(fsize)

    if fsize > (1024 * 1024 * 1024):
        return [ '%.2f' % (float(fsize) / 1024 / 1024 / 1024), 'GiB' ]
    elif fsize > (1024 * 1024):
        return [ '%.2f' % (float(fsize) / 1024 / 1024), 'MiB' ]
    elif fsize > 1024:
        return [ '%.2f' % (float(fsize) / 1024), 'KiB' ]
    else:
        return [ str(fsize), 'B' ]

#####################################################################

def printVersion():
    print 'dir-stats-ini2html v' + SCRIPT_VERSION + ' - released ' \
            + 'under the Zlib license'

#####################################################################

def usage():
    printVersion()
    print 'Usage: ' + os.path.basename(sys.argv[0]) + ' [options] ' \
            + 'inifiles'
    print
    print 'Options:'
    print '  -h, --help'
    print '    Display this usage message and exit.'
    print '  --version'
    print '    Display the version of the script and exit.'
    print '  -p PREFIX, --prefix=PREFIX'
    print '    The prefix for all filenames. Defaults to nothing.'
    print '  -s SUFFIX, --suffix=SUFFIX'
    print '    The suffix for all filenames. Defaults to nothing.'
    print '  -e EXTENSION, --extension=EXTENSION'
    print '    The extension of the HTML files. Defaults to "html".'
    print '  -t TITLE, --title=TITLE'
    print '    Defines the title of the HTML file.'
    print '  -w WORD, --word=WORD'
    print '    Defines words to highlight in the output. Defaults to ' \
            + 'nothing. May be'
    print '    given multiple times to highlight multiple words. ' \
            + 'Words are'
    print '    case-insensitive. Only full lines are marked.'
    print
    print '"inifiles" is a list of one or more INI files that shall ' \
            + 'be compiled to one'
    print 'or more HTML files.'

#####################################################################

if '__main__' == __name__:
    main()
    sys.exit(0)

