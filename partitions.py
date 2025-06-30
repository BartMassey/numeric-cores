#!/usr/bin/python
# Sequence partitioning.

import math

# Produce all partitions of ndigits digits into ngroups
# groups, in lexical order. Recursive.
def partitions(ndigits, ngroups):
    assert ngroups >= 1
    assert ndigits >= ngroups

    # Base case: take the rest
    if ngroups == 1:
        return [[ndigits]]

    # Recursive case: form all possible
    # groupings of remaining digits.
    excess = ndigits - ngroups
    choices = []
    for i in range(excess + 1):
        for r in partitions(ndigits - i - 1, ngroups - 1):
            choices.append([i + 1] + r)

    return choices

# Produce all partitions of ndigits digits into ngroups
# groups. Non-recursive.
def partitions_nr(ndigits, ngroups):
    assert ngroups >= 1
    assert ndigits >= ngroups

    choices = [[]]
    
    for cur_groups in range(ngroups - 1):
        new_choices = []
        for c in choices:
            nused = sum(c)
            excess = ndigits - nused - (ngroups - cur_groups) + 1
            for d in range(excess):
                new_choices.append([d + 1] + c)
        choices = new_choices

    new_choices = []
    for c in choices:
        nused = sum(c)
        new_choices.append([ndigits - nused] + c)
    choices = new_choices

    return choices

def test_partitions(pfunc, lexical=True):
    for ndigits in range(1, 8):
        for ngroups in range(1, ndigits):
            p = pfunc(ndigits, ngroups)

            # Check group counts
            for e in p:
                assert len(e) == ngroups

            # Check partition sizes
            for e in p:
                assert sum(e) == ndigits
            
            # Check partition uniqueness
            s = set(tuple(e) for e in p)
            assert len(s) == len(p)

            # Check partition count
            n = math.comb(ndigits - 1, ngroups - 1)
            n0 = len(p)
            assert n0 == n, f"{ndigits} {ngroups} {n} {n0}"

            # If lexical, check order
            if lexical:
                dstrings = ["".join(str(e)) for e in p]
                assert dstrings == sorted(dstrings)

if __name__ == "__main__":
    test_partitions(partitions)
    test_partitions(partitions_nr, lexical = False)
