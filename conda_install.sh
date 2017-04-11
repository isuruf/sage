#!/bin/bash

# Since sage version number and conda version number are different, we don't check it for now.
conda install --no-update-deps $1 -c conda-forge -p $2
touch "$SAGE_SPKG_INST/$3"
