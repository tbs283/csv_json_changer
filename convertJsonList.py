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
        "clothesFlg": row.get("clothesFlg", "1"),
        "seed": (
            [s.strip() for s in row["seed"].split(",")] 
            if row.get("seed") 
            else []
        )
    }


def main():

    if not INPUT_DIR.exists():
        print("❌ inputフォルダがない")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)

    subdirs = sorted([d for d in INPUT_DIR.iterdir() if d.is_dir()])
    if not subdirs:
        print("❌ input内にサブフォルダがありません")
        return

    for subdir in subdirs:
        csv_files = sorted(subdir.glob("*.csv"))
        if not csv_files:
            print(f"⚠️ {subdir.name} にCSVがありません。スキップします")
            continue

        folder_data = {}
        folder_item_count = 0

        for csv_file in csv_files:
            key = csv_file.stem
            results = []

            # UTF-8 → CP932に対応
            with open(csv_file, encoding="cp932") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    results.append(convert_row(row))

            folder_data[key] = results
            folder_item_count += len(results)
            print(f"✅ {subdir.name}/{csv_file.name} を処理完了 ({len(results)}件)")

        output_path = OUTPUT_DIR / f"{subdir.name}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(folder_data, f, ensure_ascii=False, indent=2)

        print(f"📁 {subdir.name}.json を出力 ({len(folder_data)}ファイル、{folder_item_count}件)")

    print("\n🎉 全変換完了")


if __name__ == "__main__":
    main()
