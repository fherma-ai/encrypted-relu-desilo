# max(0, x) for every element over CKKS — DESILO

> Implements [`relu` / `f64@1.0.0`](https://www.fherma.io/kernels/relu/specifications/f64)
> on the FHERMA kernel catalogue, with [DESILO FHE](https://fhe.desilo.dev/).

```text
kernel relu<N: u32>(
    %xs: secret<tensor<N x f64>>,
) -> %r: secret<tensor<N x f64>>
```

## The polynomial is not ours

It is the one the OpenFHE and FIDESlib answers to this specification evaluate:
the MILP-optimised polynomial of order 16 from the ReLUFunction component of
[polycircuit](https://github.com/fairmath/polycircuit) (Apache-2.0), the
winning entry of the FHERMA ReLU challenge's depth-constrained track. Its
seventeen coefficients are in `solve.py`, unchanged.

So what separates this measurement from the others on the board is the library,
not the method.

## What differs is how it is evaluated

The published component folds the leading coefficient in by repeated
subtraction, because -54 is an integer and the challenge's depth budget left no
room for it as a scalar multiplication. That constraint was the challenge's,
not this specification's, and this library evaluates a polynomial in one call,
so the measured circuit is that call.

## Accuracy

The specification holds the worst error to 0.05 and asks that 85% of elements
land within 1e-3. This answer reaches 0.030 and 88.3% at N = 1024 — the share
is a property of the polynomial, which cannot follow the kink at x = 0. The
level budget is 5, which is what the circuit spends.

## Running it yourself

In the `fherma/desilo:1.17.0` image, or anywhere the wheel installs:

```sh
pip install --no-cache-dir --target . desilofhe==1.17.0
python main.py <point directory>
```

A point directory is what the specification's testing bundle writes with
`main.py make`; the same bundle judges the result with `main.py verify`.

## Layout

```
solution/
  solve.py       the four functions — the only file written by hand
  config.jsonc   the engine: scheme, mode, level budget, which keys
  fherma.toml    what it implements, and with what
  envelope.py    generated — engine, keys, encryption. Holds the secret key
  main.py        generated — the measured loop
  fherma.py      generated — the types, from the signature
```

Everything but `solve.py` and `config.jsonc` is emitted by `fherma-lang` from the
specification's signature and replaced at every measurement, so a solution
cannot drift from the contract it claims to meet.

## Licence

The solution is Apache-2.0. The DESILO library is not redistributed here: the
build installs it from PyPI, under its own licence, which permits
non-commercial use.
