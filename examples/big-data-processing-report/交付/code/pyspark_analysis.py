from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def pandas_fallback(input_path: Path, output_dir: Path) -> None:
    df = pd.read_csv(input_path)
    category_df = (
        df.groupby("course_type", as_index=False)
        .agg(order_count=("user_id", "count"), avg_payment=("payment_amount", "mean"))
    )
    province_df = (
        df.groupby("province", as_index=False)
        .agg(total_payment=("payment_amount", "sum"))
        .sort_values("total_payment", ascending=False)
    )
    daily_df = (
        df.groupby("visit_date", as_index=False)
        .agg(order_count=("user_id", "count"))
        .sort_values("visit_date")
    )
    category_df.to_csv(output_dir / "category_stats.csv", index=False, encoding="utf-8-sig")
    province_df.to_csv(output_dir / "province_revenue.csv", index=False, encoding="utf-8-sig")
    daily_df.to_csv(output_dir / "daily_trend.csv", index=False, encoding="utf-8-sig")
    (output_dir / "analysis_runtime.json").write_text(
        json.dumps({"engine": "pandas_fallback", "rows": int(len(df))}, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    data_path = base_dir / "data" / "clean_learning_data.csv"
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)
    try:
        from pyspark.sql import SparkSession
        from pyspark.sql.functions import avg, col, count, sum

        spark = SparkSession.builder.appName("course-learning-analysis").getOrCreate()
        source = spark.read.option("header", True).option("inferSchema", True).csv(str(data_path))

        category_df = source.groupBy("course_type").agg(
            count("*").alias("order_count"),
            avg("payment_amount").alias("avg_payment")
        )
        province_df = source.groupBy("province").agg(
            sum("payment_amount").alias("total_payment")
        ).orderBy(col("total_payment").desc())
        daily_df = source.groupBy("visit_date").agg(
            count("*").alias("order_count")
        ).orderBy("visit_date")

        category_df.toPandas().to_csv(output_dir / "category_stats.csv", index=False, encoding="utf-8-sig")
        province_df.toPandas().to_csv(output_dir / "province_revenue.csv", index=False, encoding="utf-8-sig")
        daily_df.toPandas().to_csv(output_dir / "daily_trend.csv", index=False, encoding="utf-8-sig")
        (output_dir / "analysis_runtime.json").write_text(
            json.dumps({"engine": "pyspark", "rows": int(source.count())}, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        spark.stop()
    except Exception:
        pandas_fallback(data_path, output_dir)

    print(f"analysis outputs written to {output_dir}")


if __name__ == "__main__":
    main()
