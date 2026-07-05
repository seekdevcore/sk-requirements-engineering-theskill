#!/usr/bin/env bash
#
# new-item.sh — the GENERATIVE layer of the engenharia-de-requisitos skill.
#
# Companion of assets/scaffold-structure.sh. Where the scaffolder builds the empty structure,
# THIS creates a single backlog/requirements artifact in ONE command: it allocates the next free
# ID, instantiates the correct _TEMPLATE.md, places it in the right bucket, fills in the id/slug/date,
# and prints the path. This closes the automation gap — creating a spike/bug/issue/… stops being a
# manual "copy template + find next number + fill" chore (which is why it never happened by itself).
#
# USAGE:
#   new-item.sh <kind> <slug> [--title "Business title"] [--root docs] [--apply]
#
#   <kind>   spike | bug | issue | qa | tx | epic | feature | rf | rnf | pm | runbook | adr | sprint
#   <slug>   kebab-case identifier fragment (e.g. "index-strategy", "duplicate-athlete")
#   --title  optional; replaces the <...> placeholder in the H1
#   --root   docs root (default: docs)
#   --apply  actually write the file (without it: dry-run — prints the plan + the resolved id/path)
#
# ID allocation is deterministic: scans the destination bucket for the highest existing number and
# adds 1 (ADR scans BOTH tiers — planning/adrs/ + specs/*/adrs/ — for the one global sequence).
# RNF is slug-based (RNF-<slug>); sprint is number-based (sprint-N).
#
# EXIT: 0 ok · 1 usage · 2 runtime
set -euo pipefail

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TPL="$SELF_DIR/templates"
ROOT="docs"; APPLY=0; TITLE=""
c_grn=$'\033[32m'; c_yel=$'\033[33m'; c_cyn=$'\033[36m'; c_red=$'\033[31m'; c_rst=$'\033[0m'
die(){ printf '%s%s%s\n' "$c_red" "$*" "$c_rst" 1>&2; exit "${2:-1}"; }

[ $# -ge 2 ] || die "usage: new-item.sh <kind> <slug> [--title T] [--root docs] [--apply]"
KIND="$1"; SLUG="$2"; shift 2
while [ $# -gt 0 ]; do case "$1" in
  --title) TITLE="${2:?}"; shift 2;;
  --root) ROOT="${2:?}"; shift 2;;
  --apply) APPLY=1; shift;;
  *) die "unknown arg: $1";;
esac; done
ROOT="${ROOT%/}"
[ -d "$TPL" ] || die "template dir not found: $TPL" 2

# kind -> template | dest dir | id prefix | id style (num2 | num3 | slug | sprint | adr)
case "$KIND" in
  spike)   t=backlog/support-quality-investigation/issues/spikes/_TEMPLATE.md; d=backlog/support-quality-investigation/issues/spikes; pre=SPK; sty=num2;;
  bug)     t=backlog/bugs/_TEMPLATE.md;                                         d=backlog/bugs;                                        pre=BUG; sty=num2;;
  issue)   t=backlog/support-quality-investigation/issues/_TEMPLATE.md;         d=backlog/support-quality-investigation/issues;        pre=ISS; sty=num2;;
  qa)      t=backlog/support-quality-investigation/qa/_TEMPLATE.md;             d=backlog/support-quality-investigation/qa;            pre=QA;  sty=num2;;
  tx)      t=backlog/support-quality-investigation/support/_TEMPLATE.md;        d=backlog/support-quality-investigation/support;       pre=TX;  sty=num2;;
  epic)    t=backlog/epics/_TEMPLATE.md;    d=backlog/epics;    pre=EP;  sty=num2;;
  feature) t=backlog/features/_TEMPLATE.md; d=backlog/features; pre=F;   sty=num2;;
  rf)      t=requirements/RF/_TEMPLATE.md;  d=requirements/RF;  pre=RF;  sty=num3;;
  rnf)     t=requirements/RNF/_TEMPLATE.md; d=requirements/RNF; pre=RNF; sty=slug;;
  pm)      t=postmortems/_TEMPLATE.md;      d=postmortems;      pre=PM;  sty=num2;;
  runbook) t=runbooks/_TEMPLATE.md;         d=runbooks;         pre=RB;  sty=num2;;
  adr)     t=planning/adrs/_TEMPLATE.md;    d=planning/adrs;    pre=ADR; sty=adr;;
  sprint)  t=backlog/sprints/_TEMPLATE.md;  d=backlog/sprints;  pre=sprint; sty=sprint;;
  *) die "unknown kind '$KIND' (spike|bug|issue|qa|tx|epic|feature|rf|rnf|pm|runbook|adr|sprint)";;
