import re, os, sys
LOCAL = __import__("os").environ.get("LOCAL_MATHLIB", ".lake/packages/mathlib/Mathlib")  # local Mathlib v4.36 source
PIN = __import__("os").environ.get("PINNED_MATHLIB", "pinned-mathlib/Mathlib")  # source checkout of mathlib 0df444a
DECL=re.compile(r"^(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|nonrec|scoped)\s+)*(?:theorem|lemma|def|abbrev|instance|alias)\s+([^\s:({\[]+)(.*?)(?=:=|\n\n|\Z| where)", re.M|re.S)
def sigs(root, want):
    out={}
    for dp,_,fs in os.walk(root):
        for f in fs:
            if not f.endswith(".lean"): continue
            s=open(os.path.join(dp,f),encoding="utf-8",errors="ignore").read()
            for m in DECL.finditer(s):
                n=m.group(1).split(".")[-1]
                if n in want:
                    out.setdefault(n,set()).add(re.sub(r"\s+"," ",m.group(2)).strip()[:400])
    return out
code=open(sys.argv[1],encoding="utf-8").read()
code=re.sub(r"/-.*?-/","",code,flags=re.S); code=re.sub(r"--.*","",code)
own=set(m.group(1).split(".")[-1] for m in DECL.finditer(code))
toks=set(t.split(".")[-1] for t in re.findall(r"[A-Za-z_][A-Za-z0-9_'.₀₁₂]*",code))
want={t for t in toks if t not in own and len(t)>=3}
L=sigs(LOCAL,want); P=sigs(PIN,want)
for n in sorted(L):
    if n in P and not (L[n] & P[n]):
        print("==",n); print("  local:",sorted(L[n])[0][:250]); print("  pin  :",sorted(P[n])[0][:250])
