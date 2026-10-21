#!/usr/bin/env python3
"""SLR v2 pipeline: ingest -> dedup -> filter -> recall -> snowball -> export.

Standard library only (openpyxl is needed for `coding-form` only).
Every command appends a JSON line to <run_dir>/run_log.jsonl with its
arguments, input/output counts and the SHA-256 of this script, so the
PRISMA counts can be reproduced from the log (`prisma` command).

Typical use (from the repository root):
  P=v2/pipeline/slr_pipeline.py; RUN=v2/runs/2026-11-ebsco-v2
  python $P ingest   --run $RUN --db EBSCO exports/ebsco_*.csv
  python $P dedup    --run $RUN
  python $P filter   --run $RUN --config v2/pipeline/filter_rules.json
  python $P recall   --run $RUN --gold v2/protocol/gold_set.csv
  python $P export   --run $RUN
  python $P snowball --run $RUN --seeds included.csv --direction both
  python $P prisma   --run $RUN
"""
import argparse, csv, difflib, hashlib, html, json, os, re, sys, time, unicodedata
import urllib.parse, urllib.request
from datetime import datetime, timezone

csv.field_size_limit(sys.maxsize)
FIELDS = ["record_id", "source_db", "source_file", "an", "title", "abstract", "authors", "year",
          "venue", "doc_type", "language", "doi", "url", "keywords", "peer_reviewed", "retracted"]

# ----------------------------------------------------------------- utilities
def norm_title(t):
    t = unicodedata.normalize("NFKD", html.unescape(t or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]", "", t)

def norm_doi(d):
    if not d:
        return ""
    m = re.search(r"10\.\d{4,9}/[^\s\"'<>;,]+", str(d))
    return m.group(0).rstrip(".)]").lower() if m else ""

def year_of(*vals):
    for v in vals:
        m = re.search(r"(19|20)\d{2}", str(v or ""))
        if m:
            return m.group(0)
    return ""

def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

def write_csv(path, rows, fields):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

def sha256_self():
    with open(__file__, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]

def log(run, command, **info):
    os.makedirs(run, exist_ok=True)
    entry = {"utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "command": command,
             "script_sha256_16": sha256_self(), **info}
    with open(os.path.join(run, "run_log.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(json.dumps({k: v for k, v in entry.items() if k not in ("utc", "script_sha256_16")}, ensure_ascii=False))

# ------------------------------------------------------------------ parsers
ALIASES = {  # normalised header -> schema field
    "title": "title", "itemtitle": "title", "articletitle": "title", "documenttitle": "title", "ti": "title",
    "abstract": "abstract", "ab": "abstract",
    "authors": "authors", "author": "authors", "contributors": "authors", "au": "authors",
    "year": "year", "publicationyear": "year", "publicationdate": "year", "coverdate": "year", "py": "year",
    "source": "venue", "publicationtitle": "venue", "journal": "venue", "sourcetitle": "venue", "booktitle": "venue",
    "doctypes": "doc_type", "pubtypes": "doc_type", "contenttype": "doc_type", "documenttype": "doc_type", "type": "doc_type",
    "language": "language", "la": "language",
    "doi": "doi", "itemdoi": "doi", "doids": "doi", "identifiers": "doi",
    "url": "url", "link": "url", "plink": "url",
    "subjects": "keywords", "keywords": "keywords", "authorkeywords": "keywords",
    "an": "an", "accessionnumber": "an",
    "peerreviewed": "peer_reviewed", "retracted": "retracted",
}

def from_csv(path):
    out = []
    for row in read_csv(path):
        rec = {}
        for k, v in row.items():
            f = ALIASES.get(re.sub(r"[^a-z]", "", (k or "").lower()))
            if f and v not in (None, "", "None", "null") and not rec.get(f):
                rec[f] = str(v).strip()
            elif f == "doc_type" and v and rec.get(f) and v not in rec[f]:
                rec[f] += "; " + str(v).strip()   # keep both docTypes and pubTypes
        out.append(rec)
    return out

def from_ris(path):
    out, rec = [], {}
    tagmap = {"TI": "title", "T1": "title", "AB": "abstract", "N2": "abstract", "AU": "authors", "A1": "authors",
              "PY": "year", "Y1": "year", "DA": "year", "JO": "venue", "JF": "venue", "T2": "venue", "BT": "venue",
              "DO": "doi", "UR": "url", "LA": "language", "KW": "keywords", "AN": "an", "TY": "doc_type"}
    for line in open(path, encoding="utf-8-sig", errors="replace"):
        m = re.match(r"^([A-Z][A-Z0-9])  - ?(.*)$", line.rstrip("\n"))
        if not m:
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "ER":
            out.append(rec); rec = {}; continue
        f = tagmap.get(tag)
        if f in ("authors", "keywords") and rec.get(f):
            rec[f] += "; " + val
        elif f and not rec.get(f):
            rec[f] = val
    return out

def from_bib(path):
    text = open(path, encoding="utf-8-sig", errors="replace").read()
    out = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]*),(.*?)\n\}", text, re.S):
        rec = {"doc_type": m.group(1), "an": m.group(2).strip()}
        for fm in re.finditer(r"(\w+)\s*=\s*(\{(?:[^{}]|\{[^{}]*\})*\}|\"(?:[^\"\\]|\\.)*\"|\d+)\s*,?", m.group(3), re.S):
            k, v = fm.group(1).lower(), fm.group(2).strip()
            v = re.sub(r"\s+", " ", v[1:-1] if v[0] in "{\"" else v).replace("{", "").replace("}", "")
            f = {"journal": "venue", "booktitle": "venue", "author": "authors", "keywords": "keywords"}.get(k, k)
            if f in FIELDS and v and v != "null":
                rec[f] = v
        out.append(rec)
    return out

