from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    raw_path = data_dir / "raw_learning_data.csv"
    clean_path = data_dir / "clean_learning_data.csv"
    summary_path = output_dir / "cleaning_summary.json"

    df = pd.read_csv(raw_path)
    before_rows = len(df)
    duplicate_count = int(df.duplicated().sum())
    df = df.drop_duplicates()
    df["province"] = df["province"].fillna("未知地区")
    df["rating"] = df["rating"].fillna(df["rating"].median())
    df["watch_seconds"] = df["watch_seconds"].clip(lower=60, upper=14400)
    df["visit_date"] = pd.to_datetime(df["visit_date"]).dt.strftime("%Y-%m-%d")
    df["payment_amount"] = df["payment_amount"].round(2)
    df.to_csv(clean_path, index=False, encoding="utf-8-sig")

    summary = {
        "before_rows": before_rows,
        "after_rows": int(len(df)),
        "removed_duplicates": duplicate_count,
        "missing_province_filled": True,
        "missing_rating_filled_with_median": True
    }
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
