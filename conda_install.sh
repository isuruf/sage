#!/usr/bin/env bash

for f in $2/conda-meta/$1-*; do
    [ -e "$f" ] && echo "Already installed using conda" || conda install $1 -c conda-forge -c r --use-local -p $2
    break
done

