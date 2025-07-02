#!/usr/bin/python
# Bart Massey 2025
#
# "Numeric core" from BluePrince. Group the digits of a
# 4+-digit number into four groups, then combine them using
# the operators -,*,/ in arbitrary order. If a positive
# integer of four or more digits is produced, iterate the
# process. The "numeric core" is the calculations that give
# the smallest positive integer answer.

import argparse
from fractions import Fraction
from partitions import partitions
from permutations import permutations
from roman import from_roman
from sys import stderr

ap = argparse.ArgumentParser()
ap.add_argument("--roman", action="store_true", help="source is roman numeral")
ap.add_argument("--segmented", action="store_true", help="source is pre-segmented")
ap.add_argument("--cores", action="store_true", help="just show core(s)")
ap.add_argument("--all-cores", action="store_true", help="show all cores")
ap.add_argument("start", nargs="*", help="starting point for core")
args = ap.parse_args()

def compute_cores(start, operands, roman = False, pretrace=""):
    assert len(operands) == 4

    def sub(a, b):
        return a - b

    def mult(a, b):
        return a * b

    def div(a, b):
        if b != 0:
            return Fraction(a) / Fraction(b)
        return None
    
    found_cores = set()
    for p in permutations([(sub, "-"), (mult, "*"), (div, "÷")]):
        t = operands[0]
        trace = f"{start}: {t}"
        if pretrace:
            trace = f"{pretrace}, {trace}"
        ok = True
        for (op, name), operand in zip(p, operands[1:]):
            t0 = op(t, operand)
            if not t0:
                ok = False
                break
            t = t0
            trace += f", {name} {operand}"
        if ok and t.is_integer() and t > 0:
            t = int(t)
            if len(str(t)) < 4:
                trace += f"; Core = {t}"
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
        if not s:
            continue
        for core, trace in compute_cores(digits, s):
            if core not in result | continuing:
                result.add((core, trace))

    return result

def min_core(cs):
    if cs:
        return min(cs, key=lambda x: x[0])
    return None

def segmented_cores(segments, roman=False):
    if roman:
        s = [from_roman(seg) for seg in segments]
    else:
        s = [int(seg) for seg in segments]
            
    return compute_cores(''.join(segments), s, roman=roman)

def smoke_tests():
    print("86455", cores("86455"))
    print()
    print("3614", cores("3614"))
    print()
    print("1213", cores("1213"))
    print()
    print(segmented(["M", "CC", "XI", "II"], roman=True))

if args.segmented:
    if len(args.start) != 4:
        print("error: expected 4 segments", file=stderr)
        exit(1)
    run = segmented_cores(args.start, roman=args.roman)
else:
    if len(args.start) != 1:
        print("error: expected one core", file=stderr)
        exit(1)
    run = cores(args.start[0], roman=args.roman)
    
if args.all_cores:
    if run:
        for c, t in run:
            if args.cores:
                print(c)
            else:
                print(t)
    else:
        print("no cores")
else:
    core = min_core(run)
    if core:
        if args.cores:
            print(core[0])
        else:
            print(core[1])
    else:
        print("no core")
