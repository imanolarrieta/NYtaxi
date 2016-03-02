#!/usr/bin/env python2.7
# Imanol Arrieta Ibarra
# Identity mapper.
# Call : cat file | ./identity-mapper.py

import sys

for line in sys.stdin:

    print line.rstrip('\n')
