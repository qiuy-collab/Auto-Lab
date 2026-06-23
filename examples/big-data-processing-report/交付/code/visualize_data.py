from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    output_dir = base_dir / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    category_df = pd.read_csv(output_dir / "category_stats.csv")
    province_df = pd.read_csv(output_dir / "province_revenue.csv").head(10)
    daily_df = pd.read_csv(output_dir / "daily_trend.csv").head(30)

    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "Arial Unicode MS"]
    plt.rcParams["axes.unicode_minus"] = False

    plt.figure(figsize=(10, 6))
    plt.bar(category_df["course_type"], category_df["order_count"], color="#3a7afe")
    plt.title("课程类别订单量统计")
    plt.xlabel("课程类别")
    plt.ylabel("订单量")
    plt.tight_layout()
    plt.savefig(output_dir / "course_type_count.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.barh(province_df["province"], province_df["total_payment"], color="#33a06f")
    plt.title("地区收入Top10")
    plt.xlabel("总收入")
    plt.ylabel("地区")
    plt.tight_layout()
    plt.savefig(output_dir / "province_revenue_top10.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.plot(daily_df["visit_date"], daily_df["order_count"], color="#e67e22", marker="o", linewidth=1)
    plt.title("访问日趋势统计")
    plt.xlabel("日期")
    plt.ylabel("订单量")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(output_dir / "daily_trend.png", dpi=200)
    plt.close()

    print(f"charts written to {output_dir}")


if __name__ == "__main__":
    main()
