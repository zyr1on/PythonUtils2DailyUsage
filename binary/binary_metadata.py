# binary_metadata.py
import argparse
from detect import detect_binary
from common import common_metadata
from elf import analyze_elf
from pe import analyze_pe
from packer import detect_packer
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    ftype = detect_binary(args.file)
    if not ftype:
        print("Unsupported file type")
        return

    result = {}
    result["type"] = ftype
    result.update(common_metadata(args.file))

    if ftype == "ELF":
        result.update(analyze_elf(args.file))
    elif ftype == "PE":
        result.update(analyze_pe(args.file))

    result["packer"] = detect_packer(args.file)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for k, v in result.items():
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()
