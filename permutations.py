#!/usr/bin/python
# Sequence permutations.

import math

# Produce all permutations of the input sequence.
# Recursive.
def permutations(seq):
    nseq = len(seq)

    # Base case: no permutations
    if nseq <= 1:
        return [seq]

    # Recursive case: prepend all possible permutations
    # of remaining elements
    perms = []
    for i in range(nseq):
        # Place target element at beginning.
        seq[i], seq[0] = seq[0], seq[i]

        # Get all the permutations starting with this
        # element.
        for p in permutations(seq[1:]):
            perms.append([seq[0]] + p)

        # Restore the sequence.
        seq[i], seq[0] = seq[0], seq[i]

    return perms

def test_permutations():
    for ndigits in range(5):
        s = [i for i in range(1, ndigits + 1)]
        perms = permutations(s)

        # Check permutedness.
        for p in perms:
            assert(s == sorted(p))

        # Check number of unique permutations.
        nperms = math.factorial(ndigits)
        pset = {tuple(p) for p in perms}
        assert len(pset) == nperms

if __name__ == "__main__":
    test_permutations()
