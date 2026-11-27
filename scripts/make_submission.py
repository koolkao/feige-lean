#!/usr/bin/env python3
"""Concatenate the project into one Left to Solve submission file.

Usage: python3 scripts/make_submission.py
Writes
  submission/opg-sums-of-independent-random-variables-with-unbounded-variance.lean   (for CI)
  submission/LocalCheck.lean   (same body, the statement inlined instead of the import; for v4.36)
"""
import re, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ID = "opg-sums-of-independent-random-variables-with-unbounded-variance"
STMT_MOD = "OMAStatements.S_opg_sums_of_independent_random_variables_with_unbounded_variance"
DECL = "OMA.S_opg_sums_of_independent_random_variables_with_unbounded_variance.main"

ORDER = [
    "Vendor/LeanPool/TwoPointMixture",
    "Vendor/LeanPool/MeasurableTwoPointKernel",
    "Vendor/LeanPool/AugmentedTwoPointKernel",
    "Vendor/LeanPool/ProductTwoPointKernel",
    "Vendor/LeanPool/RecursiveLatentProbability",
    "Vendor/LeanPool/MeanOneAugmentedMixture",
    "Vendor/LeanPool/ConditionalProductKernel",
    "Vendor/LeanPool/TwoPointParameters",
    "Vendor/LeanPool/AugmentedParameterization",
    "Vendor/LeanPool/AugmentedLatentSupport",
    "Calculus/NoInteriorMin",
    "Calculus/HDelta",
    "Bernoulli/Ex",
    "Bernoulli/ZM",
    "Bernoulli/Moments",
    "Bernoulli/Step",
    "Bernoulli/Claim32",
    "Bernoulli/Thm21",
    "Bernoulli/TwoPointBound",
    "Bridge/PiDirac",
    "Bridge/MeanOne",
    "Main",
]


def body(rel):
    s = open(os.path.join(ROOT, "Feige", rel + ".lean"), encoding="utf-8").read()
    out = []
    for line in s.splitlines():
        t = line.strip()
        if t == "module" or t.startswith("import ") or t.startswith("public import "):
            continue
        if t == "@[expose] public section":
            continue
        out.append(line)
    return "\n".join(out).strip("\n")


HEADER = f"""/-
Feige's inequality for every δ > 0 (Open Problem Garden: sums of independent random variables
with unbounded variance), following Z. Ling, On Samuels' Conjecture, arXiv:2608.18392v2.

Generated from the Lake project feige-lean by scripts/make_submission.py.
The parts in namespace `Feige` are vendored from LeanPool/lean-pool
(https://github.com/LeanPool/lean-pool, LeanPool/Feige/, commit 9decab6, Apache-2.0,
author Zhengqing Zhou); see the per-part headers below. Everything else is in namespace `Samuels`.
-/
"""

parts = []
for rel in ORDER:
    parts.append(f"/- ===== {rel}.lean ===== -/\nsection\n\n" + body(rel) + "\n\nend")
code = "\n\n".join(parts)

# The project's `main` lives in the statement namespace; rename it for the submission.
main_ns = "namespace OMA.S_opg_sums_of_independent_random_variables_with_unbounded_variance"
assert main_ns in code
code = code.replace(main_ns, "namespace Samuels.Submission")
code = code.replace("end OMA.S_opg_sums_of_independent_random_variables_with_unbounded_variance",
                    "end Samuels.Submission")
code = code.replace("\ntheorem main :", "\ntheorem feige_main :")

tail = f"""

theorem OMA.solution : type_of% @{DECL} :=
  Samuels.Submission.feige_main
"""

sub = f"import {STMT_MOD}\nimport Mathlib\n\n" + HEADER + "\n" + code + tail
os.makedirs(os.path.join(ROOT, "submission"), exist_ok=True)
open(os.path.join(ROOT, "submission", ID + ".lean"), "w", encoding="utf-8").write(sub)

stmt = open(os.path.expanduser("~/dev/lefttosolve/feige-manuscript/inputs/feige-statement.lean"),
            encoding="utf-8").read()
stmt_body = stmt.replace("import Mathlib\n", "", 1)
local = "import Mathlib\n\n" + stmt_body + "\n" + HEADER + "\n" + code + tail
open(os.path.join(ROOT, "submission", "LocalCheck.lean"), "w", encoding="utf-8").write(local)
print(len(sub.encode()), "bytes")
