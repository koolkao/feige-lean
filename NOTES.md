# Feige / Samuels Lean formalization: working notes

Target: `main` in `feige-manuscript/inputs/feige-statement.lean` (general δ > 0), following
Ling, *On Samuels' Conjecture* (arXiv:2608.18392v2).

## Build approach

* Lake project with a **path dependency** on the prebuilt Mathlib v4.36.0 at
  `~/dev/pequalnp/pequalnp-proofs/lean/.lake/packages/mathlib` (toolchain `leanprover/lean4:v4.36.0`).
  The other Mathlib dependencies (batteries, aesop, …) are also required by path; Lake prints a
  harmless "remove these dependencies" warning. Prebuilt oleans are reused: first build of a
  file importing `Mathlib` took 23 s total, no Mathlib rebuild.
* Single-file checks: `timeout 900 lake env lean <file>`; full: `timeout 900 lake build`.
* Axiom check: `lake env lean scripts/Axioms.lean`.

## Design decision: route to `main`

For Feige's equal-means case all Bernoulli bounds are equal (`aᵢ = 1/Λ`), so after Claim 3.2
the bound is `P(T<1) ≥ (1 - a/R)^{L/a} = h_D(L/a)` with `D = d/a = δ`, and Prop. 5.2 in its
*real* form (`(1 - 1/(x+D))^x ≥ min(D/(1+D), e⁻¹)` for real `x ≥ 1`) finishes. So Claims 3.3
and 3.4 (and the ordering of the means) are not needed for `main`. They are needed only for the
full Samuels Theorem 1.1, which is planned after `main`.

Also: in the two-point reduction every Bernoulli parameter satisfies `0 ≤ p < 1` (`p = 0` for
atoms), and Claim 3.2 / Claim 3.1 only need `p < 1` (so `P(T<1) > 0`), not `p > 0` and not
`w ≤ 1`. So neither the truncation `w̄ = min(w,1)` nor the boundary limit (§3.2) is needed for
`main`.

## Module status

| Module | File | Status |
|---|---|---|
| Vendored LeanPool two-point mixture | `Feige/Vendor/LeanPool/*` | compiles (vendored, Apache-2.0) |
| No-interior-minimum lemma | `Feige/Calculus/NoInteriorMin.lean` | proved |
| M-Calc-A, Prop 5.2 | `Feige/Calculus/HDelta.lean` (`Samuels.min_le_rpow`, `Samuels.min_le_pow`) | proved, axioms OK |
| Finite Bernoulli expectations | `Feige/Bernoulli/Ex.lean`, `ZM.lean` | proved |
| Claim 3.1 / 3.2 | | in progress |
| M-Calc-B, Prop 5.1 / Claim 3.3 | | not started (not needed for `main`) |
| Measure bridge, `main` | | not started |

## Prop 5.2 proof used (differs from manuscript, avoids limits)

`f(x) = x (log(x+D-1) - log(x+D))`, `f'' = ((2D-1)u - D)/(u²(u-1)²)`, `u = x+D`.
* `D ≤ 1/2`: `log y ≤ (y - 1/y)/2` (y ≥ 1) gives `f' ≥ (1-2D)/(2u(u-1)) ≥ 0`, so `f(x) ≥ f(1)`.
* `D > 1/2`: four-term Taylor bound `log(1-t) ≤ -(t + t²/2 + t³/3 + t⁴/4)` gives `f' < 0` wherever
  `f'' ≥ 0` (polynomial `(6-12D)u³+2u²+u+3 < 0`), so stationary points are strict maxima; and
  `f(N) ≥ -1` once `N(2D-1) ≥ 2D(1-D)`. No-interior-min on `[1, N]` gives `f(x) ≥ min(f 1, -1)`.

## Pitfalls

* `cat > file` with no heredoc blocks on stdin; killed it.
* `push_neg` is deprecated in this Mathlib: use `push Not`.
* `HasDerivAt.sub` of functions yields `(f - g) x` terms: `simp only [Pi.sub_apply]` before `field_simp`.

## Helper consultations

(see below)
