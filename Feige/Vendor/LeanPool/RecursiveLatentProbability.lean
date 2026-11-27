/-
Copyright (c) 2026 Zhengqing Zhou and contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Zhengqing Zhou, GPT-5.6 Pro
-/
-- Vendored from LeanPool/lean-pool (https://github.com/LeanPool/lean-pool),
-- file LeanPool/Feige/RecursiveLatentProbability.lean at commit 9decab6341e6b0fd82bd7f9763a5dd7a9ce8778d, Apache-2.0 (see LICENSE in this folder).
-- Changes: import paths renamed from `LeanPool.Feige.*` to `Feige.Vendor.LeanPool.*`.

module

public import Feige.Vendor.LeanPool.ProductTwoPointKernel

/-!
# Probability instance for the recursive latent product
-/

@[expose] public section

open MeasureTheory

namespace Feige

noncomputable section

instance recursiveAugmentedLatent_isProbability
    (n : ℕ)
    (latent : Fin n → Measure AugmentedTwoPointParams)
    [∀ i, IsProbabilityMeasure (latent i)] :
    IsProbabilityMeasure (recursiveAugmentedLatent n latent) := by
  induction n with
  | zero =>
      unfold recursiveAugmentedLatent
      infer_instance
  | succ n ih =>
      let : ∀ i : Fin n,
          IsProbabilityMeasure (latent (Fin.succ i)) :=
        fun i ↦ inferInstance
      let : IsProbabilityMeasure
          (recursiveAugmentedLatent n
            (fun i ↦ latent (Fin.succ i))) :=
        ih (fun i ↦ latent (Fin.succ i))
      unfold recursiveAugmentedLatent
      infer_instance

end

end Feige