esac
[ -f "$TPL/$t" ] || die "template missing: $TPL/$t" 2
DEST="$ROOT/$d"

# ---- allocate the id ----
next_num() {  # next_num <glob-dir...> <regex-capturing-\1-as-number>
  local re="$1"; shift; local max=0 n
  for dir in "$@"; do
    [ -d "$dir" ] || continue
    for f in "$dir"/*.md; do
      [ -e "$f" ] || continue
      if [[ "$(basename "$f")" =~ $re ]]; then n=$((10#${BASH_REMATCH[1]})); [ "$n" -gt "$max" ] && max=$n; fi
    done
  done
  echo $((max + 1))
}
case "$sty" in
  num2)   n=$(next_num "^${pre}-([0-9]+)-" "$DEST"); ID=$(printf '%s-%02d' "$pre" "$n"); FN="$ID-$SLUG.md";;
  num3)   n=$(next_num "^${pre}-([0-9]+)-" "$DEST"); ID=$(printf '%s-%03d' "$pre" "$n"); FN="$ID-$SLUG.md";;
  adr)    n=$(next_num "^ADR-([0-9]+)[-:]" "$ROOT/planning/adrs" "$ROOT"/specs/*/adrs); ID=$(printf 'ADR-%03d' "$n"); FN="$ID-$SLUG.md";;
  sprint) n=$(next_num "^sprint-([0-9]+)-" "$DEST"); ID="sprint-$n"; FN="sprint-$n-$SLUG.md";;
  slug)   ID="RNF-$SLUG"; FN="RNF-$SLUG.md";;
esac
OUT="$DEST/$FN"

printf '%s== new-item ==%s  kind=%s  id=%s\n' "$c_cyn" "$c_rst" "$KIND" "$ID"
if [ -e "$OUT" ]; then die "target already exists: $OUT" 2; fi
[ "$APPLY" -eq 0 ] && { printf '%sDRY-RUN%s would create: %s  (from %s)\n' "$c_yel" "$c_rst" "$OUT" "$t"; printf 'Re-run with --apply to write.\n'; exit 0; }

# ---- instantiate ----
mkdir -p "$DEST"
today=$(date +%d/%m/%Y 2>/dev/null || echo DD/MM/YYYY)
# self-id placeholder in the template: <PREFIX>-NN (num) / RF-NNN / ADR-NNN / RNF-<slug> / Sprint N
python3 - "$TPL/$t" "$OUT" "$pre" "$ID" "$SLUG" "$TITLE" "$today" "$sty" <<'PY'
import sys,re
tpl,out,pre,ID,slug,title,today,sty=sys.argv[1:9]
s=open(tpl,encoding="utf-8").read()
# replace the SELF id placeholder only (not cross-ref placeholders like F-NN / US-NN.M / ADR-NNN)
if sty=="num3": s=s.replace(f"{pre}-NNN",ID)
elif sty=="adr": s=re.sub(r"ADR-NNN(?=[-:\s])",ID,s,count=1); s=s.replace("ADR-NNN:",f"{ID}:")
elif sty=="slug": s=s.replace("RNF-<slug>",ID)
elif sty=="sprint": s=re.sub(r"# Sprint N\b",f"# {ID.replace('sprint-','Sprint ')}",s)
else: s=s.replace(f"{pre}-NN",ID)
if today!="DD/MM/YYYY": s=s.replace("DD/MM/YYYY",today).replace("<DD/MM/YYYY>",today)
if title:  # fill the first <...> placeholder in the H1
    s=re.sub(r"(^#[^\n<]*)<[^>]*>",lambda m:m.group(1)+title,s,count=1,flags=re.M)
open(out,"w",encoding="utf-8").write(s)
PY
printf '%screate%s  %s\n' "$c_grn" "$c_rst" "$OUT"
printf '  next: fill the ↑/↓ traceability links, then reference it from the sprint doc.\n'
