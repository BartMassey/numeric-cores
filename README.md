# numeric-cores: BluePrince puzzle
Bart Massey 2025

"Numeric cores" [puzzle](https://blue-prince.fandom.com/wiki/Numeric_Core)
from [BluePrince](https://www.blueprincegame.com/).

Group the digits of a 4-or-more-digit number into four
groups, then combine them using the operators -, *, / in
arbitrary order. The "numeric core" is the calculation that
gives the smallest positive integer, without division by
zero at any point. If no 3-or-less-digit core is found,
iterate on the smallest current core.

Roman numerals are available (because reasons). No iteration
will be done when finding Roman cores.

Run with `python cores.py --help` in the repo directory to
see the possible arguments, then proceed accordingly. Known
to work with Python 3.10 or later.

# Acknowledgments

Thanks to Cousin Rob for introducing me to the
puzzle. Thanks to GrinGene at
<https://blue-prince.fandom.com> for corrections.

## License

This work is made available under the "MIT License". See the
file `LICENSE.txt` in this distribution for license terms.
