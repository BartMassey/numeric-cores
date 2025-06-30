#!/usr/bin/python3
# Bart Massey 2025
#
# Roman Numeral conversions.

digit_values = {
    "M" : 1000,
    "D" : 500,
    "C" : 100,
    "L" : 50,
    "X" : 10,
    "V" : 5,
    "I" : 1,
}

class RomanException(Exception):
    pass

# Convert a non-empty Roman numeral (in all-caps) into a
# number.  Allows some irregular forms like "XIIIV" == 12.
# Raises RomanException on malformed input.

def from_roman(digits):
    assert len(digits) > 0
    ds = list(reversed(digits))

    d = ds[0]
    if d not in digit_values:
        raise RomanException(f"bad roman digit {d}")
    t = digit_values[d]
    borrow_end = t
    borrow_cur = None
    for d in ds[1:]:
        if d not in digit_values:
            raise RomanException(f"bad roman digit {d}")
        dv = digit_values[d]
        if dv < borrow_end:
            if borrow_cur and borrow_cur != dv:
                raise RomanException(f"malformed (mixed) numeral {digits}")
            t -= dv
            if t <= 0:
                raise RomanException(f"malformed (underflow) numeral {digits}")
        else:
            t += dv
            borrow_end = dv

    return t

if __name__ == "__main__":
    tests = [
        ("MCMXLVI", 1946),
        ("MCMXLIV", 1944),
        ("MCMXLVII", 1947),
        ("IIID", 497),
        ("IMIIIIV", 1000),
        ("MIDIIIIV", 1500),
    ]
    for roman, numeral in tests:
        n = from_roman(roman)
        assert n == numeral, f"{roman} {numeral} {n}"
