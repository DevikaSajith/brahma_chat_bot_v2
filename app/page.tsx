'use client';

import { useState, useRef, useEffect } from 'react';

// 1. Define the shape of the message object
interface Message {
  role: 'bot' | 'user';
  text: string;
}

export default function Home() {
  // 2. Add types to State hooks
  const [messages, setMessages] = useState<Message[]>([
    { role: 'bot', text: 'Welcome to Brahma \'26. How can I assist you?' }
  ]);
  const [input, setInput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);

  // 3. Add type to useRef (HTMLDivElement is the specific type for a <div>)
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { role: 'user', text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.text }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: 'bot', text: data.reply }]);
    } catch (e) {
      setMessages((prev) => [...prev, { role: 'bot', text: 'Error: System Offline' }]);
    } finally {
      setLoading(false);
    }
  };

  // 4. Helper for type-safe keyboard events
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      <div className="tape-strip">AI ASSISTANT // V.26</div>

      <div className="chat-header">
        <div style={{ display: 'flex', alignItems: 'center' }}>
          {/* Ensure the file name matches your public folder exactly */}
          <img src="/brahma_logo.jpg" alt="Logo" className="header-logo" />
          <h1 className="chat-title">BRAHMA <span style={{ color: 'var(--brahma-cyan)' }}>BOT</span></h1>
        </div>
        <div className="status-dot"></div>
      </div>

      <div className="chat-body" ref={scrollRef}>
        <img src="/brahma_logo.jpg" className="watermark" alt="" />

        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role === 'user' ? 'user-msg' : 'bot-msg'}`}>
            {msg.role === 'bot' && <strong>SYSTEM: </strong>}
            {msg.text}
          </div>
        ))}

        {loading && <div className="message bot-msg">Processing...</div>}
      </div>

      <div className="input-area">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type command..." 
          autoComplete="off"
        />
        <button onClick={sendMessage}>SEND</button>
      </div>
    </div>
  );
}