def from_schema_csv(path):
    return read_csv(path)

# ----------------------------------------------------------------- commands
def cmd_ingest(a):
    allrecs, per_file = [], {}
    for path in a.files:
        ext = os.path.splitext(path)[1].lower()
        if ext == ".csv":
            with open(path, encoding="utf-8-sig") as f:
                header = f.readline()
            recs = from_schema_csv(path) if header.startswith("record_id,") else from_csv(path)
        elif ext in (".ris", ".txt"):
            recs = from_ris(path)
        elif ext == ".bib":
            recs = from_bib(path)
        else:
            sys.exit(f"unsupported file type: {path}")
        base = os.path.basename(path)
        for i, r in enumerate(recs, 1):
            if r.get("record_id"):          # already in schema (e.g. snowball output)
                allrecs.append(r); continue
            r["source_db"] = a.db
            r["source_file"] = base
            r["doi"] = norm_doi(r.get("doi")) or norm_doi(r.get("url"))
            r["year"] = year_of(r.get("year"))
            key = r.get("an") or r["doi"] or hashlib.sha1(f"{base}#{i}".encode()).hexdigest()[:12]
            r["record_id"] = f"{a.db}:{key}"
            allrecs.append(r)
        per_file[base] = len(recs)
    missing_title = sum(1 for r in allrecs if not r.get("title"))
    out = os.path.join(a.run, "01_records_ingested.csv")
    prev = read_csv(out) if (a.append and os.path.exists(out)) else []
    seen = {r["record_id"] for r in prev}
    for r in allrecs:                      # guarantee unique record_ids (e.g. same DOI twice in one export)
        rid, n = r["record_id"], 1
        while r["record_id"] in seen:
            n += 1; r["record_id"] = f"{rid}~{n}"
        seen.add(r["record_id"])
    write_csv(out, prev + allrecs, FIELDS)
    log(a.run, "ingest", db=a.db, files=per_file, records_in=len(allrecs), records_total=len(prev) + len(allrecs),
        missing_title=missing_title)

def _quality(r):
    return (bool(r.get("doi")), len(r.get("abstract", "")), bool(r.get("year")))

