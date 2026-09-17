# -*- coding: utf-8 -*-
"""
기상청 ASOS 일자료 조회 공통 모듈.
대전(지점 133)의 날짜별 평균/최저/최고 기온을 받아온다.
서울 csv와 열 구조를 똑같이 맞춘다: 날짜, 지점, 평균기온, 최저기온, 최고기온
"""
import os
import time
import requests
import pandas as pd

# 공공데이터포털에서 발급받은 "디코딩(Decoding) 인증키"를 환경변수로 전달받는다.
SERVICE_KEY = os.environ["DATA_GO_KR_KEY"]

STN_ID = "133"  # 대전 관측소 지점번호 (서울은 108)
URL = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"
COLS = ["날짜", "지점", "평균기온", "최저기온", "최고기온"]


def fetch_range(start_dt: str, end_dt: str) -> pd.DataFrame:
    """start_dt, end_dt 는 'YYYYMMDD' 문자열. 해당 기간 대전 일별 기온을 DataFrame 으로 반환."""
    rows = []
    page = 1
    while True:
        params = {
            "serviceKey": SERVICE_KEY,
            "pageNo": page,
            "numOfRows": 999,          # 한 번에 최대 999행
            "dataType": "JSON",
            "dataCd": "ASOS",
            "dateCd": "DAY",           # 일자료
            "startDt": start_dt,
            "endDt": end_dt,
            "stnIds": STN_ID,
        }
        resp = requests.get(URL, params=params, timeout=30)
        resp.raise_for_status()

        try:
            body = resp.json()["response"]["body"]
        except Exception:
            # 인증키 오류 등으로 JSON 이 아니면 원문을 보여주고 중단
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

        total = int(body.get("totalCount", 0))
        if page * 999 >= total:
            break
        page += 1
        time.sleep(0.3)  # 서버 배려

    return pd.DataFrame(rows, columns=COLS)
