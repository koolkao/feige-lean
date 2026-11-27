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

## Module status (26 Nov 2026)

**`main` is fully proved**: `OMA.S_opg_sums_of_independent_random_variables_with_unbounded_variance.main`
in `Feige/Main.lean`, statement byte-identical to `feige-statement.lean` (checked by `diff`, and
re-elaborated from the original file text in `scripts/CheckStatement.lean`).
`#print axioms` → `[propext, Classical.choice, Quot.sound]`. No `sorry`/`admit`/`axiom` anywhere.

| Module | File / theorem | Status |
|---|---|---|
| Vendored LeanPool two-point mixture (Prop 2.3, Lemma 2.4) | `Feige/Vendor/LeanPool/*` | compiles (Apache-2.0, unchanged except imports; two files trimmed) |
| No-interior-minimum lemma | `Calculus/NoInteriorMin.lean` `min_endpoints_le_of_stationary` | proved |
| M-Calc-A, Prop 5.2 | `Calculus/HDelta.lean` `min_le_rpow`, `min_le_pow` | proved |
| Finite Bernoulli expectations | `Bernoulli/Ex.lean`, `ZM.lean`, `Moments.lean` | proved |
| Claim 3.1 | `ZM.lean` `one_sub_E_le`; used in `Thm21.lean` | proved |
| Claim 3.2 | `Bernoulli/Claim32.lean` `claim32` (general aᵢ), step in `Step.lean` | proved |
| Thm 2.1, equal-bound case | `Bernoulli/Thm21.lean` `bernoulli_equal_bound` | proved |
| Bernoullification (§2.2, equal means) | `Bernoulli/TwoPointBound.lean` `twoPoint_bound` | proved |
| Product of two-point laws = Bernoulli sum | `Bridge/PiDirac.lean` `pi_twoPt_apply` | proved |
| Mean-one product bound | `Bridge/MeanOne.lean` `pi_meanOne_bound` | proved |
| Shift/scale reduction + `main` | `Feige/Main.lean` | proved |
| M-Calc-B, Prop 5.1 / Claims 3.3–3.4, ordered general Thm 2.1, Thm 1.1 | | not started (not needed for `main`) |
| Boundary limit §3.2 | | not needed (p ∈ [0,1) suffices) |

Timings: every module compiles in < 15 s; full `lake build` of the project ≈ 1 min.

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

1. Before Claim 3.2 and the measure bridge (owner rule), asked Fable (`claude-fable-5-2`) and
   Gemini 4 Neon in parallel for alternative strategies and a critique.
   * Both independently confirmed the Part A math and that only `p < 1` (not `p > 0`, not `w ≤ 1`)
     is needed. Held up in Lean.
   * Fable: isolate a pure-real "step lemma" (no Finsets) and choose the index via
     `wᵢ Dᵢ ≥ 0` handling `wᵢ = 0` directly. **Adopted; worked first try** (`Step.lean`, `exists_index`).
   * Fable/Gemini: shift and scale at the random-variable level with `iIndepFun.comp`, then one
     `iIndepFun_iff_map_fun_eq_pi_map` (AEMeasurable suffices). **Adopted; held.** Instances for
     `Measure.map` of AEMeasurable maps come from `Measure.isProbabilityMeasure_map_iff`.
   * Gemini: avoid `Bool` encodings by proving `Measure.pi (twoPt…) = ∑_S wt • dirac v_S` via
     `Measure.pi_eq` + `Finset.prod_add`. **Adopted; held** (`PiDirac.lean`).
   * Gemini's warnings to check strictness `1 < y` of the latent pair (true a.e. via
     `AugmentedParamNonnegative`) and `0 < μ`, `0 < δ` (hypotheses of `main`) were correct.
   * Gemini's alternative "induct on the support of p with `Function.update p i 0`" was not used.
   * Lemma names suggested from memory were partly wrong in this Mathlib (e.g. `integral_finset_sum`
     is `integral_finsetSum`, `isProbabilityMeasure_map` does not exist); fixed by grep.

## Errors found in Ling's argument

None. Every step used for `main` (Claims 3.1–3.2, §2.2, Prop 2.3/Lemma 2.4 via LeanPool, Prop 5.2)
is machine-checked. Observations: Claim 3.2 does not need `wᵢ ≤ 1` or `pᵢ > 0`; the truncation
`w̄ = min(w,1)` and the boundary limit (§3.2) are therefore unnecessary for the equal-means case.