def cmd_dedup(a):
    recs = read_csv(os.path.join(a.run, "01_records_ingested.csv"))
    recs.sort(key=_quality, reverse=True)       # best-described record first becomes the kept one
    parent = list(range(len(recs)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]; i = parent[i]
        return i
    pairs = []
    def union(i, j, method, score):
        ri, rj = find(i), find(j)
        if ri != rj:
            keep, drop = min(ri, rj), max(ri, rj)
            member = j if rj == drop else i       # the record that triggered the merge on the dropped side
            parent[drop] = keep
            pairs.append({"kept": recs[keep]["record_id"], "duplicate": recs[member]["record_id"],
                          "method": method, "score": score})
    by_doi, by_title = {}, {}
    for i, r in enumerate(recs):
        d = r.get("doi")
        if d:
            if d in by_doi: union(by_doi[d], i, "doi", 1.0)
            else: by_doi[d] = i
    for i, r in enumerate(recs):
        t = norm_title(r.get("title"))
        if len(t) < 15:
            continue
        for j in by_title.get(t, []):
            yi, yj = r.get("year"), recs[j].get("year")
            if not yi or not yj or abs(int(yi) - int(yj)) <= 1:
                d1, d2 = r.get("doi"), recs[j].get("doi")
                if d1 and d2 and d1 != d2:      # same title, different DOIs: e.g. preprint vs. version; log but keep both
                    pairs.append({"kept": recs[j]["record_id"], "duplicate": r["record_id"], "method": "title-same-doi-differs(NOT merged)", "score": 1.0})
                    continue
                union(j, i, "title+year", 1.0)
        by_title.setdefault(t, []).append(i)
    # near-duplicate titles within blocks sharing the first 25 normalised characters
    blocks = {}
    for i, r in enumerate(recs):
        t = norm_title(r.get("title"))
        if len(t) >= 25:
            blocks.setdefault(t[:25], []).append(i)
    for idx in blocks.values():
        for x in range(len(idx)):
            for y in range(x + 1, len(idx)):
                i, j = idx[x], idx[y]
                if find(i) == find(j):
                    continue
                s = difflib.SequenceMatcher(None, norm_title(recs[i]["title"]), norm_title(recs[j]["title"])).ratio()
                yi, yj = recs[i].get("year"), recs[j].get("year")
                if s >= a.fuzzy and (not yi or not yj or abs(int(yi) - int(yj)) <= 1):
                    d1, d2 = recs[i].get("doi"), recs[j].get("doi")
                    if d1 and d2 and d1 != d2:
                        continue
                    union(i, j, "fuzzy-title", round(s, 3))
    groups = {}
    for i in range(len(recs)):
        groups.setdefault(find(i), []).append(i)
    kept = []
    for root, members in groups.items():
        r = dict(recs[root])
        r["merged_ids"] = "; ".join(recs[m]["record_id"] for m in members)
        r["sources"] = "; ".join(sorted({recs[m]["source_db"] for m in members}))
        kept.append(r)
    against = 0
    if a.against:
        prev = read_csv(a.against)
        pd = {norm_doi(p.get("doi")) for p in prev if p.get("doi")}
        pt = {norm_title(p.get("title")) for p in prev}
        rest = []
        for r in kept:
            if (r.get("doi") and r["doi"] in pd) or norm_title(r.get("title")) in pt:
                pairs.append({"kept": "(previously screened)", "duplicate": r["record_id"], "method": "against:" + os.path.basename(a.against), "score": 1.0})
                against += 1
            else:
                rest.append(r)
        kept = rest
    write_csv(os.path.join(a.run, "02_records_deduplicated.csv"), kept, FIELDS + ["merged_ids", "sources"])
    write_csv(os.path.join(a.run, "02_duplicate_pairs.csv"), pairs, ["kept", "duplicate", "method", "score"])
    merged = sum(1 for p in pairs if not p["method"].startswith(("against", "title-same")))
    log(a.run, "dedup", records_in=len(recs), duplicates_removed=merged, removed_as_previously_screened=against,
        records_out=len(kept), fuzzy_threshold=a.fuzzy,
        by_method={m: sum(1 for p in pairs if p["method"] == m) for m in sorted({p["method"] for p in pairs})})

def cmd_filter(a):
    cfg = json.load(open(a.config, encoding="utf-8"))
    recs = read_csv(os.path.join(a.run, "02_records_deduplicated.csv"))
    keep, excl = [], []
    for r in recs:
        reason = None
        for rule in cfg["rules"]:
            val = r.get(rule["field"], "") or ""
            if rule["kind"] == "year_range":
                if val and not (rule["min"] <= int(val) <= rule["max"]): reason = rule
                elif not val and rule.get("missing") == "exclude": reason = rule
            elif rule["kind"] == "exclude_regex":
                if val and re.search(rule["pattern"], val, re.I): reason = rule
            elif rule["kind"] == "require_regex":
                if val and not re.search(rule["pattern"], val, re.I): reason = rule
                elif not val and rule.get("missing") == "exclude": reason = rule
            if reason:
                excl.append({"record_id": r["record_id"], "rule_id": rule["id"], "field": rule["field"], "value": val[:120], "title": r.get("title", "")})
                break
        if not reason:
            keep.append(r)
    write_csv(os.path.join(a.run, "03_records_eligible_for_screening.csv"), keep, FIELDS + ["merged_ids", "sources"])
    write_csv(os.path.join(a.run, "03_excluded_by_rule.csv"), excl, ["record_id", "rule_id", "field", "value", "title"])
    counts = {}
    for e in excl:
        counts[e["rule_id"]] = counts.get(e["rule_id"], 0) + 1
    log(a.run, "filter", config=os.path.basename(a.config), records_in=len(recs), excluded_by_automation=len(excl),
        by_rule=counts, records_out=len(keep))

def cmd_recall(a):
    fname = a.stage or "03_records_eligible_for_screening.csv"
    recs = read_csv(os.path.join(a.run, fname))
    dois = {r["doi"]: r for r in recs if r.get("doi")}
    titles = {norm_title(r.get("title")): r for r in recs}
    gold = [g for g in read_csv(a.gold) if g.get("in_recall_denominator", "Y").upper() != "N"]
    rows, found = [], 0
    for g in gold:
        d, t = norm_doi(g.get("doi")), norm_title(g.get("title"))
        hit, how = None, ""
        if d and d in dois: hit, how = dois[d], "doi"
        elif t in titles: hit, how = titles[t], "title"
        else:
            best = max(((difflib.SequenceMatcher(None, t, k).ratio(), k) for k in titles if k[:10] == t[:10]), default=(0, None))
            if best[0] >= 0.93: hit, how = titles[best[1]], f"fuzzy-title({best[0]:.2f})"
        found += bool(hit)
        rows.append({"gold_id": g.get("gold_id"), "title": g.get("title"), "found": "Y" if hit else "N", "match": how,
                     "record_id": hit["record_id"] if hit else ""})
    write_csv(os.path.join(a.run, "04_recall_report.csv"), rows, ["gold_id", "title", "found", "match", "record_id"])
    rec = round(found / len(gold), 3) if gold else None
    log(a.run, "recall", stage=fname, gold_total=len(gold), gold_found=found, recall=rec,
        missed=[r["gold_id"] for r in rows if r["found"] == "N"])

# ------------------------------------------------------------------ OpenAlex
OA = "https://api.openalex.org"

def oa_get(path, **params):
    if os.environ.get("OPENALEX_MAILTO"):
        params["mailto"] = os.environ["OPENALEX_MAILTO"]
    url = f"{OA}{path}?{urllib.parse.urlencode(params)}"
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=30) as resp:
                return json.load(resp)
        except Exception as e:  # rate limit / transient errors
            if attempt == 4:
                raise RuntimeError(f"OpenAlex request failed: {url}: {e}")
            time.sleep(2 ** attempt)

