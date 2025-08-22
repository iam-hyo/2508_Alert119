import React, { useState } from 'react';

function ContactForm({ onAddContact }) {
  const [role, setRole] = useState('입주민');
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!name || !phone) {
      alert("이름과 전화번호를 모두 입력해주세요.");
      return;
    }
    onAddContact({ role, name, phone });
    // 입력 필드 초기화
    setName('');
    setPhone('');
  };

  return (
    <div className="form-container">
      <h2>새 연락처 추가</h2>
      <form onSubmit={handleSubmit}>
        <select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="입주민">입주민</option>
          <option value="관리자">관리자</option>
        </select>
        <input
          type="text"
          placeholder="이름"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <input
          type="tel"
          placeholder="전화번호 (예: 01012345678)"
          value={phone}
          onChange={(e) => setPhone(e.target.value)}
        />
        <button type="submit">저장</button>
      </form>
    </div>
  );
}

export default ContactForm;