#!/usr/bin/env python3
"""Deterministic term counts per PDF for absence ratings (codebook v2, section 6, rule R-ABS).

For every PDF and every dimension (D2-D6) plus the multi-cloud term list (MC, used for M1),
counts case-insensitive hits per term and records the PDF page numbers (1-based, as shown by a
PDF viewer). No judgement is made: coders still inspect the hits before rating G1/M1.
The same output is given to both coders, so it does not affect coder independence.

Usage:
  python v2/pipeline/term_counts.py --pdfs <folder> --out v2/coding/term_counts.csv \
      [--map study_map.csv]      # optional CSV with columns study_id,pdf (file name); default: file stem
Writes <out> (one row per study x list x term) and <out stem>_by_cell.csv (one row per study x
dimension, ready to copy into term_search_terms / term_search_hits of the coding form).
Requires pdftotext (poppler) or, as fallback, pypdf.
"""
import argparse, csv, hashlib, json, os, re, shutil, subprocess, sys

# Codebook v2 section 6. Change only together with a codebook version change.
TERMS = {
    "D2": ["governance", "oversight", "role*", "responsibilit*", "risk strategy"],
    "D3": ["policy", "polic*", "enforce*", "guardrail", "configuration", "baseline"],
    "D4": ["shared responsibility", "SSRM", "responsibility model", "accountab*", "key management"],
    "D5": ["monitor*", "posture", "CSPM", "risk assess*", "logging", "telemetry"],
    "D6": ["identity", "federat*", "IdP", "SAML", "OIDC", "OAuth", "provisioning", "token"],
    "MC": ["multi-cloud", "multicloud", "multiple cloud", "cross-cloud", "inter-cloud", "federat*",
           "heterogeneous provider*", "CSPs"],
}
CODEBOOK_VERSION = "v2.0-draft"   # update when the codebook is frozen

def pattern(term):
    parts = [re.escape(w).replace(r"\*", r"\w*") for w in term.split()]
    body = r"[\s\-]+".join(parts)
    body = body.replace(r"\-", r"[\s\-]?")      # multi-cloud ~ multi cloud ~ multicloud
    return re.compile(r"(?<!\w)" + body + (r"" if term.endswith("*") else r"(?!\w)"), re.I)

def pages_of(pdf):
    if shutil.which("pdftotext"):
        txt = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True, check=True).stdout
        pages = txt.split("\f")
        if pages and not pages[-1].strip():
            pages = pages[:-1]
    else:
        from pypdf import PdfReader
        pages = [p.extract_text() or "" for p in PdfReader(pdf).pages]
    return [re.sub(r"(\w)-\n\s*(\w)", r"\1\2", p) for p in pages]   # undo end-of-line hyphenation

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pdfs", required=True); ap.add_argument("--out", required=True); ap.add_argument("--map")
    a = ap.parse_args()
    files = sorted(f for f in os.listdir(a.pdfs) if f.lower().endswith(".pdf"))
    names = {f: os.path.splitext(f)[0] for f in files}
    if a.map:
        m = {r["pdf"]: r["study_id"] for r in csv.DictReader(open(a.map, encoding="utf-8-sig"))}
        names = {f: m[f] for f in files if f in m}
        missing = [f for f in files if f not in m]
        if missing: print("not in map, skipped:", missing, file=sys.stderr)
    rows, cells = [], []
    for f, sid in names.items():
        path = os.path.join(a.pdfs, f)
        pages = pages_of(path)
        empty = sum(1 for p in pages if len(p.strip()) < 50)
        if empty > len(pages) / 2:
            print(f"WARNING {f}: {empty}/{len(pages)} pages without text (scanned PDF?) - counts unreliable", file=sys.stderr)
        sha = hashlib.sha256(open(path, "rb").read()).hexdigest()[:16]
        for lst, terms in TERMS.items():
            for t in terms:
                rx = pattern(t)
                per = [(i + 1, len(rx.findall(p))) for i, p in enumerate(pages)]
                hits = [(pg, n) for pg, n in per if n]
                rows.append({"study_id": sid, "pdf": f, "pdf_sha256_16": sha, "list": lst, "term": t,
                             "hits": sum(n for _, n in hits), "pdf_pages": " ".join(str(pg) for pg, _ in hits)})
        for d in ["D2", "D3", "D4", "D5", "D6"]:
            own = [r for r in rows if r["study_id"] == sid and r["list"] == d]
            mc = [r for r in rows if r["study_id"] == sid and r["list"] == "MC"]
            cells.append({"cell_id": f"{sid}-{d}", "study_id": sid, "dimension": d,
                          "term_search_terms": "; ".join(r["term"] for r in own) + " | MC: " + "; ".join(r["term"] for r in mc),
                          "term_search_hits": "; ".join(f"{r['term']}={r['hits']}" for r in own) + " | MC: " +
                                              "; ".join(f"{r['term']}={r['hits']}" for r in mc)})
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    with open(a.out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
    by_cell = os.path.splitext(a.out)[0] + "_by_cell.csv"
    with open(by_cell, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cells[0])); w.writeheader(); w.writerows(cells)
    print(json.dumps({"codebook": CODEBOOK_VERSION, "pdfs": len(names), "rows": len(rows), "cells": len(cells),
                      "out": a.out, "by_cell": by_cell}))

if __name__ == "__main__":
    main()
