from difflib import SequenceMatcher

from src.sequence import Sequence


class Fragment:
    '''
    Class to properly handle fragments

    len : int
        The length of the fragment i.e. how good it is
    seq1 : tuple[str, int]
        Tuple with `(name, index)`, `index` being the starting index of the
        fragment in the sequence `name`
    seq2 : tuple[str, int]
        Same as `seq1` for the second sequence involved in the fragment
    '''

    def __init__(self, l, seq1, seq2):
        self.len = l
        self.seq1 = seq1
        self.seq2 = seq2


def get_fragments(seqs: list[Sequence]) -> list[Fragment]:
    '''
    Return all the fragments for given sequences
    '''
    n_seqs = len(seqs)
    frags = []

    # we iterate through each pair of sequences
    for i in range(n_seqs):
        seq1 = seqs[i]
        for j in range(i + 1, n_seqs):
            seq2 = seqs[j]

            # we search matching substrings in the pair of sequences
            s = SequenceMatcher(None, seq1.seq, seq2.seq)
            for block in s.get_matching_blocks()[:-1]:
                frags.append(Fragment(
                    block.size,
                    (seq1.name, block.a),
                    (seq2.name, block.b)
                    ))

    return frags
