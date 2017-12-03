# dir-stats

A set of scripts to create and transform directory statistics, based on file extensions and file sizes.

## Files

* dir-stats.py  
The main script. This one creates an INI file containing the desired statistics.
* dir-stats-summary.py  
This one takes one or more INI files and summarizes directory sizes, returning only those directories that hit a given size limit.
* dir-stats-ini2html.py  
This one takes an INI file and transforms it into a HTML file.
* dir-stats-htmlmarker.py  
This one goes through a HTML file created by `dir-stats-ini2html.py` and highlights certain lines based on keywords.

### dir-stats.py

`./dir-stats.py [options] <basedir> [extensions]`

Options:

* -h, --help  
Display an usage message and exit.
* -s STYLE, --style=STYLE  
Define the style of the output. Accepted values are "win" and "unix". The default value us "win".

"basedir" is the directory where the script starts to search for files.

"extensions" is an unlimited list of file extensions that shall be included in the statistics. If you want to include each and every file in the statistics use '*' as the extension. The default extension list is "avi", "mpeg", "mpg" and "wmv".

### dir-stats-summary.py

`./dir-stats-summary.py [options] <filenames ...>`

Options:

* -h, --help  
Display an usage message and exit.
* -l BYTES, --limit=BYTES  
Set the minimum number of bytes that triggers reporting of a directory. The default limit is 50000000 bytes.
* -s STYLE, --style=STYLE  
Define the style of the output. Accepted values are "win" and "unix". The default value is "win".

"filenames" is a list of one or more INI files that shall be summarized.

### dir-stats-ini2html.py

`./dir-stats-ini2html.py [options] <inifiles ...>`

Options:

* -h, --help  
Display an usage message and exit.
* --version  
Display the version of the script and exit.
* -p PREFIX, --prefix=PREFIX  
The prefix for all filenames. Defaults to nothing.
* -s SUFFIX, --suffix=SUFFIX  
The suffix for all filenames. Defaults to nothing.
* -e EXTENSION, --extension=EXTENSION  
The extension of the HTML files. Defaults to "html".
* -t TITLE, --title=TITLE  
Defines the title of the HTML file.
* -w WORD, --word=WORD  
Defines words to highlight in the output. Defaults to nothing. May be given multiple times to highlight multiple words. Words are case-insensitive. Only full lines are marked.

"inifiles" is a list of one or more INI files that shall be compiled to one or more HTML files.

### dir-stats-htmlmarker.py

`./dir-stats-htmlmarker.py [options] <htmlfile>`

Options:

* -h, --help  
Display an usage message and exit.
* --version  
Display the version of the script and exit.
* -x, --exitcodes  
Display a list of possible exit codes and exit.
* -w WORD, --word=WORD  
Search for the keyword WORD. Defaults to nothing. Can be given multiple times.
* -f FILENAME, --wordfile=FILENAME  
Read keywords from the file FILENAME. Can be combined with '-w'.
* -o FILENAME, --outfile=FILENAME  
Write the output to the file FILENAME instead of stdout.

"htmlfile" is the HTML file that shall be parsed.

## Sample Usage

Get statistics from a backup directory, looking at all files. Redirect the output to an INI file:

`./dir-stats.py /mnt/Backup '*' >backup-stats.ini`

Summarize those statistics to only get directories that contain 100 MB or more. Redirect the output to another INI file:

`./dir-stats-summary.py -l 100000000 backup-stats.ini >backup-stats-summary.ini`

Transform the INI file to a HTML file, titled "My Backup Summary". The HTML file will be written automatically:

`./dir-stats-ini2html.py -t "My Backup Summary" backup-stats-summary.ini`

Highlight the word "media" (case-insensitive) within the HTML file. Redirect the output to a new HTML file:

`./dir-stats-htmlmarker.py -w media backup-stats-summary.ini.html >backup-stats-summary-highlighted.html`

## Source

The main repository for dir-stats is located at GitLab: [https://gitlab.com/rbrt-weiler/dir-stats](https://gitlab.com/rbrt-weiler/dir-stats)

## License

dir-stats is released under the Zlib License.

## Copyright

dir-stats is (c) 2007-2017 Robert Weiler.

