#!/usr/bin/env python3
"""
PDF Chapter Extractor → Markdown
Extracts chapters from a PDF using its bookmark outline (TOC).
Falls back to heuristic heading detection if no TOC is present.

Usage:
    python pdf_to_markdown.py book.pdf
    python pdf_to_markdown.py book.pdf --out ./chapters
    python pdf_to_markdown.py book.pdf --toc          # just print TOC/outline
"""

import sys
import re
import argparse
from pathlib import Path

try:
    import fitz  # pymupdf
except ImportError:
    sys.exit("Missing dependency. Run: pip install pymupdf")


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:60]


def extract_page_text(page) -> str:
    """Extract text from a page, preserving basic structure."""
    blocks = page.get_text("dict")["blocks"]
    lines = []
    prev_y = None

    for block in blocks:
        if block["type"] != 0:  # skip image blocks
            continue
        for line in block["lines"]:
            y = line["bbox"][1]
            # Insert blank line on large vertical gaps (paragraph breaks)
            if prev_y is not None and (y - prev_y) > 20:
                lines.append("")
            text = " ".join(span["text"] for span in line["spans"]).strip()
            if text:
                lines.append(text)
            prev_y = y

    return "\n".join(lines)


def toc_to_chapters(doc) -> list[dict]:
    """
    Use PDF bookmark outline to define chapters.
    Returns list of {title, start_page, end_page}.
    Only uses top-level entries (level == 1).
    """
    toc = doc.get_toc()  # [[level, title, page], ...]
    if not toc:
        return []

    # Filter to top-level entries only
    top = [(title, page - 1) for level, title, page in toc if level == 1]

    chapters = []
    for i, (title, start) in enumerate(top):
        end = top[i + 1][1] - 1 if i + 1 < len(top) else doc.page_count - 1
        chapters.append({"title": title, "start": start, "end": end})

    return chapters


def heuristic_chapters(doc) -> list[dict]:
    """
    Fallback: detect chapter headings by looking for large/bold text
    near the top of a page that looks like a chapter title.
    """
    chapters = []
    chapter_re = re.compile(
        r"^(chapter\s+\d+|section\s+\d+|\d+\.\s+\w)", re.IGNORECASE
    )

    for page_num in range(doc.page_count):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] != 0:
                continue
            for line in block["lines"]:
                text = " ".join(s["text"] for s in line["spans"]).strip()
                size = max((s["size"] for s in line["spans"]), default=0)
                flags = max((s["flags"] for s in line["spans"]), default=0)
                is_bold = bool(flags & 2**4)
                is_large = size >= 14
                y_pos = line["bbox"][1]
                near_top = y_pos < page.rect.height * 0.35

                if (is_large or is_bold) and near_top and chapter_re.match(text):
                    chapters.append({"title": text, "start": page_num})
                    break

    # Fill in end pages
    result = []
    for i, ch in enumerate(chapters):
        end = chapters[i + 1]["start"] - 1 if i + 1 < len(chapters) else doc.page_count - 1
        result.append({**ch, "end": end})

    return result


def chapter_to_markdown(doc, chapter: dict) -> str:
    lines = [f"# {chapter['title']}\n"]

    for page_num in range(chapter["start"], chapter["end"] + 1):
        page = doc[page_num]
        text = extract_page_text(page)

        # Basic markdown cleanup
        text = re.sub(r" {3,}", "  ", text)          # collapse big spaces
        text = re.sub(r"\n{3,}", "\n\n", text)        # max double newlines
        text = text.strip()

        if text:
            lines.append(f"\n<!-- page {page_num + 1} -->\n")
            lines.append(text)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Extract PDF chapters to Markdown")
    parser.add_argument("pdf", help="Path to input PDF")
    parser.add_argument("--out", default="./chapters", help="Output directory (default: ./chapters)")
    parser.add_argument("--toc", action="store_true", help="Print TOC and exit")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.exists():
        sys.exit(f"File not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    print(f"Opened: {pdf_path.name} ({doc.page_count} pages)")

    # --- Detect chapters ---
    chapters = toc_to_chapters(doc)
    if chapters:
        print(f"Found {len(chapters)} top-level TOC entries")
    else:
        print("No PDF outline found — trying heuristic chapter detection...")
        chapters = heuristic_chapters(doc)
        if chapters:
            print(f"Heuristic found {len(chapters)} chapters")
        else:
            print("No chapters detected. Extracting as single document.")
            chapters = [{"title": pdf_path.stem, "start": 0, "end": doc.page_count - 1}]

    # --- Print TOC mode ---
    if args.toc:
        print("\nChapters found:")
        for i, ch in enumerate(chapters, 1):
            print(f"  {i:2}. [{ch['start']+1}–{ch['end']+1}] {ch['title']}")
        return

    # --- Extract to markdown ---
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    for i, chapter in enumerate(chapters, 1):
        fname = f"{i:02d}-{slugify(chapter['title'])}.md"
        out_path = out_dir / fname
        print(f"  Writing: {fname}  (pages {chapter['start']+1}–{chapter['end']+1})")
        md = chapter_to_markdown(doc, chapter)
        out_path.write_text(md, encoding="utf-8")

    print(f"\nDone. {len(chapters)} files written to: {out_dir.resolve()}")


if __name__ == "__main__":
    main()
