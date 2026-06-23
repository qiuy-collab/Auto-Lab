from __future__ import annotations

import csv
import random
from datetime import date, timedelta
from pathlib import Path


PROVINCES = ["北京", "上海", "广东", "江苏", "浙江", "四川", "湖北", "山东", "河南", None]
COURSE_TYPES = ["Python开发", "大数据基础", "Spark分析", "数据库应用", "Linux运维"]
PAYMENT_STATUS = ["paid", "paid", "paid", "refund"]


def main() -> None:
    random.seed(20260618)
    base_dir = Path(__file__).resolve().parents[1]
    data_dir = base_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    output_path = data_dir / "raw_learning_data.csv"
    start_day = date(2026, 1, 1)

    rows = []
    for index in range(6500):
        watch_seconds = random.randint(120, 18000)
        if index % 137 == 0:
            watch_seconds = 30000
        rating = random.choice([3.5, 4.0, 4.5, 5.0, None])
        row = {
            "user_id": f"U{100000 + index}",
            "province": random.choice(PROVINCES),
            "course_type": random.choice(COURSE_TYPES),
            "watch_seconds": watch_seconds,
            "payment_amount": round(random.uniform(29, 499), 2),
            "completion_rate": round(random.uniform(0.15, 1.0), 2),
            "rating": rating,
            "payment_status": random.choice(PAYMENT_STATUS),
            "visit_date": (start_day + timedelta(days=random.randint(0, 140))).isoformat()
        }
        rows.append(row)

    rows.extend(rows[:25])
    with output_path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"raw rows written: {len(rows)}")
    print(output_path)


if __name__ == "__main__":
    main()
