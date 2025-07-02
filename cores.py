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
ap.add_argument("--cores", action="store_true", help="just show core(s)")
ap.add_argument("--all-cores", action="store_true", help="show all cores")
ap.add_argument(
    "start",
    nargs="*",
    help="starting point for core: 1 or 4 numbers"
)
args = ap.parse_args()
nstart = len(args.start)
if nstart == 1:
    segmented = False
elif nstart == 4:
    segmented = True
else:
    print("start argument must be either 1 or 4 numbers", file=stderr)
    exit(1)

roman_digits = "MDCLXVI"
is_roman = False
for a in args.start:
    for d in a:
        if d in roman_digits:
            is_roman = True
            break
    if is_roman:
        break

def compute_cores(start, operands, pretrace=""):
    assert len(operands) == 4

    def sub(a, b):
        return a - b

    def mult(a, b):
        return a * b

    def div(a, b):
        if b != 0:
            return Fraction(a) / Fraction(b)
        return None
    
    result = set()
    for p in permutations([(sub, "-"), (mult, "*"), (div, "÷")]):
        t = operands[0]
        if pretrace:
            trace = f"{pretrace} → {t}"
        else:
            trace = f"{start}: {t}"
        ok = True
        for (op, name), operand in zip(p, operands[1:]):
            t0 = op(t, operand)
            if not t0:
                ok = False
                break
            t = t0
            trace += f", {name} {operand}"
        if ok and Fraction(t).denominator == 1 and t > 0:
            t = int(t)
            trace += f"; Core = {t}"
            result.add((t, trace))

    return result

def make_seq(digits, part):
    result = []
    i = 0
    for n in part:
        ds = digits[i:i+n]
        result.append(ds)
        i += n
    return result

def min_core(cs):
    if cs:
        return min(cs, key=lambda x: x[0])
    return None

def cores(digits, roman=False, pretrace=""):
    ndigits = len(digits)
    assert ndigits >= 4
    for d in digits:
        if roman:
            assert d in roman_digits
        else:
            assert d >= "0" and d <= "9"
    
    result = set()
    parts = partitions(ndigits, 4)
    for p in parts:
        xs = make_seq(digits, p)
        if roman:
            s = [from_roman(ds) for ds in xs]
        else:
            s = [int(ds) for ds in xs]
        if not s:
            continue
        candidates = compute_cores(
            digits,
            s,
            pretrace=pretrace,
        )
        for core, trace in candidates:
            if core not in result:
                result.add((core, trace))

    m = min_core(result)
    if m:
        core, trace = m
        s = str(core)
        if len(s) >= 4:
            result |= cores(s, pretrace=trace)

    return result

def segmented_cores(segments, roman=False):
    if roman:
        s = [from_roman(seg) for seg in segments]
    else:
        s = [int(seg) for seg in segments]
            
    return compute_cores(' '.join(segments), s)

if segmented:
    if len(args.start) != 4:
        print("error: expected 4 segments", file=stderr)
        exit(1)
    run = segmented_cores(args.start, roman=is_roman)
else:
    if len(args.start) != 1:
        print("error: expected one core", file=stderr)
        exit(1)
    run = cores(args.start[0], roman=is_roman)
    
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
