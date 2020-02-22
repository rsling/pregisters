import sys
import os
import re
import argparse
import lxml.etree as ET


def xmlify(line):
    elems = line.split('\t')
    if len(elems) < 1:
        raise Exception('An empty VRT line was passed.')
    xmlified = u'<token><word>{}</word>'.format(elems[0])
    if len(elems) > 1:
        xmlified = xmlified + u'<annotations><annotation>{}</annotation></annotations>'.format(u'</annotation><annotation>'.join(elems[1:]))
    xmlified = xmlified + u'</token>'
    return(''.join(xmlified))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('xml', help='input COW-XML document')
    parser.add_argument('xsl', help='xsl file to be used')
    parser.add_argument('html', help='output HTML file')
    parser.add_argument('--css', help='stylesheet to be linked')
    parser.add_argument('--erase', action='store_true', help="erase outout files if present")
    args = parser.parse_args()

    # Check input files.
    infiles = [args.xml, args.xsl]
#    if args.css is not None:
#        infiles.append(args.css)
    for fn in infiles:
        if not os.path.exists(fn):
            sys.exit("Input file does not exist: " + fn)

    # Check (potentially erase) output files.
    outfiles = [args.html]
    for fn in outfiles:
        if fn is not None and os.path.exists(fn):
            if args.erase:
                try:
                    os.remove(fn)
                except:
                    sys.exit("Cannot delete pre-existing output file: " + fn)
            else:
                sys.exit("Output file already exists: " + fn)

    # Load document.
    doc = ['<?xml version="1.0" encoding="UTF-8"?><?xml-stylesheet type="text/xsl" href="cow.xsl"?>']
    with open(args.xml, 'r') as h:
        for l in h:
            if l is not None and not re.match(r'^\s*$', l):
                doc.append(l.decode('utf-8').strip())

    # XML-encode VRT.
    doc = [line if re.match(r'^<', line) else xmlify(line) for line in doc]

    # Apply XSLT.
    dom = ET.fromstring(' '.join(doc).encode('utf-8'))
    xslt = ET.parse(args.xsl)
    transform = ET.XSLT(xslt)
    dom = transform(dom)

    # Link CSS.
    if args.css is not None:
        head = dom.find('head')
        link = ET.Element('link', {'rel': 'stylesheet', 'type': 'text/css', 'href': args.css})
        head.append(link)

    with open(args.html, 'wb') as f:
        f.write(ET.tostring(dom, pretty_print=True))

if __name__ == "__main__":
    main()
