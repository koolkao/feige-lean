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
| M-Calc-B, Prop 5.1 (Claim 3.4) | `Calculus/Prop51.lean` `prop51` | proved |
| Claim 3.3 (rearrangement, any i) | `Bernoulli/Thm21General.lean` `claim33` | proved |
| Thm 2.1, general sorted aᵢ | `Bernoulli/Thm21General.lean` `thm21` | proved |
| Bernoullification, unequal means | `Samuels/Theorem11.lean` `weighted_twoPoint_bound` | proved |
| **Thm 1.1 lower bound (Samuels)** | `Samuels/Theorem11.lean` `samuels_lower`, `samuels_lower_exists` | proved |
| Thm 1.1 sharpness (§2.3) | | not done (optional) |
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

## Other prior art (TauCeti, LeanPool ConcentrationInequalities, atlas-lean)

The coordinator pointed to these after the measure bridge was already proved using only the vendored
LeanPool Feige files plus ~250 lines of our own (`PiDirac.lean`, `MeanOne.lean`, `Main.lean`).
They were not needed and no code from them was used.

## Task A: Left to Solve submission file (prepared, NOT submitted)

* File: `submission/opg-sums-of-independent-random-variables-with-unbounded-variance.lean`
  (≈ 135 KiB, limit 512 KiB), generated by `scripts/make_submission.py` from the project
  (all parts wrapped in `section … end`; `module` / `public import` / `@[expose] public section` lines removed;
  project `main` renamed `Samuels.Submission.feige_main`; ends with
  `theorem OMA.solution : type_of% @OMA.S_….main := Samuels.Submission.feige_main`).
* `submission/LocalCheck.lean`: the same body with the #590 statement inlined instead of the import.
  Compiles on v4.36 with no errors; `#print axioms OMA.solution` → `[propext, Classical.choice, Quot.sound]`.
