#!/usr/bin/env python3
import argparse
import pysubs2
import sys
import os

def main():
    parser = argparse.ArgumentParser(description="SRT/ASS subtitle time shift")
    parser.add_argument("--file", "-f", required=True, help="File to edit subtitle time")
    parser.add_argument("--time", "-t", type=float, required=True, help="Time Shift (seconds, + , - )")
    parser.add_argument("--output", "-o", help="Output name (optional)")
    
    args = parser.parse_args()
    
    try:
        subs = pysubs2.load(args.file,encoding="utf-8")
    except UnicodeDecodeError:
        subs = pysubs2.load(args.file,encoding="windows-1254")
    except Exception as e:
        print(f"file could not be read: {e}")
        sys.exit(1)

    subs.shift(s=args.time)
    
    if args.output:
        ext = os.path.splitext(args.file)[1]
        output_file = f"{args.output}{ext}"
    else:
        base, ext = os.path.splitext(args.file)
        output_file = f"{base}_rsynced{ext}"
    try:
        subs.save(output_file)
        print(f"Subtitle shifted {args.time} and saved as '{output_file}'")
    except Exception as e:
        print(f"file could not be saved: {e}")
        sys.exit(1)
if __name__ == "__main__":
    main()
