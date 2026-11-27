# A machine-checked proof of Feige's inequality for all δ > 0

This repository contains a Lean 4 / Mathlib formalization of **Feige's small-deviation inequality in its
general form**. Let X₁, …, Xₙ be independent, nonnegative and integrable random variables with E[Xᵢ] ≤ μ,
and suppose μ > 0 and δ > 0. Then

  P( ∑ Xᵢ − E[∑ Xᵢ] < δ μ ) ≥ min( δ/(1+δ), e⁻¹ ).

Feige conjectured this in 2004 (STOC '04; SIAM J. Comput. 35 (2006)). This is the statement of the Open Problem
Garden entry *Sums of independent random variables with unbounded variance*. The δ = 1 case was formalized by
Zhengqing Zhou in [LeanPool/lean-pool](https://github.com/LeanPool/lean-pool) (`LeanPool/Feige/`). As far as we
know, this is the first formalization of the general-δ statement.

The proof follows Zhi Ling, *On Samuels' Conjecture*, [arXiv:2608.18392](https://arxiv.org/abs/2608.18392)
(two-point mixture decomposition, Bernoullification and a Bellman-type induction on weighted Bernoulli sums).
For equal means the formal route is shorter than the paper's. Claim 3.2 together with a real-variable form of the
minimisation lemma closes the argument. Ling's Claims 3.3 and 3.4, the truncation w̄ = min(w, 1) and the
boundary limit (§3.2) are not needed. See `NOTES.md`.

## Main theorem

`OMA.S_opg_sums_of_independent_random_variables_with_unbounded_variance.main` in `Feige/Main.lean`. Its
statement is identical to the one submitted to [Left to Solve](https://lefttosolve.com)
([PR #590](https://github.com/GuillaumeBAUD-coder/open-math-agents/pull/590)). `scripts/CheckStatement.lean`
re-states it independently, and `scripts/Axioms.lean` prints its axioms:

```
depends on axioms: [propext, Classical.choice, Quot.sound]
```

The proof contains no `sorry`, no extra axioms and no `native_decide`.

## Layout

| Path | Content |
|---|---|
| `Feige/Calculus/` | Minimisation lemma for m ↦ (1 − 1/(m+δ))^m (real and integer forms); no-interior-minimum lemma |
| `Feige/Bernoulli/` | Finite weighted-Bernoulli sums; Ling's Claims 3.1–3.2 (Bellman induction); Theorem 2.1, equal-bound case; two-point bound |
| `Feige/Bridge/` | Product of two-point laws as a finite Bernoulli sum; mean-one product bound |
| `Feige/Vendor/LeanPool/` | Two-point mixture decomposition, vendored from LeanPool/lean-pool (Apache-2.0, Zhengqing Zhou and contributors; see the attribution headers) |
| `Feige/Main.lean` | Shift and scale to mean one, then `main` |

## Build

Lean `v4.36.0` and Mathlib `v4.36.0`. Building takes about 2 minutes after the Mathlib cache is downloaded.

```
lake exe cache get
lake build
lake env lean scripts/Axioms.lean
```

## Credits

- Author: Ming-Chih Kao (Stanford University).
- AI assistance: the formalization was developed with Claude (Anthropic). Fable (Anthropic) and Gemini 4 Neon
  (Google) were consulted on proof strategy. The author reviewed the work and takes responsibility for it.
- Vendored code: LeanPool/lean-pool, Apache-2.0.

## License

Apache-2.0 (see `LICENSE`).