* `tools/lint.py` passes (run in a scratch copy of the repo with the #590 statement file under `statements/`).
  PR #590's statement file is byte-identical to `inputs/feige-statement.lean`.
* Non-module pitfall found: in a non-module file importing Mathlib, three vendored proofs failed to
  elaborate (`exact` did not unfold a local `def` / `Set.inter` of `setOf`s). Patched the vendored copies
  (type annotations, `rw [Set.setOf_and]`, helper `measurable_twoPointParams_val`); the project still builds.
* Pinned v4.33.1 / mathlib 0df444a checks (no pinned build available):
  - `scripts/pinned_names.py`: every identifier in the file that is declared in local Mathlib/Batteries
    is also declared in the pinned Mathlib (only `congrArg₂` flagged; it is in Batteries and used by pinned Mathlib).
  - `scripts/pinned_sigs.py`: signatures of all used Mathlib declarations agree, except
    `measurable_const` / `measurable_id` gaining implicit `MeasurableSpace` binders (harmless).
  - `push Not` exists in the pinned `Mathlib/Tactic/Push.lean`.
  - **Unverified risks:** tactic behaviour differences (`field_simp`, `simp` simp-set, `positivity`,
    `nlinarith`, `fun_prop`) and elaboration/unification differences; Lean core lemma names
    (`if_pos`, `if_neg` are deprecated only in v4.36); deprecated aliases used locally
    (`Measure.finsetSum_apply`, deprecated 2026-10-23, should be the primary name on the pin).
    The ~40 `field_simp` calls are the main risk (STRATEGY: field_simp is stronger in v4.36).
  - Follow-up: diffed pinned vs local `Mathlib/Tactic/FieldSimp*.lean`, `Positivity/Core.lean`,
    `Linarith/Frontend.lean`: only import/refactoring changes (≤ 54 lines, no behavioural change seen),
    so the `field_simp` risk looks low.

## Task B: Samuels' Theorem 1.1, lower bound (done)

`Samuels.samuels_lower` (n > 0, `0 ≤ m` monotone, `∑ m < λ`, independent nonnegative integrable
`Xᵢ` with `E Xᵢ = mᵢ`): `univ.inf' (qS m λ) ≤ (ℙ {∑ Xᵢ < λ}).toReal`,
`qS m λ i = ∏_{j ≥ i} (1 - mⱼ/(λ - ∑_{k<i} mₖ))`; `samuels_lower_exists` is the `∃ i` form.
Axioms: `[propext, Classical.choice, Quot.sound]`.

Route: zero-mean coordinates → constant 1 (LeanPool `meanOneNormalize` idea), others `Xᵢ/mᵢ`;
mixture (`pi_meanOne_lower`); Bernoullification with `wᵢ = mᵢ(yᵢ-xᵢ)/Λ`, `aᵢ = mᵢ/Λ`, `d = δ/Λ`
(exactly, so no monotonicity in `d` is needed); `Ex` restricted from `univ` to `s = {mᵢ > 0}`
(`Ex_union_irrelevant`, as `wᵢ = 0` off `s`); `thm21` on `s`; `term` identified with `qᵢ`
(factors off `s` are 1). The boundary limit (§3.2) is again unnecessary (`p ∈ [0,1)`).

Consultation (rule 8), before Theorem 2.1 general: Fable and Gemini both confirmed the plan and
that there is no gap at the empty product / pole (the split `L ≤ a_max` vs `L > a_max` forces
`i ≠ max`, so `R > aⱼ` on the whole closed interval). Both proposed a second-derivative-free Claim 3.4
via the integrating factor `R(R-b) g'` being antitone; I kept my already-compiled stationary-point
proof (Gemini's "Strategy 3"). Adopted from Fable: work in logs (no `rpow`), state Claim 3.3 for every
`i`, conclusion as `∃ i ∈ s, term i ≤ Z`, `Z > 0` from Claim 3.1. All held.

Errors in Ling: none found. Remarks for the paper: Claim 3.4 needs `i ≠ max` (true in the proof);
the truncation `w̄`, the boundary limit, and monotonicity of the bound in `d` are not needed.

## Pinned-CI verification (26 Nov 2026) and review follow-up

**Real test on the CI pin** (formal-conjectures 9097e2f, Lean v4.33.1, mathlib 0df444a, at
`~/dev/lefttosolve/fc-pinned`): scratch clone of open-math-agents with the #590 statement as
`statements/<id>.lean` and the submission as `proofs/<id>.lean`, then
`~/dev/lefttosolve/tools/pinned_check.sh <clone> proofs/<id>.lean` (exactly CI's `tools/check.sh`):
`accepted - kernel accepted; axioms within propext, Classical.choice, Quot.sound`, log line
`'OMA.solution' depends on axioms: [propext, Classical.choice, Quot.sound]`. Final file 140,074 bytes; lint OK;
project and `submission/LocalCheck.lean` still compile on v4.36.

The first pinned compile of the previous file had 28 errors (so the earlier static scan was not enough):
* `ite_eq_left`/`ite_eq_right` unknown on v4.33.1 (core rename) → `if_pos`/`if_neg`.
* `AEMeasurable.of_eval` unknown on the pin (it is `aemeasurable_pi_lambda` there, with explicit `f`)
  → `first | exact AEMeasurable.of_eval haeY | exact aemeasurable_pi_lambda _ haeY`.
  The name scanner missed it because it compares last name components only (`Measurable.of_eval` exists).
* Root cause of most other errors: under `open MeasureTheory`, bare `add_apply`/`smul_apply` resolve on the pin
  to generic `IsAddApply`/`IsSMulApply` lemmas with no `Measure` instance → qualified as `Measure.add_apply`/
  `Measure.smul_apply` (exist on both; deprecated aliases on v4.36). This also fixed the `fun_prop` failure
  in `measurable_twoPointMeasure_apply` and two `simp made no progress` errors.
* Set a.e.-equality goals are `Eq` on the pin and `Iff` on v4.36 → `try rw [eq_iff_iff]` before `constructor`.
* `IsProbabilityMeasure (map …)` not found by `infer_instance` on the pin → explicit
  `(Measure.isProbabilityMeasure_map_iff …).mpr inferInstance`.

**Review items (Gemini ranking).**
* (a) `ite_eq_*`: APPLIED, confirmed as a real blocker. `pinned_names.py` now also scans Lean core `Init`/`Std`
  and pinned Batteries; documented its last-component weakness.
* (b) `push Not` → explicit rewrites: REJECTED: `push Not` exists on the pin and all 8 uses compile there.
* (c) `field_simp` hardening: REJECTED: all calls compile on the pin unchanged.
* (d) `fun_prop` → combinators: the one failure (line 387) was caused by `add_apply`, fixed at the root; others
  compile on the pin. No further change.
* (e) `nlinarith` → `linarith`, `Set.mem_ofPred_eq`: not changed (compile on both). `Measure.finsetSum_apply`:
  verified it is the primary name on the pin (deprecated alias on v4.36).
Rationale: once the exact CI check passes, extra edits only add regression risk.

**Inventory** (`Feige.lean` + `Feige/**/*.lean`): 30 files, 4,410 lines (13 vendored LeanPool files, 2,092 lines).
The reviewers' 4,374 lines predate today's portability fixes and header notes. (Earlier "58 files / 7,600 lines"
was wrong.)
