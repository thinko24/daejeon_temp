# -*- coding: utf-8 -*-
"""
[매일 실행] csv 의 마지막 날짜 다음날부터 '어제'까지를 받아 아래에 이어붙인다.
하루 빠지거나 며칠 밀려도 알아서 빈 날짜를 모두 채운다(자가 복구).
"""
import os
import datetime as dt
import pandas as pd
from kma import fetch_range, COLS

OUT = "data/daejeon.csv"
START_YEAR = 1969  # csv 가 아예 없을 때의 시작점


def main():
    if os.path.exists(OUT):
        old = pd.read_csv(OUT, dtype=str)
    else:
        old = pd.DataFrame(columns=COLS)

    yesterday = dt.date.today() - dt.timedelta(days=1)

    if not old.empty:
        last = dt.datetime.strptime(old["날짜"].max(), "%Y-%m-%d").date()
        start = last + dt.timedelta(days=1)
    else:
        start = dt.date(START_YEAR, 1, 1)

    if start > yesterday:
        print("이미 최신입니다.")
        return

    new = fetch_range(start.strftime("%Y%m%d"), yesterday.strftime("%Y%m%d"))
    if new.empty:
        print("새로 추가할 데이터가 없습니다.")
        return

    merged = pd.concat([old, new], ignore_index=True)
    merged = merged.drop_duplicates(subset="날짜").sort_values("날짜")
    merged.to_csv(OUT, index=False, encoding="utf-8")
    print(f"추가 완료: {len(new)}행 -> 총 {len(merged)}행")


if __name__ == "__main__":
    main()
