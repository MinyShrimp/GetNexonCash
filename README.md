# 넥슨캐쉬 사용내역 확인

## 환경

- 개발일자: **2025.02.02**
- `python`: 3.13.0
- `pip`: 25.0
- `git bash`

## 세팅

### 파이썬, git 최신 버전 설치

- https://www.python.org/
- https://git-scm.com/downloads

### 프로젝트 Copy

- 아래 코드는 `git bash`에서 실행
```
git clone https://github.com/MinyShrimp/GetNexonCash.git
cd GetNexonCash
```

### 파이썬 가상환경 설정

- 아래 코드는 `git bash`에서 실행
```
python.exe -m venv .venv
python.exe -m pip install --upgrade pip
source .venv/Scripts/activate
pip install -r requirements.txt
```

### 넥슨 NPP 코드 얻기

- 넥슨 로그인
- https://payment.nexon.com/usage 접속

![img](./imgs/넥슨캐쉬_사용내역.png)

- 브라우저 관리자 툴 열기 (`F12` 혹은 `Ctrl+Shift+I`)

![img](./imgs/개발자도구.png)

- 응용프로그램 -> 쿠키 -> `https://payment.nexon.com` -> `NPP`

![img](./imgs/개발자콘솔.png)

- `NPP` 값 복사


### .env 파일 설정

- `.env.copy` 파일 => `.env` 변경
- `your-npp-code`에 `NPP` 코드 입력

### 파이썬 코드 실행

```
python main.py
```

## 출력 예시 데이터

- 실제로는 숫자로 나옵니다

```
[넥슨]에서 사용한 총 금액: x,xxx,xxx
======================================================
[메이플스토리]에서 사용한 총 금액: x,xxx,xxx
------------------------------------------------------
  2020년: xxx,xxx
    12월: xxx,xxx
  2021년: x,xxx,xxx
    01월: x,xxx,xxx
    02월: xxx,xxx
    08월: xx,xxx
  2022년: x,xxx,xxx
    01월: xx,xxx
    07월: xx,xxx
    10월: xxx,xxx
    11월: x,xxx,xxx
    12월: xxx,xxx
  2023년: x,xxx,xxx
    09월: xx,xxx
    10월: xxx,xxx
    11월: xxx,xxx
    12월: xxx,xxx
  2024년: xxx,xxx
    01월: xxx,xxx
    09월: x,xxx
======================================================
[마비노기]에서 사용한 총 금액: x,xxx,xxx
------------------------------------------------------
  2024년: x,xxx,xxx
    06월: xxx,xxx
    07월: xxx,xxx
======================================================
[카트라이더: 드리프트]에서 사용한 총 금액: xx,xxx
------------------------------------------------------
  2024년: xx,xxx
    09월: xx,xxx
======================================================
```
