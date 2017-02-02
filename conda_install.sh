#!/usr/bin/env bash

exists=`conda list $1$ --json -p $2`
echo "$exists"
if [ "$exists" == "[]" ]; then
    conda install $1 -c conda-forge -c r -p $2
fi
