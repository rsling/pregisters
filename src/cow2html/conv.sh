#!/bin/bash

set -e
set -u

OUTDIR=html
CONV=/Users/user/Workingcopies/COW2HTML/convert.py
XSL=/Users/user/Workingcopies/COW2HTML/cow.xsl
CSS='../../../cow.css'

mkdir -p ${OUTDIR}

cp cow.css ${OUTDIR}

r=$(pwd)
c="${r}/${OUTDIR}"

for f in $(find precox -name '*.xml')
do
  b=$(basename ${f})
  d=$(dirname ${f})
  od=${r}/${OUTDIR}/${d}
  of=${od}/$(basename ${b} .xml).html
  mkdir -p ${od}
  echo "${f} > ${of}"
  python ${CONV} ${f} ${XSL} ${of} --css ${CSS} --erase
  
  cd ${r}
done
