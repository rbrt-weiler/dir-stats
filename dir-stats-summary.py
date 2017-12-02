#!/usr/bin/python
# vim: set sw=4 sts=4 ts=8 et ft=python fenc=utf8 ff=unix tw=74 :

#
# SYNOPSIS
# ========
# This script analyses an INI file created by dir-stats.py and displays
# directories containing a certain amount of data.
#
# ARGUMENTS
# =========
# Call the script without any parameters to see an unsage message.
#
# OUTPUT
# ======
# The script will print an INI style list of directory names and byte
# counts to stdout.
#
# HISTORY
# =======
# 2008-Jan-22 rbrt-weiler
#   * Created the script.
#

import getopt
import os.path
import sys
import time
import ConfigParser

##########################################################################

SCRIPT_VERSION = '1.0.0'

opt_limit = 50000000
opt_style = 'win'

##########################################################################

class MyRawConfigParser(ConfigParser.RawConfigParser):
    def optionxform(self, optionstr):
        return str(optionstr)

##########################################################################

def main():
    global opt_limit, opt_style
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hl:s:', [ 'help',
                'limit=', 'style=' ])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(1)
        if o in ('-l', '--limit'):
            opt_limit = int(a)
        if o in ('-s', '--style'):
            if a in ('win', 'unix'):
                opt_style = a
            else:
                usage()
                sys.exit(1)

    if 0 == len(args):
        usage()
        sys.exit(1)
    else:
        for arg in args:
            if not os.path.isfile(arg):
                print 'Error: "' + arg + '" is no file.'
                sys.exit(2)

    summarize(args)

##########################################################################

def summarize(filenames):
    if 'win' == opt_style:
        cmt_char = ';'
        kv_sep = ' = '
    else:
        cmt_char = '#'
        kv_sep = ': '

    summary = { }
    
    print cmt_char + ' created ' + time.asctime() + ' by ' \
            + 'dir-stats-summary v' + SCRIPT_VERSION
    print cmt_char + ' using a limit of ' + str(opt_limit) + ' bytes'

    for filename in filenames:
        cfg_parser = MyRawConfigParser()
        try:
            f_in = open(filename, 'r')
        except:
            print 'Error: Cannot read file "' + filename + '".'
            sys.exit(3)
        cfg_parser.readfp(f_in)
        f_in.close()

        sections = cfg_parser.sections()
        for section in sections:
            options = cfg_parser.options(section)
            for option in options:
                try:
                    size = cfg_parser.getint(section, option)
                except ValueError:
                    size = 0
                (basedir, basename) = os.path.split(option)
                if summary.has_key(basedir):
                    summary[basedir] = summary[basedir] + size
                else:
                    summary[basedir] = size

        total_dirs = 0
        total_size = 0
        filename = os.path.basename(filename)

        dirs = summary.keys()
        dirs.sort()
        print
        print '[' + filename + ']'
        for dir in dirs:
            if summary[dir] >= opt_limit:
                print dir + kv_sep + str(summary[dir])
                total_dirs = total_dirs + 1
                total_size = total_size + summary[dir]
        print cmt_char + ' ' + filename + ': ' + str(total_dirs) \
                + ' directories with ' + str(total_size) + ' bytes'
        
        cfg_parser = None
        summary = { }

##########################################################################

def usage():
    print 'dir-stats-summary v' + SCRIPT_VERSION + ' - released ' \
            + 'under the Zlib license'
    print 'Usage: ' + os.path.basename(sys.argv[0]) + ' [options] ' \
            + 'filename [...]'
    print
    print 'Options:'
    print '  -h, --help'
    print '    Display this usage message and exit.'
    print '  -l BYTES, --limit=BYTES'
    print '    Set the minimum number of bytes that triggers reporting '
    print '    of a directory.'
    print '    The default limit is 50000000 bytes.'
    print '  -s STYLE, --style=STYLE'
    print '    Define the style of the output. Accepted values are ' \
            + '"win" and "unix".'
    print '    The default value is "win".'

##########################################################################

if '__main__' == __name__:
    main()
    sys.exit(0)
