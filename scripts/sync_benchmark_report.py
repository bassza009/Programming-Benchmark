#!/usr/bin/env python3
"""
sync_benchmark_report.py - Synchronize benchmark results, compile Programming_Benchmark_Report.docx,
and facilitate repository updates and Git push.
"""

import os
import re
import sys
import subprocess
import docx
from docx.shared import Cm, Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml import OxmlElement
from docx.oxml.ns import nsdecls, qn

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORT_MD = os.path.join(REPO_ROOT, "Programming_Benchmark_Report.md")
REPORT_DOCX = os.path.join(REPO_ROOT, "Programming_Benchmark_Report.docx")
SUMMARY_PY = os.path.join(REPO_ROOT, "pos_web_benchmark", "results", "generate_summary.py")
if not os.path.exists(SUMMARY_PY):
    SUMMARY_PY = os.path.join(REPO_ROOT, "main_web_benchmark", "results", "generate_summary.py")

def run_summary_generator():
    """Step 1: Execute generate_summary.py to aggregate raw results."""
    if os.path.exists(SUMMARY_PY):
        print("[1/4] Running generate_summary.py...")
        subprocess.run([sys.executable, SUMMARY_PY], cwd=os.path.dirname(SUMMARY_PY), check=True)
    else:
        print("[1/4] generate_summary.py not found, skipping.")

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

# ---------------------------------------------------------------------------
# Report layout follows the STOU academic report manual (สบฑ. 07/2550):
#   A4, margins top 1.5" / left 1.5" / right 1" / bottom 1" (chapter pages start 2" from top),
#   paragraph indent 8 characters, table caption above the table,
#   figure caption below the figure followed by "ที่มา:", page number top right.
# Markdown conventions used in Programming_Benchmark_Report.md:
#   "# บทที่ N" + "# ชื่อบท"   -> chapter title (new page, centered)
#   "# บรรณานุกรม" / "# ภาคผนวก ..." -> unnumbered chapter-level title
#   "## 1.1 ..." / "### 1.1.1 ..." -> headings
#   "ตารางที่ ..." line before a | table |, "ภาพที่ ..." and "ที่มา: ..." lines
#   "- item" bullets, "1) item" numbered items, **bold** inline
# ---------------------------------------------------------------------------
THAI_FONT = "TH Sarabun New"
BODY_PT = 16


def set_run_font(run, size=BODY_PT, bold=False):
    """Thai text uses the complex-script font slots (w:cs, w:szCs), so set them all."""
    run.font.name = THAI_FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(attr), THAI_FONT)
    for tag in ("w:szCs",):
        el = rpr.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            rpr.append(el)
        el.set(qn("w:val"), str(size * 2))
    if bold:
        b_cs = OxmlElement("w:bCs")
        rpr.append(b_cs)


def add_text(paragraph, text, size=BODY_PT, bold=False):
    """Add text with **bold** spans; strips `code` backticks."""
    text = text.replace("`", "")
    for i, part in enumerate(re.split(r"\*\*", text)):
        if part:
            set_run_font(paragraph.add_run(part), size, bold or i % 2 == 1)


def add_page_number(section):
    p = section.header.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run()
    for kind, text in (("begin", None), (None, "PAGE"), ("end", None)):
        if kind:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), kind)
        else:
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = text
        run._element.append(el)
    set_run_font(run)


def write_table(doc, rows):
    cols = max(len(r) for r in rows)
    tbl = doc.add_table(rows=len(rows), cols=cols)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(rows):
        for c_idx in range(cols):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = ""
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            add_text(p, row[c_idx] if c_idx < len(row) else "", size=14, bold=(r_idx == 0))
            if r_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_paragraph().paragraph_format.space_after = Pt(0)


