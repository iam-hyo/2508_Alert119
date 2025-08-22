네, 이 프로젝트에 대한 README 파일을 작성해 드릴게요. 아래 내용을 프로젝트 최상위 폴더에 README.md 파일로 저장하여 사용하시면 됩니다.

🔥 알림 119: MVP 문자 전송 시스템
## 1. 프로젝트 개요
알림 119는 화재 경보음(RNN) 및 경고등(CNN) 감지 시 지정된 수신자에게 자동으로 긴급 알림 문자를 전송하는 시스템의 MVP(Minimum Viable Product) 버전입니다.

본 MVP 프로젝트의 핵심 목표는 실제 감지 모델 연동에 앞서, Solapi(구 coolSMS) API를 활용하여 안정적인 문자 메시지 전송 환경을 구축하고 기술적 타당성을 검증하는 것입니다.

## 2. 핵심 기능
📞 수신자 관리: JSON 파일을 통해 관리자/입주민 역할, 이름, 전화번호를 관리합니다.

✉️ 문자 메시지 전송: 웹 UI에서 전송할 메시지 내용을 작성하고, 등록된 수신자를 선택하여 문자를 보냅니다.

⚙️ 백엔드 API: 연락처 관리 및 문자 전송 요청을 처리하는 Flask 기반의 REST API를 제공합니다.

🖥️ 프론트엔드 UI: 사용자가 수신자를 추가하고 문자를 보낼 수 있는 간단한 React 기반 웹 인터페이스를 제공합니다.

## 3. 기술 스택
Backend: Python, Flask

Frontend: React (Vite), JavaScript, HTML/CSS

API: Solapi (coolSMS) Messages V4 API

Data Store: JSON (contacts.json)

Dependencies:

Python: requests, python-dotenv, Flask-Cors

JavaScript: axios

## 4. 프로젝트 구조
alarm119_mvp/
├── backend/
│   ├── app.py          # Flask 메인 애플리케이션
│   ├── contacts.json   # 연락처 데이터
│   ├── .env            # API 키 등 민감 정보 (Git 추적 안 됨)
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx     # 메인 애플리케이션 컴포넌트
    │   └── ...
    └── package.json
## 5. 설치 및 실행 방법
### 사전 요구사항
Python 3.9+

Node.js 및 npm

Git

### 1. 프로젝트 클론
Bash

git clone [저장소 URL]
cd alarm119_mvp
### 2. 백엔드 설정
두 개의 터미널 창이 필요합니다.

🖥️ 터미널 1을 열고 아래 명령어를 순서대로 실행하세요.

Bash

# 1. backend 폴더로 이동
cd backend

# 2. Python 가상환경 생성 및 활성화
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate

# 3. 필요한 라이브러리 설치
pip install -r requirements.txt

# 4. .env 파일 설정
# .env 파일을 생성하고 아래 내용을 채워넣으세요.
# API 키와 발신번호는 Solapi 사이트에서 발급받아야 합니다.
# (발신번호는 반드시 Solapi에 등록 및 인증이 완료되어야 합니다.)
backend/.env 파일 내용
COOLSMS_API_KEY="NCS..."
COOLSMS_API_SECRET="YOUR_API_SECRET"
SENDER_PHONE_NUMBER="YOUR_SENDER_NUMBER"
### 3. 프론트엔드 설정
🖥️ 터미널 2를 열고 아래 명령어를 순서대로 실행하세요.

Bash

# 1. frontend 폴더로 이동 (프로젝트 최상위 폴더 기준)
cd frontend

# 2. 필요한 라이브러리 설치
npm install
### 4. 프로젝트 실행
두 개의 터미널을 각각 사용하여 백엔드와 프론트엔드 서버를 실행합니다.

🖥️ 터미널 1 (백엔드)

Bash

# (backend 폴더, 가상환경 활성화 상태)
flask run
# * 백엔드 서버가 http://127.0.0.1:5000 에서 실행됩니다.
🖥️ 터미널 2 (프론트엔드)

Bash

# (frontend 폴더)
npm run dev
# * 프론트엔드 서버가 http://localhost:5173 (또는 다른 포트) 에서 실행됩니다.
이제 웹 브라우저에서 프론트엔드 서버 주소(http://localhost:5173)로 접속하여 서비스를 사용할 수 있습니다.

## 6. 향후 계획
🧠 실제 감지 모듈 연동: RNN/CNN 모델의 감지 신호를 받아 자동으로 문자 전송 API를 호출하도록 연동

💾 데이터베이스 도입: contacts.json 대신 SQLite 또는 다른 RDBMS를 사용하여 수신자 정보를 안정적으로 관리

📈 전송 로그 기록: 문자 전송 성공/실패 여부, 시간 등을 DB에 기록하여 관리 및 분석 기능 추가
