#!/usr/bin/python
# vim: set sw=4 sts=4 ts=8 et ft=python fenc=utf8 ff=unix tw=74 :

#
# SYNOPSIS
# ========
# This script creates a statistic of specific files contained in a
# directory and all its subdirectories.
#
# ARGUMENTS
# =========
# One parameter is required: It is the base directory where the script
# starts to search for files. The base dir is expected as the first
# argument.
# One can provide an unlimited number of optional arguments after the
# base dir. These arguments are treated as file extensions. The default
# list of file extensions includes some media files. If you provide any
# number of optional arguments the default list won't be used at all.
#
# HOW IT WORKS
# ============
# This script will start searching for files. The extension of every
# found file is then checked against the list of file extensions. If a
# file matches any of the extensions its name and size is stored in an
# internal data structure. After all files have been examined the script
# prints an ini-style report to stdout.
#
# OUTPUT
# ======
# The script will print an ini-style report to stdout. This report
# contains a section for every file extension, taken from the default
# list or from the command line.
# Each section contains the names and sizes of all files found that had
# a matching extension. The filename is the key, the filesize in bytes is
# the value.
# Each section is closed by a comment. That comment includes the section
# name, the total number of files and the total size of the files.
# Furthermore there is another comment at the end of the file, stating the
# number of total files and the summed up filesize.
#
# HISTORY
# =======
# 2017-Dec-02 rbrt-weiler
#   * Now mapping empty extensions to ' '.
# 2011-Mar-22 rbrt-weiler
#   * Redirected error messages to stderr.
#   * Released the script as v1.0.3.
# 2011-Mar-18 rbrt-weiler
#   * Added support for the extension '*', meaning all files.
#   * Catched OSError when stat()ing a file fails.
#   * Released the script as v1.0.2.
# 2007-Dec-21 rbrt-weiler
#   * First bugfix, forgot to lower the extension in one case.
#   * Released the script as v1.0.1.
# 2007-Dec-19 rbrt-weiler
#   * Added usage message.
#   * Added option "-s".
#   * File extensions are now case insensitive (by lowering all of them).
#   * Released the script as v1.0.0.
# 2007-Dec-18 rbrt-weiler
#   * Created the script.
#

import getopt
import os
import sys
import time

#####################################################################

SCRIPT_VERSION = '1.0.3'

opt_style = 'win'
opt_allfiles = 0

#####################################################################

def main():
    global opt_style, opt_allfiles
    extensions = [
            'avi',
            'mpeg',
            'mpg', 
            'wmv'
    ]

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hs:', [
                'help', 'style=' ])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    for o, a in opts:
        if o in ('-s', '--style'):
            if a in ('win', 'unix'):
                opt_style = a
        if o in ('-h', '--help'):
            usage()
            sys.exit(1)

    if 0 == len(args):
        usage()
        sys.exit(2)
    else:
        basedir = args[0]
        if not os.path.isdir(basedir):
            usage()
            sys.exit(3)
        if 1 < len(args):
            extensions = args[1:]

    exts_lowered = [ ]
    for ext in extensions:
        exts_lowered.append(ext.lower())
        if '*' == ext:
            opt_allfiles = 1

    dirStats(basedir, exts_lowered, opt_allfiles)

#####################################################################

def dirStats(basedir, extensions, allfiles):
    files = { }
    if 0 == allfiles:
        for ext in extensions:
            files[ext.lower()] = { }
        
    for root, dirlist, filelist in os.walk(basedir):
        for filename in filelist:
            fullname = os.path.join(root, filename)
            if -1 != filename.find('.'):
                ext = filename.split('.')[-1]
                if '' == ext:
                    ext = ' '
            else:
                ext = '*'
            if 1 == allfiles:
                if not ext.lower() in files:
                    files[ext.lower()] = { }
                try:
                    files[ext.lower()][fullname] = os.stat(fullname).st_size
                except OSError:
                    sys.stderr.write('Error stat\'ing <' + fullname \
                        + '>' + "\r\n")
            elif ext.lower() in extensions:
                try:
                    files[ext.lower()][fullname] = os.stat(fullname).st_size
                except OSError:
                    sys.stderr.write('Error stat\'ing <' + fullname \
                        + '>' + "\r\n")

    kv_sep = ' = '
    cmt_char = '; '
    if 'unix' == opt_style:
        kv_sep = ': '
        cmt_char = '# '

    print cmt_char + 'created ' + time.asctime() + ' by dir-stats ' \
            + 'v' + SCRIPT_VERSION
    print

    totalfiles = 0
    totalsize = 0
    exts = files.keys()
    exts.sort()
    for ext in exts:
        fcnt = 0
        scnt = 0
        print '[' + ext + ']'
        keys = files[ext].keys()
        keys.sort()
        for key in keys:
            print str(key) + kv_sep + str(files[ext][key])
            fcnt = fcnt + 1
            scnt = scnt + files[ext][key]
        print cmt_char + ext + ': ' + str(fcnt) + ' files, ' \
                + str(scnt) + ' bytes'
        print
        totalfiles = totalfiles + fcnt
        totalsize = totalsize + scnt
    print cmt_char + 'total size: ' + str(totalfiles) + ' files, ' + \
            str(totalsize) + ' bytes'

#####################################################################

def usage():
    print 'dir-stats v' + SCRIPT_VERSION + ' - released under the Zlib ' \
            + 'license'
    print 'Usage: ' + os.path.basename(sys.argv[0]) + ' [options] ' \
            + 'basedir [extensions]'
    print
    print 'Options:'
    print '  -h, --help'
    print '    Display this usage message and exit.'
    print '  -s STYLE, --style=STYLE'
    print '    Define the style of the output. Accepted values are ' \
            + '"win" and "unix".'
    print '    The default value is "win".'
    print
    print '"basedir" is the directory where the script starts to ' \
            + 'search for files.'
    print
    print '"extensions" is an unlimited list of file extensions that ' \
            + 'shall be included'
    print 'in the statistics. If you want to include each and every '\
            + 'file in the'
    print 'statistics use \'*\' as the extension. The default ' \
            + 'extension list is'
    print '"avi", "mpeg", "mpg" and "wmv".'

#####################################################################

if __name__ == "__main__":
    main()
    sys.exit(0)

