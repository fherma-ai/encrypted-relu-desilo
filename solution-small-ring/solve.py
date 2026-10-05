"""max(0, x) for every element, over CKKS, with DESILO's engine.

The polynomial is the one the OpenFHE and FIDESlib answers to this
specification evaluate: the ReLUFunction component of fairmath/polycircuit,
the winning entry of the FHERMA ReLU challenge's depth-constrained track — a
MILP-optimised polynomial of order 16. So what separates these numbers from
theirs is the library, not the method.

What differs is how it is evaluated. The published component folds the leading
coefficient in by repeated subtraction, because -54 is an integer and the
challenge's depth budget left no room for it as a scalar multiplication. That
constraint is the challenge's, not this specification's, and this library
evaluates a polynomial in one call, so the circuit here is that call.
"""
import numpy as np

from fherma import Inputs, Outputs, Point

#: Coefficients of x^0 … x^16, as published. The last is the integer the
#: component carries separately.
POLYNOMIAL = [
    0.0323949878919212, 0.500001412106499, 2.13483086933591, -4.78160418051218e-05,
    -13.9205486530553, 0.00061641818435605, 70.0957556465309, -0.00388040016141976,
    -213.087053403128, 0.0129145434432087, 385.924971250905, -0.0230082806472531,
    -407.029727261512, 0.0206280915579812, 230.348436664049, -0.00728306945833855,
    -54.0,
]


def init(p: Point, cc):
    return None


def encoding(cc, inp: Inputs) -> list:
    # The whole vector in one packing, slot i holding element i.
    return [np.asarray(inp.xs.data, dtype=float).reshape(-1)]


def run(state, cc, cts: list) -> list:
    return [cc.engine.evaluate_polynomial(
        cts[0], POLYNOMIAL, cc.keys.relinearization)]


def decoding(p: Point, cc, pts: list) -> Outputs:
    from fherma import Tensor

    values = np.real(np.asarray(pts[0])).tolist()
    return Outputs(r=Tensor((p.N,), values[:p.N], "f64"))