def oa_abstract(inv):
    if not inv:
        return ""
    pos = sorted((p, w) for w, ps in inv.items() for p in ps)
    return " ".join(w for _, w in pos)

def oa_record(w, tag):
    loc = (w.get("primary_location") or {}).get("source") or {}
    return {"record_id": f"OPENALEX:{w['id'].rsplit('/', 1)[-1]}", "source_db": "OpenAlex", "source_file": tag,
            "an": w["id"].rsplit("/", 1)[-1], "title": w.get("display_name") or "",
            "abstract": oa_abstract(w.get("abstract_inverted_index")),
            "authors": "; ".join(x["author"]["display_name"] for x in w.get("authorships", []) if x.get("author")),
            "year": str(w.get("publication_year") or ""), "venue": loc.get("display_name", ""),
            "doc_type": w.get("type", ""), "language": w.get("language") or "", "doi": norm_doi(w.get("doi")),
            "url": w.get("id"), "keywords": "; ".join(k.get("display_name", "") for k in w.get("keywords", []) or []),
            "peer_reviewed": "", "retracted": str(w.get("is_retracted", ""))}

SEL = "id,doi,display_name,publication_year,type,language,primary_location,authorships,abstract_inverted_index,keywords,is_retracted,referenced_works"

def cmd_snowball(a):
    seeds = [norm_doi(s.get("doi") or s.get("doi_or_url")) for s in read_csv(a.seeds)]
    seeds = [s for s in seeds if s]
    out, per_seed, ids_back = {}, {}, set()
    for d in seeds:
        try:
            w = oa_get(f"/works/doi:{d}", select="id,referenced_works")
        except RuntimeError as e:
            per_seed[d] = f"not found: {e}"; continue
        wid = w["id"].rsplit("/", 1)[-1]
        nb = nf = 0
        if a.direction in ("backward", "both"):
            refs = [r.rsplit("/", 1)[-1] for r in w.get("referenced_works", [])]
            ids_back.update(refs); nb = len(refs)
        if a.direction in ("forward", "both"):
            cursor = "*"
            while cursor:
                page = oa_get("/works", filter=f"cites:{wid}", select=SEL, **{"per-page": 200, "cursor": cursor})
                for x in page["results"]:
                    out[x["id"]] = oa_record(x, f"forward:{d}")
                nf += len(page["results"])
                cursor = page["meta"].get("next_cursor")
        per_seed[d] = {"backward_refs": nb, "forward_citations": nf}
    ids_back = sorted(ids_back)
    for i in range(0, len(ids_back), 50):
        page = oa_get("/works", filter="openalex_id:" + "|".join(ids_back[i:i + 50]), select=SEL, **{"per-page": 50})
        for x in page["results"]:
            out.setdefault(x["id"], oa_record(x, "backward"))
    path = os.path.join(a.run, f"snowball_{a.direction}.csv")
    write_csv(path, list(out.values()), FIELDS)
    log(a.run, "snowball", direction=a.direction, seeds=len(seeds), per_seed=per_seed, records_out=len(out), output=os.path.basename(path),
        next_step="ingest this file into a new run (or --append), then dedup --against the screened set")

