from sequence import Sequence
from fragment import Fragment


def dialign(seqs: list[Sequence], frags: list[Fragment]) -> list[Sequence]:
    '''
    Return aligned sequences from non-aligned sequences and associated fragments
    '''
    # `None` lists that'll be filled with aligned fragments
    aligned_seqs = {}
    # easier to use a dictionnary to easily find a sequence by its name
    sequences = {}
    # to differenciate aligned and non-aligned indexes for lowercase insertions
    aligned_idxs = {}

    # compute longest sequence in input
    max_len = max([len(seq.seq) for seq in seqs])

    # fill our dicts
    for seq in seqs:
        aligned_idxs[seq.name] = []
        # just add the associated sequence
        sequences[seq.name] = seq.seq
        # we take longest sequence to be sure we don't get any surprise
        aligned_seqs[seq.name] = [None] * max_len * 2

    # iterate through fragments to build aligned sequences
    for frag in frags:
        # reminder: `seq1` and `seq2` are `(sequence_name, starting_index)`
        s1_name, s1_idx = frag.seq1
        s2_name, s2_idx = frag.seq2

        # the index will be the same in the aligned sequences
        aligned_idx = max(s1_idx, s2_idx)

        # case 1: both sequences can add this fragment
        # case 2: fragment was already added to one of the sequences
        if \
            ((aligned_seqs[s1_name][aligned_idx:aligned_idx + frag.len] == \
                    [None] * frag.len) \
                and (aligned_seqs[s2_name][aligned_idx:aligned_idx + frag.len] == \
                    [None] * frag.len)) \
            or (((aligned_seqs[s1_name][aligned_idx:aligned_idx + frag.len] == \
                        [None] * frag.len) \
                    or (aligned_seqs[s2_name][aligned_idx:aligned_idx + frag.len] == \
                        [None] * frag.len)) \
                and ((aligned_seqs[s1_name][aligned_idx:aligned_idx + frag.len] == \
                        list(sequences[s1_name][s1_idx:s1_idx + frag.len])) \
                    or (aligned_seqs[s2_name][aligned_idx:aligned_idx + frag.len] == \
                        list(sequences[s2_name][s2_idx:s2_idx + frag.len])))):

            # copy the associated fragment
            aligned_seqs[s1_name][aligned_idx:aligned_idx + frag.len] = \
                sequences[s1_name][s1_idx:s1_idx + frag.len]
            aligned_seqs[s2_name][aligned_idx:aligned_idx + frag.len] = \
                sequences[s2_name][s2_idx:s2_idx + frag.len]

            # add aligned indexes
            for i in range(s1_idx, s1_idx + frag.len):
                aligned_idxs[s1_name].append(i)
            for i in range(s2_idx, s2_idx + frag.len):
                aligned_idxs[s2_name].append(i)

    # insert lowercase letters for non-aligned elements
    for seq in seqs:
        i = 0 # aligned_seqs[seq.name] index
        x = 0 # seq.seq index
        y = 0 # aligned_seq index

        # create aligned list copy with no leading None
        aligned_seq = aligned_seqs[seq.name].copy()
        while aligned_seq[0] == None:
            aligned_seq = aligned_seq[1:]
            i += 1 # offset for leading None

        # main loop is on original sequence
        while x < len(seq.seq):
            # if the aligned seq differs, we add lower letter in associated list
            if seq.seq[x] != aligned_seq[y] and x not in aligned_idxs[seq.name]:
                aligned_seqs[seq.name][i] = seq.seq[x].lower()
            x += 1
            y += 1
            i += 1

    # replace remaining `None` with `-` and delete trailing None
    for seq in seqs:
        for i in range(len(aligned_seqs[seq.name])):
            if aligned_seqs[seq.name][i] == None:
                aligned_seqs[seq.name][i] = '-'
        while aligned_seqs[seq.name][-1] == '-':
            aligned_seqs[seq.name] = aligned_seqs[seq.name][:-1]

    # join sequences and return them
    return [Sequence(seq.name, ''.join(aligned_seqs[seq.name])) for seq in seqs]
