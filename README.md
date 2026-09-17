# 대전 기온 데이터 (매일 자동 갱신)

기상청 ASOS 일자료를 이용해 **대전(지점 133)** 의 날짜별 평균/최저/최고 기온을 모읍니다.
서울 데이터( `greatsong/modudata/seoul.csv` )와 **열 구조가 완전히 같습니다.**

```
날짜,지점,평균기온,최저기온,최고기온
1969-01-01,133,-2.5,-7.8,3.1
...
```

- **과거 전체**: 대전 관측 개시(1969년) 이후 오늘까지
- **매일 자동**: 매일 아침(한국시간 07:00) 어제 하루치를 자동으로 추가

수업에서는 아래 주소 하나만 쓰면 됩니다(사용자명/저장소명은 본인 것으로 교체):

```
https://raw.githubusercontent.com/사용자명/저장소명/main/data/daejeon.csv
```

판다스에서:

```python
import pandas as pd
url = "https://raw.githubusercontent.com/사용자명/저장소명/main/data/daejeon.csv"
df = pd.read_csv(url)
```

---

## 설치 방법 (파이썬 설치 불필요, 전부 웹에서)

### 1단계. 무료 API 키 발급 (약 5분)

1. [공공데이터포털](https://www.data.go.kr) 회원가입 · 로그인
2. [기상청_지상(종관, ASOS) 일자료 조회서비스](https://www.data.go.kr/data/15059093/openapi.do) 접속
3. 오른쪽 위 **[활용신청]** 클릭 → 활용목적에 "교육/수업용" 등 간단히 적고 신청
   (자동 승인이라 바로 사용 가능)
4. 마이페이지 → **오픈API → 인증키**에서 **일반 인증키(Decoding)** 값을 복사해 둡니다.
   ⚠️ **Encoding 이 아니라 Decoding** 키를 씁니다.

### 2단계. 이 폴더를 내 깃허브 저장소로 올리기

1. [github.com](https://github.com) 로그인 → **New repository** 로 새 저장소 생성
   (이름 예: `daejeon-temp`, **Public** 권장)
2. 이 폴더 안의 파일 전부를 그 저장소에 업로드
   (웹에서 **Add file → Upload files** 로 `scripts`, `.github`, `data`, `requirements.txt`,
   `README.md` 를 통째로 드래그해 올리면 됩니다)

### 3단계. API 키를 저장소 비밀값으로 등록

1. 저장소 → **Settings → Secrets and variables → Actions**
2. **New repository secret** 클릭
3. Name 에 `DATA_GO_KR_KEY`, Secret 에 1단계에서 복사한 **Decoding 키**를 붙여넣고 저장

### 4단계. 과거 데이터 한 번에 수집 (1회만)

1. 저장소 → **Actions** 탭 (처음이면 "I understand my workflows, enable them" 클릭)
2. 왼쪽 목록에서 **"과거 데이터 전체 수집 (1회)"** 선택
3. 오른쪽 **Run workflow** 버튼 클릭 → 잠시 기다리면 `data/daejeon.csv` 가 과거 전체로 채워집니다.

### 5단계. 끝. 이제 매일 자동으로 갱신됩니다

- **"대전 기온 매일 갱신"** 워크플로가 매일 아침 7시(KST)에 어제 데이터를 자동으로 붙입니다.
- 하루 이틀 놓쳐도 다음 실행 때 빠진 날짜를 알아서 모두 채웁니다.

---

## 파일 설명

| 파일 | 역할 |
|---|---|
| `scripts/kma.py` | 기상청 API 호출 공통 코드 (지점번호 133 = 대전) |
| `scripts/backfill.py` | 과거 전체 수집 (1회) |
| `scripts/update.py` | 어제 하루치 추가 (매일) |
| `.github/workflows/backfill.yml` | 4단계 버튼 실행용 |
| `.github/workflows/daily.yml` | 매일 아침 자동 실행 |
| `data/daejeon.csv` | 결과 데이터 |

## 다른 도시로 바꾸려면

`scripts/kma.py` 의 `STN_ID` 값만 바꾸면 됩니다. (서울 108, 대전 133, 부산 159, 대구 143, 광주 156, 인천 112 …)
