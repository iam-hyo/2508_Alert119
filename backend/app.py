# ================= app.py (공식 문서 기반 최종 버전) =================

import json
import os
import time
import hmac
import hashlib
from datetime import datetime, timezone
import requests # requests import 확인
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)
# React 앱(localhost:5173)에서의 요청을 허용
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


CONTACTS_FILE = 'contacts.json'

# --- Helper 함수들 ---
def read_contacts():
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_contacts(contacts):
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

def get_signature(api_secret, message):
    """HMAC-SHA256 서명을 생성합니다. (메시지 기반으로 변경)"""
    return hmac.new(api_secret.encode(), message.encode(), hashlib.sha256).hexdigest()

# --- API 엔드포인트 ---
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    contacts = read_contacts()
    return jsonify(contacts)

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    new_contact = request.json
    contacts = read_contacts()
    new_contact['id'] = max([c.get('id', 0) for c in contacts] or [0]) + 1
    contacts.append(new_contact)
    write_contacts(contacts)
    return jsonify({"status": "success", "contact": new_contact}), 201

@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    """문자 메시지를 발송합니다. (공식 문서 기반 최종 버전)"""
    data = request.json
    to_numbers = data.get('to')
    text = data.get('text')

    api_key = os.getenv('COOLSMS_API_KEY')
    api_secret = os.getenv('COOLSMS_API_SECRET')
    sender_number = os.getenv('SENDER_PHONE_NUMBER')

    if not all([api_key, api_secret, sender_number]):
        return jsonify({"status": "error", "message": "서버 환경 변수 설정 오류"}), 500
    
    if not to_numbers or not text:
        return jsonify({"status": "error", "message": "수신자 번호나 메시지 내용이 없습니다."}), 400

    # --- 👇 공식 문서에 따른 인증 로직 ---
    # 1. Salt 값 생성 (단순 타임스탬프를 사용해도 무방)
    salt = str(int(time.time()))
    # 2. Date 값 생성 (ISO 8601 형식)
    date = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    # 3. 서명할 메시지 생성 (date + salt)
    message = date + salt
    # 4. 서명 생성
    signature = get_signature(api_secret, message)
    # ------------------------------------
    
    url = "https://api.solapi.com/messages/v4/send-many" # URL도 solapi.com으로 변경
    
    headers = {
        # 헤더에 반드시 ApiKey, Date, Salt, Signature 4개가 모두 포함되어야 합니다.
        'Authorization': f'HMAC-SHA256 ApiKey={api_key}, Date={date}, Salt={salt}, Signature={signature}',
        'Content-Type': 'application/json; charset=utf-8' # charset=utf-8 추가
    }
    
    payload = {
        "messages": [
            {"to": number, "from": sender_number, "text": text} for number in to_numbers
        ]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return jsonify({"status": "success", "response": response.json()})

    except requests.exceptions.RequestException as e:
        # 에러 로깅 강화
        print(f"!!! 요청 실패: {e}")
        if e.response is not None:
            print(f"응답 코드: {e.response.status_code}")
            print(f"응답 내용: {e.response.text}")
        return jsonify({"status": "error", "message": e.response.text if e.response is not None else str(e)}), 500