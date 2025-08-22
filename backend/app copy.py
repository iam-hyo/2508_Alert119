import json
import os
import time
import hmac
import hashlib
from datetime import datetime, timezone
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import requests

# .env 파일에서 환경 변수 로드
load_dotenv()

app = Flask(__name__)
# React 앱(localhost:3000)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})


CONTACTS_FILE = 'contacts.json'

# --- 연락처 관리 Helper 함수 ---
def read_contacts():
    """contacts.json 파일에서 연락처 목록을 읽어옵니다."""
    try:
        with open(CONTACTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def write_contacts(contacts):
    """연락처 목록을 contacts.json 파일에 저장합니다."""
    with open(CONTACTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(contacts, f, ensure_ascii=False, indent=2)

# --- coolSMS API 서명 생성 함수 ---
def get_signature(api_secret, salt):
    """coolSMS API 요청을 위한 서명을 생성합니다."""
    return hmac.new(api_secret.encode(), salt.encode(), hashlib.sha256).hexdigest()


# --- API 엔드포인트 ---
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    """모든 연락처 정보를 반환합니다."""
    contacts = read_contacts()
    return jsonify(contacts)

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    """새로운 연락처를 추가합니다."""
    new_contact = request.json
    contacts = read_contacts()
    
    # 새 ID 생성 (가장 큰 ID + 1)
    new_contact['id'] = max([c['id'] for c in contacts] or [0]) + 1
    contacts.append(new_contact)
    
    write_contacts(contacts)
    return jsonify({"status": "success", "contact": new_contact}), 201

@app.route('/api/send-sms', methods=['POST'])
def send_sms():
    """[최종 수정 2] 선택된 수신자에게 SMS를 발송합니다."""
    data = request.json
    to_numbers = data.get('to')
    text = data.get('text')

    api_key = os.getenv('COOLSMS_API_KEY')
    api_secret = os.getenv('COOLSMS_API_SECRET')
    sender_number = os.getenv('SENDER_PHONE_NUMBER')

    if not to_numbers or not text:
        return jsonify({"status": "error", "message": "수신자 번호나 메시지 내용이 없습니다."}), 400

    # --- 👇 이 부분이 올바르게 수정되었는지 반드시 확인하세요 ---
    # 서명(Signature) 생성을 위한 nonce(단순 문자열) 생성
    nonce = str(int(time.time()))
    # Date 헤더를 위한 ISO 8601 형식의 날짜 문자열 생성
    iso_date_string = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    
    # 서명은 nonce 값을 이용해 생성합니다.
    signature = get_signature(api_secret, nonce)
    # -----------------------------------------------------------
    
    url = "https://api.coolsms.co.kr/messages/v4/send-many"
    
    headers = {
        # 헤더의 Date 값은 ISO 8601 형식을 사용합니다.
        'Authorization': f'HMAC-SHA256 ApiKey={api_key}, Date={iso_date_string}, Signature={signature}',
        'Content-Type': 'application/json'
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
        # --- 👇 터미널에 에러를 직접 출력하는 코드 추가! ---
        print("\n!!! [RequestException] 에러가 발생했습니다 !!!")
        print(f"요청 URL: {e.request.url if e.request else 'N/A'}")
        print(f"에러 내용: {str(e)}")
        if e.response is not None:
            print(f"서버 응답 코드: {e.response.status_code}")
            print(f"서버 응답 내용: {e.response.text}")
        print("-------------------------------------------\n")
        # ---------------------------------------------------
        
        error_response = e.response.json() if e.response is not None and 'application/json' in e.response.headers.get('Content-Type', '') else str(e)
        return jsonify({"status": "error", "message": error_response}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)