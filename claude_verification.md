# Verification of `int.star-contains` predicate

## cvc5 debug-check-model output

```bash
 ~/all/cvc5/liastar/build/bin/cvc5 --debug-check-models /home/mudathir/all/SQLSolver/cvc5/spark/query090-call-2.smt2 --dag-thresh=0
getValue((lambda ((u26 Int) (u30 Int) (u28 Int) (u27 Int) (u29 Int) (u22 Int) (u21 Int)) (and (= u26 (ite (and (= u28 1) (= u29 u22)) u27 0)) (= u30 (ite (and (= u28 1) (= u21 1) (= u29 u22)) u27 0))))): (lambda ((u26 Int) (u30 Int) (u28 Int) (u27 Int) (u29 Int) (u22 Int) (u21 Int)) (and (= u26 (ite (and (= u28 1) (= u29 u22)) u27 0)) (= u30 (ite (and (= u28 1) (= u21 1) (= u29 u22)) u27 0))))
getValue(u1): 1
getValue(u0): 0
getValue(u28): 1
getValue(u27): 1
getValue(u29): 4
getValue(u22): 4
getValue(u21): 1
 THEORY_ARITH has an asserted fact that the model may not satisfy.
The fact: (int.star-contains (lambda ((u26 Int) (u30 Int) (u28 Int) (u27 Int) (u29 Int) (u22 Int) (u21 Int)) (and (= u26 (ite (and (= u28 1) (= u29 u22)) u27 0)) (= u30 (ite (and (= u28 1) (= u21 1) (= u29 u22)) u27 0)))) u1 u0 u28 u27 u29 u22 u21)
Model value: (int.star-contains (lambda ((u26 Int) (u30 Int) (u28 Int) (u27 Int) (u29 Int) (u22 Int) (u21 Int)) (and (= u26 (ite (and (= u28 1) (= u29 u22)) u27 0)) (= u30 (ite (and (= u28 1) (= u21 1) (= u29 u22)) u27 0)))) 1 0 1 1 4 4 1)
sat
```
We need to check the model satisfies the lambda predicate above. 

## The predicate

```
(int.star-contains
  (lambda ((u26 Int) (u30 Int) (u28 Int) (u27 Int) (u29 Int) (u22 Int) (u21 Int))
    (and
      (= u26 (ite (and (= u28 1) (= u29 u22)) u27 0))
      (= u30 (ite (and (= u28 1) (= u21 1) (= u29 u22)) u27 0))))
  u1 u0 u28 u27 u29 u22 u21)
```

## Model values

Arguments `(u1, u0, u28, u27, u29, u22, u21) = (1, 0, 1, 1, 4, 4, 1)`.

## Question

Is `(1, 0, 1, 1, 4, 4, 1)` in the LIA* (additive Kleene closure) of the lambda?
That is, can it be written as a sum of zero or more non-negative integer tuples
each satisfying the lambda body?

## Lambda semantics

For a summand `(u26, u30, u28, u27, u29, u22, u21)` to satisfy the body:

- `u26 = ite(u28 = 1 ∧ u29 = u22, u27, 0)`
- `u30 = ite(u28 = 1 ∧ u21 = 1 ∧ u29 = u22, u27, 0)`

## Single-tuple check (n = 1) — fails

Plugging the target tuple directly:

- `u26 = ite(1 = 1 ∧ 4 = 4, 1, 0) = 1` ✓ (matches 1)
- `u30 = ite(1 = 1 ∧ 1 = 1 ∧ 4 = 4, 1, 0) = 1` ✗ (target is 0)

The target itself does not satisfy the lambda.

## Two-tuple decomposition (n = 2) — works

All variables are non-negative. Since the target's `u30 = 0`, every summand must
have `u30 = 0`.

**T₁ = (u26=1, u30=0, u28=1, u27=1, u29=4, u22=4, u21=0)**

- `u26 = ite(1 = 1 ∧ 4 = 4, 1, 0) = 1` ✓
- `u30 = ite(1 = 1 ∧ 0 = 1 ∧ 4 = 4, 1, 0) = 0` ✓ (guard false because u21 ≠ 1)

**T₂ = (u26=0, u30=0, u28=0, u27=0, u29=0, u22=0, u21=1)**

- `u26 = ite(0 = 1 ∧ 0 = 0, 0, 0) = 0` ✓
- `u30 = ite(0 = 1 ∧ 1 = 1 ∧ 0 = 0, 0, 0) = 0` ✓

Componentwise sum:

```
T₁ + T₂ = (1+0, 0+0, 1+0, 1+0, 4+0, 4+0, 0+1)
        = (1,   0,   1,   1,   4,   4,   1)
```

This matches the target.

## Conclusion

**The predicate is TRUE.** The tuple `(1, 0, 1, 1, 4, 4, 1)` is in the LIA*
closure of the lambda via the decomposition T₁ + T₂, where both T₁ and T₂
satisfy the lambda body.
