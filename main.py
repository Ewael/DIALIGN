#!/usr/bin/env python3

'''
This file is an implementation of the DIALIGN algorithm for sequences alignement
detection. It uses FASTA format as input and DIALIGN format as output.

References:

> DIALIGN manual (EN)
http://dialign.gobics.de/anchor/manual

> Input and output details (EN)
https://www.genomatix.de/online_help/help_dialign/dialign2_help.html

> `lingpy` documention (EN)
http://lingpy.org/reference/lingpy.align.html

> Algorithm details (FR)
https://wikis.univ-lille.fr/bilille/_media/ib2019-2-partie2-alignement.pdf (p. 61)
https://tel.archives-ouvertes.fr/tel-00352784/document (p. 69)
'''

import sys

from sequence import parse_sequences


def main():
    # bad usage
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} [sequence file]')
        exit(1)

    # parse file to obtain sequences
    seqs = parse_sequences(sys.argv[1])
    for seq in seqs:
        print(seq.name, seq.seq)


if __name__ == '__main__':
    main()
