import React, { useState } from 'react';

function ContactList({ contacts, onSendSms }) {
  const [selected, setSelected] = useState([]);
  const [message, setMessage] = useState('');

  const handleSelect = (id) => {
    if (selected.includes(id)) {
      setSelected(selected.filter(item => item !== id));
    } else {
      setSelected([...selected, id]);
    }
  };
  
  const handleSelectAll = (e) => {
      if(e.target.checked) {
          setSelected(contacts.map(c => c.id));
      } else {
          setSelected([]);
      }
  }

  const handleSend = () => {
    onSendSms(selected, message);
  };

  return (
    <div className="list-container">
      <h2>문자 전송</h2>
      <div className="message-form">
        <textarea
          placeholder="전송할 메시지를 입력하세요..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
        ></textarea>
        <button onClick={handleSend} className="send-btn">전송</button>
      </div>

      <h3>수신자 목록</h3>
      <table>
        <thead>
          <tr>
            <th><input type="checkbox" onChange={handleSelectAll} /></th>
            <th>역할</th>
            <th>이름</th>
            <th>전화번호</th>
          </tr>
        </thead>
        <tbody>
          {contacts.map(contact => (
            <tr key={contact.id}>
              <td>
                <input
                  type="checkbox"
                  checked={selected.includes(contact.id)}
                  onChange={() => handleSelect(contact.id)}
                />
              </td>
              <td>{contact.role}</td>
              <td>{contact.name}</td>
              <td>{contact.phone}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ContactList;