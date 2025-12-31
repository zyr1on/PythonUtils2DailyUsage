import argparse
import os

USAGE_TEXT = """
Usage examples:

  python3 remove_duplicate_lines.py input.txt
  python3 remove_duplicate_lines.py input.txt output.txt

  python3 remove_duplicate_lines.py input.txt --strip-whitespace
  python3 remove_duplicate_lines.py input.txt --in-place

  python3 remove_duplicate_lines.py input.txt --sort asc
  python3 remove_duplicate_lines.py input.txt --sort desc --in-place
"""

def remove_duplicates(
    input_file,
    output_file,
    strip_ws=False,
    inplace=False,
    sort_mode=None
):
    if not os.path.exists(input_file):
        print("Error: File not found")
        print(USAGE_TEXT)
        return

    # in-place ise geçici dosya kullan
    if inplace:
        output_file = input_file + ".tmp"
    elif not output_file:
        base, ext = os.path.splitext(input_file)
        output_file = base + "_nodup" + ext

    seen = set()
    lines_for_sort = [] if sort_mode else None

    with open(input_file, "r", encoding="utf-8") as fin, \
         open(output_file, "w", encoding="utf-8") as fout:

        for line in fin:
            key = line.strip() if strip_ws else line

            if key not in seen:
                seen.add(key)

                if sort_mode:
                    lines_for_sort.append(line)
                else:
                    fout.write(line)

    # sort istenmişse en sona yaz
    if sort_mode:
        if sort_mode == "asc":
            lines_for_sort.sort()
        elif sort_mode == "desc":
            lines_for_sort.sort(reverse=True)

        with open(output_file, "w", encoding="utf-8") as fout:
            for line in lines_for_sort:
                fout.write(line)

    # in-place ise eski dosyanın üstüne yaz
    if inplace:
        os.replace(output_file, input_file)
        print("Duplicates removed (in-place)")
        print(f"Updated file: {input_file}")
    else:
        print("Duplicates removed")
        print(f"Output file: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Remove duplicate lines from a text file (streaming)"
    )

    parser.add_argument("input", help="Input text file")
    parser.add_argument("output", nargs="?", help="Output file (optional)")

    parser.add_argument(
        "--strip-whitespace",
        action="store_true",
        help="Ignore leading/trailing whitespace when comparing lines"
    )

    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Modify the input file directly"
    )

    parser.add_argument(
        "--sort",
        choices=["asc", "desc"],
        help="Sort unique lines after removing duplicates"
    )

    args = parser.parse_args()

    if args.in_place and args.output:
        print("Error: --in-place cannot be used with output file")
        print(USAGE_TEXT)
        return

    remove_duplicates(
        input_file=args.input,
        output_file=args.output,
        strip_ws=args.strip_whitespace,
        inplace=args.in_place,
        sort_mode=args.sort
    )


if __name__ == "__main__":
    main()
