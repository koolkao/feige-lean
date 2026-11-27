# Heuristic: compares LAST name components only (so e.g. AEMeasurable.of_eval vs Measurable.of_eval is missed).
# The authoritative test is the pinned compile (tools/pinned_check.sh).
import re, os, sys, subprocess
LOCAL = __import__("os").environ.get("LOCAL_PACKAGES", ".lake/packages")  # local Mathlib v4.36 source
PIN = __import__("os").environ.get("PINNED_MATHLIB", "pinned-mathlib")  # source checkout of mathlib 0df444a
DECL=re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|nonrec|scoped)\s+)*(?:theorem|lemma|def|abbrev|instance|alias|structure|class|inductive|irreducible_def|opaque|axiom)\s+([^\s:({\[]+)", re.M)
def names(root, dirs):
    out=set()
    for d in dirs:
        for dp,_,fs in os.walk(os.path.join(root,d)):
            for f in fs:
                if f.endswith(".lean"):
                    s=open(os.path.join(dp,f),encoding="utf-8",errors="ignore").read()
                    for m in DECL.finditer(s):
                        n=m.group(1).split(".")[-1]
                        out.add(n)
                    for m in re.finditer(r"alias\s+⟨([^⟩]*)⟩",s):
                        for n in m.group(1).split(","): out.add(n.strip().split(".")[-1])
    return out
def add_variants(S):
    extra=set()
    for n in S:
        for a,b in [("prod","sum"),("mul","add"),("one","zero"),("pow","nsmul"),("inv","neg"),("div","sub")]:
            if a in n: extra.add(n.replace(a,b))
    return S|extra
LOCAL_INIT=os.path.expanduser("~/.elan/toolchains/leanprover--lean4---v4.36.0/src/lean")
PIN_INIT=os.path.expanduser("~/.elan/toolchains/leanprover--lean4---v4.33.1/src/lean")
PIN_PKG=os.path.expanduser("~/dev/lefttosolve/fc-pinned/.lake/packages")
loc=add_variants(names(LOCAL,["mathlib/Mathlib","batteries/Batteries"])|names(LOCAL_INIT,["Init","Std"]))
pin=add_variants(names(PIN,["Mathlib"])|names(PIN_PKG,["batteries/Batteries"])|names(PIN_INIT,["Init","Std"]))
code=open(sys.argv[1],encoding="utf-8").read()
code=re.sub(r"/-.*?-/","",code,flags=re.S); code=re.sub(r"--.*","",code)
toks=set(re.findall(r"[A-Za-z_][A-Za-z0-9_'.₀₁₂]*",code))
own=set(m.group(1).split(".")[-1] for m in DECL.finditer(code))
flag=[]
for t in sorted(toks):
    n=t.split(".")[-1]
    if n in own or len(n)<3: continue
    if n in loc and n not in pin: flag.append(t)
print("\n".join(flag))
