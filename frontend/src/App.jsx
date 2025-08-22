import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ContactList from './components/ContactList';
import ContactForm from './components/ContactForm';
import './App.css';

const API_URL = 'http://127.0.0.1:5000/api';

function App() {
  const [contacts, setContacts] = useState([]);

  // 컴포넌트 마운트 시 연락처 데이터 로드
  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    try {
      const response = await axios.get(`${API_URL}/contacts`);
      setContacts(response.data);
    } catch (error) {
      console.error("연락처를 불러오는 중 오류 발생:", error);
    }
  };

  const handleAddContact = async (contact) => {
    try {
      await axios.post(`${API_URL}/contacts`, contact);
      fetchContacts(); // 연락처 추가 후 목록 새로고침
    } catch (error) {
      console.error("연락처 추가 중 오류 발생:", error);
    }
  };

  const handleSendSms = async (selectedContacts, message) => {
    if (selectedContacts.length === 0) {
      alert("문자를 보낼 대상을 선택해주세요.");
      return;
    }
    if (!message) {
      alert("메시지 내용을 입력해주세요.");
      return;
    }

    const toNumbers = selectedContacts.map(id => {
      const contact = contacts.find(c => c.id === parseInt(id));
      return contact.phone;
    });

    try {
      const response = await axios.post(`${API_URL}/send-sms`, {
        to: toNumbers,
        text: message
      });
      alert('문자 전송 요청 성공!');
      console.log('전송 결과:', response.data);
    } catch (error) {
      alert('문자 전송 요청 실패!');
      console.error("SMS 전송 중 오류 발생:", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🔥 알림 119 MVP</h1>
      </header>
      <main>
        <ContactForm onAddContact={handleAddContact} />
        <hr />
        <ContactList 
          contacts={contacts} 
          onSendSms={handleSendSms}
        />
      </main>
    </div>
  );
}

export default App;