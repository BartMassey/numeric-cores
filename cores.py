#!/usr/bin/python
# "Numeric cores" from BluePrince
# Group the digits of a 4+-digit number
# into four groups, then combine them
# using the operators -,*,/ in arbitrary
# order. The "numeric cores" are those
# calculations that give a positive answer

from partitions import partitions
from permutations import permutations

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

def make_seq(digits, part):
    result = []
    i = 0
    for n in part:
        result.append(int(digits[i:i+n]))
        i += n
    return result

def cores(digits):
    ndigits = len(digits)
    assert ndigits >= 4
    for d in digits:
        assert d >= "1" and d <= "9"
    
    result = set()
    continuing = set()
    parts = partitions(ndigits, 4)
    for p in parts:
        seq = make_seq(digits, p)
        for core, trace in compute_cores(seq):
            if core not in result | continuing:
                result.add(core)
                print(trace)

    return result

def roman():
    for core, trace in compute_cores([1000, 200, 11, 2]):
        print(core, trace)

if __name__ == "__main__":
    print("86455", cores("86455"))
    print("3614", cores("3614"))
    print("1213", cores("1213"))

    print()
    roman()
