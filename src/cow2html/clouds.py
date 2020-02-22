# -*- coding: utf-8 -*-

import sys
import os
import re
import glob
import argparse
import wordcloud

HTML_IN=u'<html><head><link href="../../../cow.css" rel="stylesheet" type="text/css"/></head><body><div id="outer"><div class="header"><h1>PreCOX pregister'
HTML_MID=u'</h1><h2><a href="cloud.html" class="faint">See the feature cloud…</a></h2><h2><a href="../index.html" class="faint">Back to all pregisters…</a></h2></div><h1>Best documents for this pregister:</h1><div class="listing"><table class="list"><tr><th>DECOW16B ID</th><th>probability</th></tr>'
HTML_OUT=u'</table></div></body></html>'

HTML_IN2=u'<html><head><link href="../../cow.css" rel="stylesheet" type="text/css"/></head><body><div id="outer"><div class="header"><h1>PreCOX corpus'
HTML_MID2=u'</h1></div><h1>Pregisters in this corpus:</h1><div class="listing">'
HTML_OUT2=u'</div></body></html>'

HTML_IN3=u'<html><head><link href="../../../cow.css" rel="stylesheet" type="text/css"/></head><body><div id="outer"><div class="header"><h1>Feature cloud for PreCOX pregister'
HTML_OUT3=u'</h1><h2><a href="index.html" class="faint">Back to overview for this pregister…</a></h2></div><img src="cloud.png" class="cloud"/></body></html>'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('topics', help='input file with topic-term mapping')
    parser.add_argument('mapping', help='file with feature mapping')
    parser.add_argument('directory', help='root directory with topic-wise numbered folders')
    parser.add_argument('identifier', help='identifier of the LDA experiment')
    parser.add_argument('--noclouds', action='store_true', help='do not regenerate clouds')
    args = parser.parse_args()

    # Check input files.
    infiles = [args.topics, args.mapping]
    for fn in infiles:
        if not os.path.exists(fn):
            sys.exit("Input file does not exist: " + fn)
    
    if not os.path.isdir(args.directory):
        sys.exit("Folder does not exist.")

    # Load mapping.
    mapping = dict()
    with open(args.mapping, 'r') as h:
        for l in h:
            if l is not None:
                ls = l.decode('utf-8').strip().split('\t')
                if not len(ls) == 2:
                    sys.exit('Problem with: ' + l.encode('utf-8'))
                mapping[ls[0]] = ls[1]
 
    # Load topics.
    topics = dict()
    with open(args.topics, 'r') as h:
        for l in h:
            if l is not None:
                ls = l.decode('utf-8').strip().split('\t')
                topics[int(re.sub(r'topic', r'', ls[0]))] = dict(zip(
                    [mapping[x] for x,y in [z.split(' ') for z in ls[1:]]],
                    [float(y) for x,y in [z.split(' ') for z in ls[1:]]])
                    )
 
    for i in topics.keys():

        # Check and list directory.
        path='{}/{}/'.format(args.directory, i)
        if not os.path.isdir(path):
            sys.exit("Folder does not exist: {}".format(path))
        lst = glob.glob("{}*.html".format(path))
        lst.reverse()
        lst = [os.path.basename(x) for x in lst if not os.path.basename(x)=='index.html' and not os.path.basename(x)=='cloud.html']
 
        # Make word cloud.
        if not args.noclouds:
            wc = wordcloud.WordCloud(width=1600, height=800)
            wc.fit_words(topics[i])
            wc.to_file('{}cloud.png'.format(path, i))
 
        # Create listing.
        page=[HTML_IN, '{} in corpus {}'.format(i, args.identifier), HTML_MID]

        # The list needs to be sorted by a file name component (probability)
        for fi in sorted(lst, key=lambda x: float(re.sub(r'^[^_]+_(.+)\.html$', r'\1', x)), reverse = True):
            prob = float(re.sub(r'^[^_]+_(.+)\.html$', r'\1', fi))
            docname = re.sub(r'_[0-9.]+\.html$', r'', fi)
            page.append('<tr class="listrow"><td class="listcell"><a href="{0}" style="color: rgba(100, {3}, 50);">{1}</a></td><td class="listcell" style="color: rgba(0, {3}, 0);">{2}</td></tr>'.format(fi, u'{}...{}'.format(docname[:2], docname[-2:]), prob, prob*255))
    
        page.append(HTML_OUT)
        with open('{}index.html'.format(path), 'wb') as f:
            f.write('\n'.join(page).encode('utf-8'))

        # Create cloud HTML page.
        page=[HTML_IN3, '{} in corpus {}'.format(i, args.identifier), HTML_OUT3]
        with open('{}cloud.html'.format(path), 'wb') as f:
            f.write('\n'.join(page).encode('utf-8'))
 
    
    # Make master index.

    # List directory.
    path=args.directory
    lst = glob.glob("{}/*".format(path))
    lst = [os.path.basename(x) for x in lst if not os.path.basename(x)=='index.html']
    lst.sort(key = lambda x: int(x))

    # Create listing.
    page=[HTML_IN2, args.identifier, HTML_MID2]

    for fi in lst:
        page.append('<span class="listspan"><a href="{}/index.html">{}</a></span>'.format(fi, fi))

    page.append(HTML_OUT2)
    with open('{}/index.html'.format(path), 'wb') as f:
        f.write('\n'.join(page).encode('utf-8'))

if __name__ == "__main__":
    main()
