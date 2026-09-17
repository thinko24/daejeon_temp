# -*- coding: utf-8 -*-
"""
[1회 실행] 대전 관측 개시(1969년) 이후 오늘까지의 과거 데이터를 통째로 수집한다.
연도별로 나눠 받아 data/daejeon.csv 를 새로 만든다.
"""
import datetime as dt
import pandas as pd
from kma import fetch_range, COLS

START_YEAR = 1969          # 대전 관측 개시 연도 (그 이전은 데이터가 없어 자동으로 건너뜀)
OUT = "data/daejeon.csv"


def main():
    today = dt.date.today()
    frames = []

    for year in range(START_YEAR, today.year + 1):
        start = f"{year}0101"
        end = f"{year}1231" if year < today.year else today.strftime("%Y%m%d")
        print(f"수집 중... {year}")
        try:
            df = fetch_range(start, end)
        except Exception as e:
            print(f"  {year} 건너뜀: {e}")
            continue
        if not df.empty:
            frames.append(df)

    if not frames:
        print("수집된 데이터가 없습니다. 인증키를 확인하세요.")
        return

    all_df = pd.concat(frames, ignore_index=True)
    all_df = all_df.drop_duplicates(subset="날짜").sort_values("날짜")
    all_df.to_csv(OUT, index=False, encoding="utf-8")
    print(f"완료: {len(all_df)}행 저장 -> {OUT}")


if __name__ == "__main__":
    main()
