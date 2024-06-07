
__all__ = ['Curve']

from field import Field, FieldElement

class Curve:
    def __init__(self, A):
        if not isinstance(A, FieldElement):
            raise ValueError('not a field element')
        if A == 2 or A == -2:
            raise ValueError('this curve is singular')
        self.A = A

    def __repr__(self):
        if not self.A:
            return 'y² = x³ + x'
        if self.A == 1:
            return 'y² = x³ + x² + x'
        return f'y² = x³ + {self.A}x² + x'

    def __eq__(self, other):
        if not isinstance(other, Curve):
            return NotImplemented
        return self.A == other.A

    def __call__(self, *args, **kwds):
        return KummerPoint(self, *args, **kwds)

    def zero(self):
        return self()

    def xDBL(self, P):
        if not isinstance(P, KummerPoint):
            raise TypeError('not a point')
        if P.E != self:
            raise ValueError('not a point on this curve')
        a = self.A
        X1, Z1 = P.x, P.z

        # TODO: Hey there! Please implement some nice formulas here :-)

        return # some nice X and Z coordinate here

    def xADD(self, P, Q, PQ):
        if not (isinstance(P, KummerPoint) and isinstance(Q, KummerPoint) and isinstance(PQ, KummerPoint)):
            raise TypeError('not a point')
        if not P.E == Q.E == PQ.E == self:
            raise ValueError('not a point on this curve')
        X2, Z2 = P.x, P.z
        X3, Z3 = Q.x, Q.z
        X1, Z1 = PQ.x, PQ.z

        # TODO: Hey there! Please implement some nice formulas here :-)

        return # some nice X and Z coordinate here

    def is_x_coordinate(self, x):
        return (x * (1 + x * (self.A + x))).is_square()

    def random(self):
        while True:
            x = self.A.gf.random()
            if self.is_x_coordinate(x):
                return self(x)

class KummerPoint:
    def __init__(self, E, x, z=1):
        assert isinstance(E, Curve)
        x,z = map(E.A.gf, (x,z))
        if not x and not z:
            raise ValueError('projective point (0:0) is invalid')
        self.E = E
        self.x = x
        self.z = z

    def __repr__(self):
        x, z = self.x, self.z
        if not z:
            x = x.gf.one()
        else:
            x = x / z
            z = z.gf.one()
        return f'Kummer point ({x}:{z})'

    def _scale(self, s):
        one = self.E.A.gf.one()
        self.x = one if self.x == s else self.x * s
        self.z = one if self.z == s else self.z * s

    def _normalize(self):
        self._scale(~(self.z or self.x))

    def __eq__(self, other):
        if not isinstance(other, KummerPoint):
            return NotImplemented
        if self.E != other.E:
            raise TypeError('points lie on different curves')
        return self.x * other.z == self.z * other.x

    def __bool__(self):
        return bool(self.z)

    def __mul__(self, other):
        if not self.z:
            return self
        n = abs(int(other))
        R0 = self.E(1, 0)
        R1 = self
        for k in reversed(range(n.bit_length())):
            # TODO: Hey there! Please implement a nice Montgomery ladder here :-)
        return R0
    __rmul__ = __mul__

################################################################

import pytest
import random

class Test:
    @staticmethod
    def test_arith():
        gf = Field(2**61 - 1)
        E = Curve(gf(42))
        P = E(1463231399, 340844173)
        R = E(12270276136, 8839223951)
        assert E.xDBL(P) == R

        Q = E(2121144403, 924364499)
        PQ = E(733275521, 967273905)
        S = E(1665137133, 121917320)
        assert E.xADD(P, Q, PQ) == S

    @staticmethod
    def test_ladder():
        gf = Field(2**31 - 1)
        E = Curve(gf(42))
        P = E.random()
        assert 0 * P == E(1, 0)
        assert 1 * P == P
        a = random.randrange(2**99)
        b = random.randrange(2**99)
        assert P * a == a * P
        assert b * (a * P) == a * (b * P)
        assert a * (b * P) == (a * b) * P

    @staticmethod
    def test_curve25519():
        ... #TODO

    ... #TODO

