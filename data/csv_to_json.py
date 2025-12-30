import csv
import json
import sys
import os

def csv_to_json(csv_file, json_file=None):
    if not os.path.exists(csv_file):
        print("Error: CSV file not found")
        return

    if json_file is None:
        base = os.path.splitext(csv_file)[0]
        json_file = base + ".json"

    with open(csv_file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Converted: {csv_file} → {json_file}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 csv_to_json.py input.csv [output.json]")
        sys.exit(1)

    csv_file = sys.argv[1]
    json_file = sys.argv[2] if len(sys.argv) > 2 else None

    csv_to_json(csv_file, json_file)
