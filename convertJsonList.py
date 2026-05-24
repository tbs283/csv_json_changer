import csv
import json
from pathlib import Path

INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")

# =========================
# 不正文字列置換テーブル
# =========================
REPLACE_TABLE = {
    "ground grab": "hands on the ground",
}


# =========================
# 文字列置換
# =========================
def normalize_text(text):

    if not isinstance(text, str):
        return text

    for before, after in REPLACE_TABLE.items():
        text = text.replace(before, after)

    return text


# =========================
# 再帰置換
# dict/list/str 全対応
# =========================
def normalize_data(value):

    if isinstance(value, dict):
        return {
            k: normalize_data(v)
            for k, v in value.items()
        }

    if isinstance(value, list):
        return [
            normalize_data(v)
            for v in value
        ]

    if isinstance(value, str):
        return normalize_text(value)

    return value


def convert_row(row):

    data = {
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
            "girlTop": "",
            "girlBottom": "",
            "girlUnder": "",
            "girlAction": row["girlAction_c"],
            "clothesStatus": row["clothesStatus"],
        },
        "上下フラグ": row.get("上下フラグ", "3"),
        "キャラヘッダフラグ": row.get("キャラヘッダフラグ", "1"),
        "縦横比": row.get("縦横比", "1"),
        "clothesFlg": row.get("clothesFlg", "1"),
        "seed_id": row.get("seed_id")
    }

    # 🔥 全体正規化
    return normalize_data(data)


def open_csv_auto(path):

    encodings = [
        "utf-8-sig",
        "cp932",
        "utf-8"
    ]

    for enc in encodings:
        try:

            f = open(path, encoding=enc)

            f.read()
            f.seek(0)

            print(f"📖 {path.name}: {enc}")

            return f

        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "unknown",
        b"",
        0,
        1,
        f"文字コード判定失敗: {path}"
    )


def main():

    if not INPUT_DIR.exists():
        print("❌ inputフォルダがない")
        return

    OUTPUT_DIR.mkdir(exist_ok=True)

    subdirs = sorted([
        d for d in INPUT_DIR.iterdir()
        if d.is_dir()
    ])

    if not subdirs:
        print("❌ input内にサブフォルダがありません")
        return

    for subdir in subdirs:

        csv_files = sorted(subdir.glob("*.csv"))

        if not csv_files:
            print(f"⚠️ {subdir.name} にCSVがありません")
            continue

        folder_data = {}
        folder_item_count = 0

        for csv_file in csv_files:

            key = csv_file.stem
            results = []

            with open_csv_auto(csv_file) as f:

                reader = csv.DictReader(f)

                for row in reader:
                    results.append(
                        convert_row(row)
                    )

            folder_data[key] = results
            folder_item_count += len(results)

            print(
                f"✅ {subdir.name}/{csv_file.name} "
                f"({len(results)}件)"
            )

        output_path = OUTPUT_DIR / f"{subdir.name}.json"

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                folder_data,
                f,
                ensure_ascii=False,
                indent=2
            )

        print(
            f"📁 {subdir.name}.json 出力 "
            f"({len(folder_data)}ファイル, "
            f"{folder_item_count}件)"
        )

    print("\n🎉 全変換完了")


if __name__ == "__main__":
    main()