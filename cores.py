#!/usr/bin/python
# Bart Massey 2025
#
# "Numeric cores" from BluePrince. Group the digits of a
# 4+-digit number into four groups, then combine them using
# the operators -,*,/ in arbitrary order. The "numeric
# cores" are those calculations that give a positive answer.

import argparse
from partitions import partitions
from permutations import permutations
from roman import from_roman

ap = argparse.ArgumentParser()
ap.add_argument("--roman", action="store_true", help="source is roman numeral")
ap.add_argument("--segmented", action="store_true", help="source is pre-segmented")
ap.add_argument("--cores", action="store_true", help="just show cores")
ap.add_argument("start", nargs="*", help="starting point for core")
args = ap.parse_args()

def compute_cores(operands, roman = False):
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
    
    found_cores = set()
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
            if len(str(t)) < 4:
                trace += f" = {t}"
                found_cores.add((t, trace))
            elif not roman:
                found_cores |= cores(str(t))

    return found_cores

def make_seq(digits, part, roman=False, leading_zeros=False):
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
        s = make_seq(digits, p, roman=roman)
        for core, trace in compute_cores(s):
            if core not in result | continuing:
                result.add((core, trace))

    return result

def segmented(segments, roman=False):
    if roman:
        s = [from_roman(seg) for seg in segments]
    else:
        s = [int(seg) for seg in segments]
            
    return compute_cores(s, roman=roman)

def show_tests():
    print("86455", cores("86455"))
    print()
    print("3614", cores("3614"))
    print()
    print("1213", cores("1213"))
    print()
    print(segmented(["M", "CC", "XI", "II"], roman=True))

if args.segmented:
    if len(args.start) != 4:
        print("error: expected 4 segments", file=stdout)
        exit(1)
    run = segmented(args.start, args.roman)
else:
    if len(args.start) != 1:
        print("error: expected one core", file=stdout)
        exit(1)
    run = cores(args.start[0], args.roman)
    
for c, t in run:
    if args.cores:
        print(c)
    else:
        print(t)