def cmd_openalex_search(a):
    params = {"search": a.query, "select": SEL, "per-page": 200, "cursor": "*"}
    if a.filter:
        params["filter"] = a.filter
    out = []
    while params["cursor"] and len(out) < a.max:
        page = oa_get("/works", **params)
        out += [oa_record(x, "openalex-search") for x in page["results"]]
        params["cursor"] = page["meta"].get("next_cursor")
    path = os.path.join(a.run, "openalex_search.csv")
    write_csv(path, out[:a.max], FIELDS)
    log(a.run, "openalex-search", query=a.query, filter=a.filter, records_out=min(len(out), a.max), output=os.path.basename(path))

# ------------------------------------------------------------- export, PRISMA
def cmd_export(a):
    recs = read_csv(os.path.join(a.run, "03_records_eligible_for_screening.csv"))
    cols = ["record_id", "title", "abstract", "authors", "year", "venue", "doc_type", "doi", "url", "sources", "merged_ids"]
    write_csv(os.path.join(a.run, "05_screening.csv"), recs, cols)
    with open(os.path.join(a.run, "05_screening.ris"), "w", encoding="utf-8") as f:
        for r in recs:
            f.write("TY  - JOUR\n")
            f.write(f"ID  - {r['record_id']}\nTI  - {r.get('title','')}\n")
            for au in [x.strip() for x in re.split(r";", r.get("authors", "")) if x.strip()]:
                f.write(f"AU  - {au}\n")
            for tag, k in (("PY", "year"), ("JO", "venue"), ("DO", "doi"), ("UR", "url"), ("AB", "abstract")):
                if r.get(k):
                    f.write(f"{tag}  - {r[k]}\n")
            f.write("ER  - \n\n")
    log(a.run, "export", records_out=len(recs), files=["05_screening.csv", "05_screening.ris"])

