# numeric-cores: BluePrince puzzle
Bart Massey 2025

"Numeric cores" [puzzle](https://blue-prince.fandom.com/wiki/Numeric_Core)
from [BluePrince](https://www.blueprincegame.com/).

Group the digits of a 4-or-more-digit number into four
groups, then combine them using the operators -, *, / in
arbitrary order. Iterate until a 3-or-less-digit number is
found.  The "numeric core" is the calculation that gives the
smallest positive integer, without division by zero at any
point.

This solver assumes no zero digits in the input, as things
get confusing otherwise. Roman numerals are available
(because reasons) but a bit fragile.

Run with `python cores.py --help` in the repo directory to
see the possible arguments, then proceed accordingly.

# Acknowledgments

Thanks to Cousin Rob for introducing me to the
puzzle. Thanks to GrinGene at
<https://blue-prince.fandom.com> for corrections.

## License

This work is made available under the "MIT License". See the
file `LICENSE.txt` in this distribution for license terms.
