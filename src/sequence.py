class Sequence:
    '''
    Class to properly handle sequences

    name : str
        Name of the sequence
    seq : str
        The sequence itself
    '''

    def __init__(self, name, seq):
        self.name = name
        self.seq = seq


def parse_sequences(filename: str) -> list[Sequence]:
    '''
    Parse input file into a list of `Sequence` objects sorted by sequence length
    '''
    seqs = []
    with open(filename) as f:
        content = f.read()

    # we ignore the first element as it should always be an empty string
    for chunk in content.split('>')[1:]:
        # `name` is the first line
        name = chunk.splitlines()[0]
        # `seq` is all the following lines in the chunk
        seq = ''.join(chunk.splitlines()[1:])
        seqs.append(Sequence(name, seq))

    # sort before return
    seqs.sort(key=lambda x: len(x.seq), reverse=True)
    return seqs
