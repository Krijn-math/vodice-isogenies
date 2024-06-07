
__all__ = ['Field']

import copy
import collections
import random
import gmpy2

class Field:
    def __init__(self, p):
        p = int(p)
        if not gmpy2.is_prime(p):
            raise ValueError('p must be a prime integer')
        if p % 4 != 3:
            raise NotImplementedError('p must be congruent to 3 modulo 4')
        self.p = p
        self.counts = collections.defaultdict(int)

    def cost(self):
        # these are very rough approximations of the relative costs
        # the actual cost always depends on implementation specifics
        # results are scaled so that a multiplication costs 1 unit
        weights = {
                'mul': 1.,
                'sq': .8,
                'inv': 95.,
                'issq': 110.,
                'sqrt': 800.,
                'add': 0.05,
            }
        return sum(weights[k]*c for k,c in self.counts.items())

    def __repr__(self):
        return f'𝔽{self.p}[√-1]'

    def __eq__(self, other):
        if not isinstance(other, Field):
            return NotImplemented
        return other.p == self.p

    def __copy__(self):
        raise RuntimeError(f'cannot copy {self}')
    __deepcopy__ = __copy__

    def __call__(self, *args, **kwds):
        if len(args) == 1 and isinstance(args[0], FieldElement):
            if args[0].gf != self:
                raise TypeError('element is not in this field')
            return args[0]
        return FieldElement(self, *args, **kwds)

    def zero(self):
        return self()

    def one(self):
        return self(1)

    def i(self):
        return self(0, 1)

    def random(self):
        return self(random.randrange(self.p), random.randrange(self.p))

class FieldElement:
    def __init__(self, gf, re=0, im=0):
        assert isinstance(gf, Field)
        self.gf = gf
        self.re = int(re) % gf.p
        self.im = int(im) % gf.p

    def __repr__(self):
        if not self.im:
            return f'{self.re}'
        if not self.re:
            if self.im == 1:
                return 'i'
            return f'{self.im}*i'
        return f'{self.re}+{self.im}*i'

    def __eq__(self, other):
        if not isinstance(other, FieldElement):
            other = self.gf(other)
        if other.gf != self.gf:
            raise TypeError('trying to compare elements of distinct fields')
        return self.re == other.re and self.im == other.im

    def __bool__(self):
        return bool(self.re or self.im)

    def __neg__(self):
        return self.gf(-self.re, -self.im)

    def __add__(self, other):
        self.gf.counts['add'] += 1
        if not isinstance(other, FieldElement):
            other = self.gf(other)
        if other.gf != self.gf:
            raise TypeError('trying to add elements of distinct fields')
        return self.gf(self.re + other.re, self.im + other.im)
    __radd__ = __add__

    def __mul__(self, other):
        self.gf.counts['mul'] += 1
        if not isinstance(other, FieldElement):
            other = self.gf(other)
        if other.gf != self.gf:
            raise TypeError('trying to multiply elements of distinct fields')
        return self.gf(self.re * other.re - self.im * other.im, self.re * other.im + self.im * other.re)
    __rmul__ = __mul__

    def _square(self):
        self.gf.counts['sq'] += 1
        return self.gf(self.re**2 - self.im**2, 2*self.re*self.im)

    def __sub__(self, other):
        return self + (-other)
    def __rsub__(self, other):
        return (-self) + other

    def __truediv__(self, other):
        if not isinstance(other, FieldElement):
            other = self.gf(other)
        return self * ~other
    def __rtruediv__(self, other):
        if not isinstance(other, FieldElement):
            other = self.gf(other)
        return ~self * other

    def __invert__(self):
        self.gf.counts['inv'] += 1
        s2 = self.re**2 + self.im**2
        try:
            s = pow(s2, -1, self.gf.p)
        except ValueError:
            raise ZeroDivisionError
        ret = self.gf(self.re * s, -self.im * s)
        return ret

    def __pow__(self, e):
        if e == 1:  # nop
            return self
        if e == -1: # inverse
            return ~self
        if e == 2:  # squaring
            return self._square()
        if e < 0:
            return ~self**-e
        r = self.gf.one()
        t = self
        while e:
            if e & 1:
                r *= t
            t *= t
            e >>= 1
        return r

    def sqrt(self):
        # https://ia.cr/2012/685 equation (7)
        self.gf.counts['sqrt'] += 1
        _counts = copy.copy(self.gf.counts)
        e1 = (self.gf.p - 1) // 2
        e2 = (self.gf.p + 1) // 4
        if self**e1 == -1:
            u = self.gf.i()
        else:
            u = (1 + self**e1)**e1
        ret = u * self**e2
        if ret**2 != self:
            raise ArithmeticError('not a square')
        self.gf.counts = _counts
        return ret

    def is_square(self):
        # this can be done much faster, but we're lazy,
        # so we'll just fake it
        self.gf.counts['issq'] += 1
        _counts = copy.copy(self.gf.counts)
        ret = not self or self**((self.gf.p**2 - 1) // 2) == 1
        self.gf.counts = _counts
        return ret


################################################################

import pytest

class Test:
    @staticmethod
    def random_field():
        p = random.randrange(2**99, 2**100)
        while True:
            p = gmpy2.next_prime(p)
            if p % 4 == 3:
                break
        return Field(p)

    @staticmethod
    def test_arith():
        gf = Test.random_field()

        a = gf.random()
        b = gf.random()
        c = gf.random()

        assert gf(a) == a

        assert gf.zero() == 0
        assert gf.one() == 1

        assert a - a == 0
        assert a + 0 == 0 + a == a
        assert a + b == b + a
        assert (a + b) + c == a + (b + c)

        assert a * 1 == 1 * a == a
        assert a * b == b * a
        assert (a * b) * c == a * (b * c)
        assert gf.i()**2 == -1

        assert (a + b) * c == a * c + b * c
        assert a * (b + c) == a * b + a * c

    @staticmethod
    def test_order():
        gf = Test.random_field()
        a = gf.random()
        assert a**gf.p**2 == a

    @staticmethod
    def test_inv():
        gf = Test.random_field()

        with pytest.raises(ZeroDivisionError):
            ~gf.zero()

        while True:
            if (a := gf.random()):
                break
        b = ~a
        assert b * a == a * b == 1

    @staticmethod
    def test_sqrt():
        gf = Test.random_field()

        assert gf.zero().is_square()
        assert gf.zero().sqrt() == gf.zero()

        a = gf.random()**2      # random square
        assert a.is_square()
        b = a.sqrt()
        assert b**2 == a        # correct
        assert a.sqrt() == b    # deterministic

        for _ in range(999):
            a = gf.random()     # square or non-square
            try:
                a.sqrt()
                assert a.is_square()
            except ArithmeticError:
                assert not a.is_square()
                break
        else:
            assert False        # either .sqrt() fails to catch non-squares, or a 2^-999 event

