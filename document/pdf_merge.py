"""
--sort name: Merge files by file name in ascending order (A → Z).
--sort name_desc: Merge files by file name in descending order (Z → A).
--sort natural: Merge files using human-friendly numeric sorting (1, 2, 10 instead of 1, 10, 2).
--sort mtime: Merge files from the oldest modified file to the newest.
--sort mtime_desc: Merge files from the newest modified file to the oldest.
"""

import argparse
import glob
import os
import re
from pypdf import PdfMerger

USAGE_TEXT = """
Usage examples:

  python3 merge.py --merge file1.pdf,file2.pdf,file3.pdf
  python3 merge.py --merge *
  python3 merge.py --merge * --sort natural
  python3 merge.py --merge * --sort mtime_desc -o output.pdf
"""

def natural_key(text):
    return [int(t) if t.isdigit() else t.lower()
            for t in re.split(r'(\d+)', text)]


def sort_files(files, sort_mode):
    if sort_mode == "name":
        return sorted(files)
    elif sort_mode == "name_desc":
        return sorted(files, reverse=True)
    elif sort_mode == "natural":
        return sorted(files, key=natural_key)
    elif sort_mode == "mtime":
        return sorted(files, key=lambda f: os.path.getmtime(f))
    elif sort_mode == "mtime_desc":
        return sorted(files, key=lambda f: os.path.getmtime(f), reverse=True)
    else:
        return files


def parse_files(merge_arg, sort_mode):
    if merge_arg.strip() == "*":
        files = glob.glob("*.pdf")
        print(f"Found {len(files)} PDF files")
    else:
        files = [f.strip() for f in merge_arg.split(",")]

    valid_files = []
    for f in files:
        if os.path.exists(f) and f.lower().endswith(".pdf"):
            valid_files.append(f)
        else:
            print(f"Skipped (not found or not a PDF): {f}")

    return sort_files(valid_files, sort_mode)


def merge_pdfs(files, output):
    if len(files) < 2:
        print("Error: At least 2 PDF files are required to merge")
        print(USAGE_TEXT)
        return

    merger = PdfMerger()

    for pdf in files:
        print(f"Adding: {pdf}")
        merger.append(pdf)

    merger.write(output)
    merger.close()

    print("\nMerge completed successfully")
    print(f"Output file: {output}")


def main():
    parser = argparse.ArgumentParser(
        description="Merge multiple PDF files into a single PDF"
    )

    parser.add_argument(
        "--merge",
        help="Comma-separated PDF files or * to merge all PDFs in the directory"
    )

    parser.add_argument(
        "--sort",
        choices=["name", "name_desc", "natural", "mtime", "mtime_desc"],
        default="name",
        help="Sorting mode (default: name)"
    )

    parser.add_argument(
        "-o", "--output",
        default="merged.pdf",
        help="Output PDF file name (default: merged.pdf)"
    )

    args = parser.parse_args()

    if not args.merge:
        print("Error: --merge argument is required")
        print(USAGE_TEXT)
        parser.print_help()
        return

    files = parse_files(args.merge, args.sort)
    merge_pdfs(files, args.output)


if __name__ == "__main__":
    main()
