import csv
import json
from pathlib import Path

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")


def convert_row(row):
    return {
        "base": {
            "quality": row["quality"],
            "style": row["style"],
            "r18": row["r18"],
            "composition": row["composition"],
            "play": row["play"],
            "girl": row["girl"],
            "girlTop": row["girlTop"],
            "girlBottom": row["girlBottom"],
            "girlUnder": row["girlUnder"],
            "girlAction": row["girlAction"],
            "male": row["male"],
            "bgBase": row["bgBase"],
            "bgTop": row["bgTop"],
            "bgBottom": row["bgBottom"],
        },
        "charaVariable": {
            "girlTop": row["girlTop_c"],
            "girlBottom": row["girlBottom_c"],
            "girlUnder": row["girlUnder_c"],
            "girlAction": row["girlAction_c"],
            "clothesStatus": row["clothesStatus"],
        },
        "上下フラグ": row.get("上下フラグ", "3"),
        "キャラヘッダフラグ": row.get("キャラヘッダフラグ", "1"),
        "縦横比": row.get("縦横比", "1"),
        "seed": row.get("seed", "")
    }


def main():

    if not INPUT_DIR.exists():
        print("❌ inputフォルダがない")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)

    csv_files = list(INPUT_DIR.glob("*.csv"))

    if not csv_files:
        print("❌ CSVがない")
        return

    for csv_file in csv_files:

        key = csv_file.stem
        results = []

        # 👇ここ修正（UTF-8 → CP932）
        with open(csv_file, encoding="cp932") as f:
            reader = csv.DictReader(f)

            for row in reader:
                results.append(convert_row(row))

        output_data = {
            key: results
        }

        output_path = OUTPUT_DIR / f"{key}.json"

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)

        print(f"✅ {csv_file.name} → {output_path}")

    print("🎉 全変換完了")


if __name__ == "__main__":
    main()