def cmd_prisma(a):
    entries = [json.loads(l) for l in open(os.path.join(a.run, "run_log.jsonl"), encoding="utf-8")]
    last = {}
    ingested = []
    for e in entries:
        last[e["command"]] = e
        if e["command"] == "ingest":
            ingested.append(e)
    print("Identification")
    for e in ingested:
        print(f"  {e['db']}: {e['records_in']} records {e['files']}")
    if "dedup" in last:
        d = last["dedup"]
        print(f"Duplicates removed: {d['duplicates_removed']}  (previously screened: {d['removed_as_previously_screened']})  by method {d['by_method']}")
    if "filter" in last:
        f = last["filter"]
        print(f"Marked ineligible by automation tools: {f['excluded_by_automation']}  {f['by_rule']}")
        print(f"Records to screen: {f['records_out']}")
    if "recall" in last:
        r = last["recall"]
        print(f"Gold-set recall: {r['gold_found']}/{r['gold_total']} = {r['recall']}  missed {r['missed']}")

# --------------------------------------------------------------- coding form
DIMS = [("D2", "Governance structure"), ("D3", "Policy definition and enforcement"),
        ("D4", "Shared responsibility and accountability"), ("D5", "Risk posture and security monitoring"),
        ("D6", "Identity and federation")]
ASPECTS = {"D2": "D2-roles, D2-oversight, D2-risk-strategy, D2-provider-mgmt, D2-other",
           "D3": "D3-sync, D3-translate, D3-enforce, D3-other",
           "D4": "D4-allocate, D4-reconcile, D4-keys, D4-other",
           "D5": "D5-assess, D5-monitor, D5-normalise, D5-other",
           "D6": "D6-trust, D6-lifecycle, D6-token, D6-mapping, D6-other"}

def cmd_coding_form(a):
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
    srcs = read_csv(a.included)
    wb = Workbook()
    ins = wb.active; ins.title = "Instructions"
    for line in [f"Coder: {a.coder}", "Codebook: v2/protocol/codebook_v2.md (frozen version only).",
                 "Code blind: do not consult other coders' forms or v1 ratings.",
                 "One row per source x dimension. G and M are independent (codebook section 4).",
                 "G1/M1 require the term search (section 6): fill term_search_terms and term_search_hits.",
                 "G2/G3/M2/M3 require >=1 quote (<=50 words) with PDF page and section.",
                 "rule_applied: cite the decision rule(s) used, e.g. R-M2a.",
                 "status: 'final' or 'unresolved' (unresolved = needs adjudication)."]:
        ins.append([line])
    ins.column_dimensions["A"].width = 110
    s = wb.create_sheet("Sources")
    s.append(["study_id", "label", "S_scope", "T_type", "N_normativity", "E_evidence_basis", "notes"])
    for r in srcs:
        s.append([r.get("study_id"), r.get("label") or r.get("title"), None, None, None, None, None])
    lists = {"S": ["S0", "S1", "S2", "S3"], "T": ["normative standard", "normative framework", "normative guidance", "empirical",
             "design/artefact", "review/SLR", "survey", "reference model"],
             "N": ["binding", "voluntary framework", "advisory guidance", "n/a (academic)"], "E": ["E1", "E2", "E3", "E4", "n/a"]}
    for col, key in zip("CDEF", "STNE"):
        dv = DataValidation(type="list", formula1='"' + ",".join(lists[key]) + '"', allow_blank=True)
        s.add_data_validation(dv); dv.add(f"{col}2:{col}{len(srcs) + 1}")
    c = wb.create_sheet("Cells")
    hdr = ["cell_id", "study_id", "label", "dimension", "dimension_name", "G", "M", "aspects", "allowed_aspects", "dual",
           "quote", "pdf_page", "section", "term_search_terms", "term_search_hits", "rule_applied", "rationale", "status", "coder"]
    c.append(hdr)
    for r in srcs:
        for d, name in DIMS:
            c.append([f"{r.get('study_id')}-{d}", r.get("study_id"), r.get("label") or r.get("title"), d, name,
                      None, None, None, ASPECTS[d], "N", None, None, None, None, None, None, None, None, a.coder])
    n = c.max_row
    for col, opts in (("F", "G1,G2,G3"), ("G", "M1,M2,M3"), ("J", "Y,N"), ("R", "final,unresolved")):
        dv = DataValidation(type="list", formula1=f'"{opts}"', allow_blank=True)
        c.add_data_validation(dv); dv.add(f"{col}2:{col}{n}")
    widths = {"A": 14, "B": 9, "C": 28, "D": 6, "E": 24, "F": 5, "G": 5, "H": 22, "I": 30, "J": 5, "K": 60, "L": 8,
              "M": 18, "N": 24, "O": 8, "P": 12, "Q": 40, "R": 10, "S": 8}
    for ws in (s, c):
        for cell in ws[1]:
            cell.font = Font(bold=True); cell.fill = PatternFill("solid", fgColor="DDDDDD")
        ws.freeze_panes = "A2"
    for k, v in widths.items():
        c.column_dimensions[k].width = v
    for row in c.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(a.out)
    print(f"wrote {a.out}: {len(srcs)} sources x {len(DIMS)} dimensions = {len(srcs) * len(DIMS)} cells")

