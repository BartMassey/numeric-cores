#!/usr/bin/python
# Bart Massey 2025
#
# "Numeric cores" from BluePrince. Group the digits of a
# 4+-digit number into four groups, then combine them using
# the operators -,*,/ in arbitrary order. The "numeric
# cores" are those calculations that give a positive answer.

from partitions import partitions
from permutations import permutations
from roman import from_roman

def compute_cores(operands):
    assert len(operands) == 4

    def sub(a, b):
        return a - b

    def mult(a, b):
        return a * b

    def div(a, b):
        if a % b == 0:
            return a // b
        else:
            return None
    
    cores = set()
    for p in permutations([(sub, "-"), (mult, "*"), (div, "/")]):
        t = operands[0]
        trace = f"{t}"
        ok = True
        for (op, name), operand in zip(p, operands[1:]):
            t0 = op(t, operand)
            if not t0 or t0 <= 0:
                ok = False
                break
            t = t0
            trace += f" {name} {operand}"
        if ok:
            trace += f" = {t}"
            cores.add((t, trace))

    return cores

def make_seq(digits, part, roman = False, leading_zeros = False):
    result = []
    i = 0
    for n in part:
        ds = digits[i:i+n]
        if not leading_zeros and ds[0] == "0":
            return None
        if roman:
            j = from_roman(ds)
        else:
            j = int(ds)
        result.append(j)
        i += n
    return result

def cores(digits, roman=False):
    ndigits = len(digits)
    assert ndigits >= 4
    for d in digits:
        if roman:
            assert d in "MDCLXVI"
        else:
            assert d >= "0" and d <= "9"
    
    result = set()
    continuing = set()
    parts = partitions(ndigits, 4)
    for p in parts:
        seq = make_seq(digits, p, roman)
        for core, trace in compute_cores(seq):
            if core not in result | continuing:
                result.add(core)
                print(trace)

    return result

def segmented(segments, roman = False):
    if roman:
        s = [from_roman(seg) for seg in segments]
    else:
        s = [int(seg) for seg in segments]
            
    return compute_cores(s)

if __name__ == "__main__":
    print("86455", cores("86455"))
    print("3614", cores("3614"))
    print("1213", cores("1213"))

    print(segmented(["M", "CC", "XI", "II"], roman = True))
