# frac.py -- Partial (add/subtract/multiply/divide) rational arithmetic implementation
# Written in 2021 by Aidan Yaklin
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
# You should have received a copy of the CC0 Public Domain Dedication along
# with this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

import math
import numbers

# Rational arithmetic class
# Stores a rational number as a pair of integers, and defines various operations
# (add, subtract, multiply, divide, and comparisons) on this number. A Rational
# can be converted to a float, but not vice-versa.
# A Rational can be created from its numerator and denominator via the constructor.
# It can also be created from a string formatted as '<numerator>/<denominator>'
# (i.e. '1/2').
class Rational:
    def __init__(self, numerator, denominator):
        """
        Create a Rational. Takes two integers, numerator and denominator. These
        values are adjusted so that the resulting fraction is reduced and has a
        positive denominator.
        """
        gcd = math.gcd(numerator, denominator)
        if denominator < 0:
            numerator = -numerator
            denominator = -denominator
        if gcd == 0:
            gcd = 1 # it's 0/0, don't raise an error
        self.__n = int(numerator / gcd)
        self.__d = int(denominator / gcd)

    def n(self):
        """
        Get the numerator
        """
        return self.__n

    def d(self):
        """
        Get the denominator
        """
        return self.__d

    @staticmethod
    def fromstring(s):
        """
        Create a Rational from a string (i.e. '1/2' or '5').
        """
        v = s.split('/')
        if len(v) == 1:
            return Rational(int(v[0]), 1)
        elif len(v) == 2:
            return Rational(int(v[0]), int(v[1]))
        else:
            raise ValueError('Invalid rational format: %s' % repr(s))

    def __eq__(self, other):
        if isinstance(other, numbers.Number):
            return float(self) == other
        elif type(other) == Rational:
            # both fractions are reduced, so the numerators and denominators should
            # be the same.
            return self.n() == other.n() and self.d() == other.d()
        else:
            return NotImplemented

    def __gt__(self, other):
        if isinstance(other, numbers.Number):
            return float(self) > other
        elif type(other) == Rational:
            return float(self) > float(other)
        else:
            return NotImplemented

    def __ge__(self, other):
        return self.__eq__(other) or self.__gt__(other)

    def __lt__(self, other):
        return not self.__ge__(other)

    def __le__(self, other):
        return not self.__gt__(other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        if self.d() == 1:
            return str(self.n())
        else:
            return '%d/%d' % (self.n(), self.d())

    def __repr__(self):
        return self.__str__()

    def __float__(self):
        return self.n() / self.d()

    def __add__(self, other):
        if type(other) == int:
            return Rational(self.n() + other * self.d(), self.d())
        elif type(other) == Rational:
            if other.d() == self.d():
                return Rational(self.n() + other.n(), self.d())
            else:
                return Rational(self.n() * other.d() + other.n() * self.d(), self.d() * other.d())
        else:
            return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self.__add__(-other)

    def __mul__(self, other):
        if type(other) == int:
            return Rational(self.n() * other, self.d())
        elif type(other) == Rational:
            return Rational(self.n() * other.n(), self.d() * other.d())
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if type(other) == int:
            return Rational(self.n(), self.d() * other)
        elif type(other) == Rational:
            return Rational(self.n() * other.d(), self.d() * other.n())
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        # other / self
        if type(other) == int:
            return Rational(self.d() * other, self.n())
        elif type(other) == Rational:
            return other.__div__(self)
        else:
            return NotImplemented

# Utility function. Takes either a string, an int, or a pair of ints, and converts
# them to a fraction. Valid argument combinations:
# * string   -- creates a Rational with Rational.fromstring()
# * int      -- creates a Rational with the specified numerator and a denominator of 1
# * int, int -- creates a Rational with the specified numerator and denominator.
def fraction(*args):
    if len(args) == 1:
        if type(args[0]) == str:
            return Rational.fromstring(args[0])
        elif type(args[0]) == int:
            return Rational(args[0], 1)
    elif len(args) == 2 and type(args[0]) == int and type(args[1]) == int:
        return Rational(args[0], args[1])
    raise ValueError("Bad arguments: %s" % ','.join((type(x).__name__ for x in args)))
