#!/usr/bin/env bash
#
# gen-done-view.sh — regenerate the DONE VIEW of a project's backlog.
#
# The skill does NOT move closed items into done/ (moving rots links and hides history in a
# folder). Instead every artifact keeps a `Status` field IN PLACE, and this generator scans the
# backlog for `Status: ✅ Done` and writes a single read-only view at `<root>/backlog/done/README.md`.
# Closing an item = set its Status to Done, then re-run this (that is what `close_item` automates).
#
# USAGE:  gen-done-view.sh [--root docs] [--apply]
#   --root   docs root (default: docs)
#   --apply  write backlog/done/README.md (without it: print the view to stdout — dry-run)
#
# EXIT: 0 ok · 2 runtime
set -euo pipefail
ROOT="docs"; APPLY=0
while [ $# -gt 0 ]; do case "$1" in
  --root) ROOT="${2:?}"; shift 2;;
  --apply) APPLY=1; shift;;
  *) echo "unknown arg: $1" 1>&2; exit 2;;
esac; done
ROOT="${ROOT%/}"
[ -d "$ROOT/backlog" ] || { echo "no $ROOT/backlog — run the scaffolder first" 1>&2; exit 2; }

today=$(date +%d/%m/%Y 2>/dev/null || echo "DD/MM/YYYY")
python3 - "$ROOT" "$APPLY" "$today" <<'PY'
import sys,re,os,glob
root,apply,today=sys.argv[1],sys.argv[2]=="1",sys.argv[3]
bl=os.path.join(root,"backlog")
# kind label by directory
def kind_of(p):
    if "/bugs/" in p: return "Bug"
    if "/spikes/" in p: return "Spike"
    if "/issues/" in p: return "Issue"
    if "/qa/" in p: return "Q&A"
    if "/support/" in p: return "TX"
    if "/improvements/" in p: return "Improvement"
    if "/features/" in p: return "Feature"
    if "/epics/" in p: return "Epic"
    return "Item"
ID_RE=re.compile(r"^#\s+((?:EP|F|US|BUG|QA|ISS|SPK|TX|PM|RB)-?\d[\w.\-]*)\b",re.I|re.M)
rows=[]
for f in glob.glob(os.path.join(bl,"**","*.md"),recursive=True):
    b=os.path.basename(f)
    if b in ("README.md","_TEMPLATE.md","glossary.md") or "/done/" in f: continue
    txt=open(f,encoding="utf-8").read()
    # a FILLED status line has a single value (no '|' option list) and says Done
    done=any(("done" in ln.lower()) and ("|" not in ln) and re.search(r"status",ln,re.I)
             and ("✅" in ln or re.search(r"\bdone\b",ln,re.I))
             for ln in txt.splitlines() if ln.strip().startswith((">","- ","|")) or "status" in ln.lower())
    if not done: continue
    m=ID_RE.search(txt); ident=m.group(1) if m else os.path.splitext(b)[0]
    h1=next((l for l in txt.splitlines() if l.startswith("# ")),"# ?")
    title=re.sub(r"^\S+\s*[—:\-]\s*","",h1[2:]).strip() or h1[2:].strip()
    rel=os.path.relpath(f,os.path.join(bl,"done"))
    rows.append((kind_of(f),ident,title,rel))
rows.sort(key=lambda r:(r[0],r[1]))
out=[]
out.append("<!-- GENERATED — do not edit by hand. Produced by assets/gen-done-view.sh from every")
out.append("     backlog item whose Status is ✅ Done. Items are NOT moved here — they stay in place;")
out.append("     this is a read-only VIEW. Regenerate after closing an item. -->")
out.append("# Done — closed items (generated view)")
out.append("")
out.append(f"> Read-only view. Every backlog item with **Status ✅ Done** is listed here, **in place** (not moved).")
out.append(f"> Regenerate: `bash <skill>/assets/gen-done-view.sh --root {root} --apply`. Last generated: {today}.")
out.append("")
if rows:
    out.append("| Kind | ID | Title | Where |")
    out.append("| --- | --- | --- | --- |")
    for k,i,t,rel in rows:
        out.append(f"| {k} | `{i}` | {t} | [{rel}]({rel}) |")
    out.append("")
    out.append(f"**Total:** {len(rows)} done.")
else:
    out.append("_No items are Done yet. Set an item's `Status` to ✅ Done and re-run._")
view="\n".join(out)+"\n"
if apply:
    dp=os.path.join(bl,"done"); os.makedirs(dp,exist_ok=True)
    open(os.path.join(dp,"README.md"),"w",encoding="utf-8").write(view)
    print(f"wrote {os.path.join(dp,'README.md')} ({len(rows)} done item(s))")
else:
    print(view)
PY