def markdown_to_docx(md_path, docx_path):
    """Step 2: Convert Programming_Benchmark_Report.md into a Word Document (.docx)."""
    print(f"[2/4] Compiling {md_path} -> {docx_path}...")
    if not os.path.exists(md_path):
        print(f"Error: {md_path} does not exist.")
        return

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    doc = docx.Document()
    section = doc.sections[0]
    section.page_width, section.page_height = Cm(21.0), Cm(29.7)
    section.top_margin = Inches(1.5)
    section.left_margin = Inches(1.5)
    section.right_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.header_distance = Inches(0.75)
    add_page_number(section)

    normal = doc.styles["Normal"]
    normal.font.name = THAI_FONT
    normal.font.size = Pt(BODY_PT)
    normal.paragraph_format.space_after = Pt(0)
    normal.paragraph_format.line_spacing = 1.0

    indent = Inches(0.6)  # about 8 characters at 16 pt
    table_rows = []
    in_bibliography = False
    first_chapter = True

    for line in lines + ["\n"]:
        stripped = line.strip()

        # Tables: collect rows until the table ends
        if stripped.startswith("|") and stripped.endswith("|"):
            if not set(stripped.replace("|", "").replace("-", "").replace(":", "").strip()):
                continue  # |---|---| separator
            table_rows.append([c.strip() for c in stripped.split("|")[1:-1]])
            continue
        if table_rows:
            write_table(doc, table_rows)
            table_rows = []

        if not stripped:
            continue

        if stripped.startswith("# "):
            title = stripped[2:]
            starts_chapter = title.startswith("บทที่") or title in ("บรรณานุกรม",) or title.startswith("ภาคผนวก")
            p = doc.add_paragraph()
            if starts_chapter and not first_chapter:
                p.paragraph_format.page_break_before = True
            if starts_chapter:
                first_chapter = False
                p.paragraph_format.space_before = Pt(36)  # chapter pages start 2" from the top
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Pt(6 if title.startswith("บทที่") else 18)
            add_text(p, title, size=20, bold=True)
            in_bibliography = title == "บรรณานุกรม"
        elif stripped.startswith("## "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(12)
            add_text(p, stripped[3:], size=18, bold=True)
        elif stripped.startswith("### "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            p.paragraph_format.left_indent = Inches(0.3)
            add_text(p, stripped[4:], bold=True)
        elif stripped.startswith("ตารางที่ "):
            p = doc.add_paragraph()
            p.paragraph_format.space_before = Pt(6)
            label, _, rest = stripped.partition(" ")
            num, _, caption = rest.partition(" ")
            add_text(p, f"{label} {num}", bold=True)
            add_text(p, f" {caption}")
        elif stripped.startswith("ภาพที่ "):
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            add_text(p, stripped, bold=True)
        elif stripped.startswith("ที่มา:"):
            p = doc.add_paragraph()
            p.paragraph_format.space_after = Pt(6)
            add_text(p, stripped, size=14)
        elif stripped.startswith(("- ", "* ")):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = indent + Inches(0.25)
            p.paragraph_format.first_line_indent = Inches(-0.25)
            add_text(p, "- " + stripped[2:])
        elif re.match(r"^\d+\) ", stripped):
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = indent + Inches(0.3)
            p.paragraph_format.first_line_indent = Inches(-0.3)
            add_text(p, stripped)
        elif in_bibliography:
            p = doc.add_paragraph()
            p.paragraph_format.left_indent = Inches(0.6)
            p.paragraph_format.first_line_indent = Inches(-0.6)
            p.paragraph_format.space_after = Pt(4)
            add_text(p, stripped)
        else:
            p = doc.add_paragraph()
            p.alignment = WD_ALIGN_PARAGRAPH.THAI_JUSTIFY
            p.paragraph_format.first_line_indent = indent
            add_text(p, stripped)

    try:
        doc.save(docx_path)
        print(f"Successfully saved Word Document: {docx_path}")
    except PermissionError:
        alt_path = docx_path.replace(".docx", "_updated.docx")
        print(f"Warning: '{docx_path}' is locked (likely open in Microsoft Word).")
        print(f"Saving to alternative path: '{alt_path}'...")
        doc.save(alt_path)
        print(f"Successfully saved to: {alt_path}")

def git_commit_and_push(commit_msg="benchmarks: update data, sync report docx, and mirror README"):
    """Step 4: Stage, commit, and push changes to GitHub."""
    print("[3/4] Checking Git status...")
    status = subprocess.run(["git", "status", "-s"], capture_output=True, text=True, cwd=REPO_ROOT).stdout
    if not status.strip():
        print("No changes detected in working tree.")
        return

    print(f"[4/4] Committing and pushing to GitHub: '{commit_msg}'...")
    subprocess.run(["git", "add", "."], cwd=REPO_ROOT, check=True)
    res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_ROOT, capture_output=True, text=True)
    print(res.stdout.strip())
    
    push_res = subprocess.run(["git", "push", "origin", "main"], cwd=REPO_ROOT, capture_output=True, text=True)
    if push_res.returncode == 0:
        print("Successfully pushed to origin/main!")
    else:
        print(f"Push output: {push_res.stderr.strip()}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Synchronize benchmark data, update report .docx, and push to GitHub.")
    parser.add_argument("--summary-only", action="store_true", help="Only run generate_summary.py")
    parser.add_argument("--docx", action="store_true", help="Compile Programming_Benchmark_Report.docx")
    parser.add_argument("--push", action="store_true", help="Commit and push changes to GitHub")
    parser.add_argument("-m", "--message", default="benchmarks: update results, sync report docx, and mirror READMEs", help="Commit message")
    parser.add_argument("--all", action="store_true", default=True, help="Execute full sync pipeline")

    args = parser.parse_args()

    if args.summary_only:
        run_summary_generator()
    elif args.docx:
        markdown_to_docx(REPORT_MD, REPORT_DOCX)
    elif args.push:
        git_commit_and_push(args.message)
    else:
        run_summary_generator()
        markdown_to_docx(REPORT_MD, REPORT_DOCX)
        if args.push or "--push" in sys.argv:
            git_commit_and_push(args.message)

if __name__ == "__main__":
    main()
