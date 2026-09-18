# -*- coding: utf-8 -*-
"""
기상청 ASOS 일자료 조회 공통 모듈.
대전(지점 133)의 날짜별 평균/최저/최고 기온을 받아온다.
"""
import os
import time
import requests
import pandas as pd

SERVICE_KEY = os.environ["DATA_GO_KR_KEY"]

STN_ID = "133"  # 대전 (서울은 108)
# https 로 접속(http/80 은 해외 서버에서 자주 타임아웃)
URL = "https://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"
COLS = ["날짜", "지점", "평균기온", "최저기온", "최고기온"]


def _get(params, retries=4):
    """접속이 끊기면 몇 초 쉬었다 다시 시도(최대 retries회)."""
    last_err = None
    for i in range(retries):
        try:
            return requests.get(URL, params=params, timeout=60)
        except requests.exceptions.RequestException as e:
            last_err = e
            wait = 5 * (i + 1)  # 5, 10, 15초... 점점 길게 대기
            print(f"  접속 실패({i + 1}/{retries}) - {wait}초 후 재시도")
            time.sleep(wait)
    raise last_err


def fetch_range(start_dt: str, end_dt: str) -> pd.DataFrame:
    rows = []
    page = 1
    while True:
        params = {
            "serviceKey": SERVICE_KEY,
            "pageNo": page,
            "numOfRows": 999,
            "dataType": "JSON",
            "dataCd": "ASOS",
            "dateCd": "DAY",
            "startDt": start_dt,
            "endDt": end_dt,
            "stnIds": STN_ID,
        }
        resp = _get(params)
        resp.raise_for_status()

        try:
            body = resp.json()["response"]["body"]
        except Exception:
            raise RuntimeError(f"API 응답 파싱 실패: {resp.text[:300]}")

        items = body.get("items", "")
        if not items or not items.get("item"):
            break

        for it in items["item"]:
            rows.append({
                "날짜": it.get("tm", ""),
                "지점": it.get("stnId", STN_ID),
                "평균기온": it.get("avgTa", ""),
                "최저기온": it.get("minTa", ""),
                "최고기온": it.get("maxTa", ""),
            })

        total = int(body.get("totalCount", 0) or 0)
        if page * 999 >= total:
            break
        page += 1
        time.sleep(0.3)

    return pd.DataFrame(rows, columns=COLS)
