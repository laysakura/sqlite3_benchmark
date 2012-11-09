#!/bin/sh

## Find sqlite3_benchmark directory
basedir=$(cd $(dirname $(readlink -f $0)); pwd)"/.."


## Check if directory is empty
if [ $(ls -a |wc -l) -ne 2 ]; then
    echo "Directory is not empty."
    exit 1
fi


mkdir python
cp -r ${basedir}/python/*.py python/
mkdir resultsDb
mkdir inputDb
cp ${basedir}/README-template.org .