# --------------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("ingest", help="normalise exports (CSV/RIS/BibTeX) into 01_records_ingested.csv")
    s.add_argument("--run", required=True); s.add_argument("--db", required=True, help="label, e.g. EBSCO, OpenAlex-snowball")
    s.add_argument("--append", action="store_true", help="append to an existing ingest in this run")
    s.add_argument("files", nargs="+"); s.set_defaults(f=cmd_ingest)
    s = sub.add_parser("dedup", help="DOI, exact-title and fuzzy-title deduplication; logs every pair")
    s.add_argument("--run", required=True); s.add_argument("--fuzzy", type=float, default=0.95)
    s.add_argument("--against", help="schema CSV of already screened records (e.g. previous 05_screening.csv)")
    s.set_defaults(f=cmd_dedup)
    s = sub.add_parser("filter", help="rule-based exclusion from a JSON config; logs every exclusion")
    s.add_argument("--run", required=True); s.add_argument("--config", required=True); s.set_defaults(f=cmd_filter)
    s = sub.add_parser("recall", help="gold-set recall of the current stage")
    s.add_argument("--run", required=True); s.add_argument("--gold", required=True)
    s.add_argument("--stage", help="file in run dir (default: 03_records_eligible_for_screening.csv)"); s.set_defaults(f=cmd_recall)
    s = sub.add_parser("snowball", help="OpenAlex backward/forward citations of seed DOIs")
    s.add_argument("--run", required=True); s.add_argument("--seeds", required=True, help="CSV with a doi column")
    s.add_argument("--direction", choices=["backward", "forward", "both"], default="both"); s.set_defaults(f=cmd_snowball)
    s = sub.add_parser("openalex-search", help="OpenAlex search for the recall cross-check")
    s.add_argument("--run", required=True); s.add_argument("--query", required=True)
    s.add_argument("--filter", default="from_publication_date:2020-01-01"); s.add_argument("--max", type=int, default=5000)
    s.set_defaults(f=cmd_openalex_search)
    s = sub.add_parser("export", help="screening CSV (ASReview/Rayyan) and RIS")
    s.add_argument("--run", required=True); s.set_defaults(f=cmd_export)
    s = sub.add_parser("prisma", help="print PRISMA counts from the run log")
    s.add_argument("--run", required=True); s.set_defaults(f=cmd_prisma)
    s = sub.add_parser("coding-form", help="blank v2 coding form (xlsx) for one coder; needs openpyxl")
    s.add_argument("--included", required=True, help="CSV with study_id and label/title")
    s.add_argument("--coder", required=True); s.add_argument("--out", required=True); s.set_defaults(f=cmd_coding_form)
    a = p.parse_args()
    a.f(a)

if __name__ == "__main__":
    main()
