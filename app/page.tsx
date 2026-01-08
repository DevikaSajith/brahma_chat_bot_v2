'use client';

import { useState, useRef, useEffect } from 'react';

// 1. TypeScript Interface
interface Message {
  role: 'bot' | 'user';
  text: string;
}

export default function AshwamedhaChat() {
  // 2. State Management
  const [messages, setMessages] = useState<Message[]>([
    { role: 'bot', text: 'Ashwamedha System Online. Awaiting command.' }
  ]);
  const [input, setInput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  
  // 3. Scroll Ref
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  // 4. Send Message Logic
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMsg: Message = { role: 'user', text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      // --- ENVIRONMENT VARIABLE ---
      // Uses .env.local variable, defaults to /api/chat
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '/api/chat';

      const res = await fetch(apiUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg.text }),
      });

      if (!res.ok) throw new Error('Network response was not ok');

      const data = await res.json();
      setMessages((prev) => [...prev, { role: 'bot', text: data.reply }]);
    } catch (e) {
      console.error("Chat Error:", e);
      setMessages((prev) => [...prev, { role: 'bot', text: 'Signal Lost. Retrying...' }]);
    } finally {
      setLoading(false);
    }
  };

  // Handle "Enter" key
  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      sendMessage();
    }
  };

  return (
    <div className="chat-container">
      {/* --- HEADER --- */}
      <div className="chat-header">
        <div className="avatar-container">
            {/* Make sure ashwa_logo.jpg is in your public folder */}
            <img src="/ashwa_logo.jpg" alt="Avatar" className="avatar-img" />
        </div>
        <h1 className="title-text">ASHWAMEDHA BOT</h1>
      </div>

      {/* --- WATERMARK --- */}
      <img src="/ashwa_logo.jpg" className="bg-watermark" alt="" />

      {/* --- MESSAGES BODY --- */}
      <div className="chat-body" ref={scrollRef}>
        {messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role === 'user' ? 'user-msg' : 'bot-msg'}`}>
                {msg.text}
            </div>
        ))}

        {loading && (
            <div className="message bot-msg" style={{color: 'var(--ashwa-lavender)'}}>
                Processing Data...
            </div>
        )}
      </div>

      {/* --- INPUT AREA --- */}
      <div className="input-area">
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Transmit message..." 
        />
        <button onClick={sendMessage}>
            SEND <span>&gt;&gt;&gt;</span>
        </button>
      </div>
    </div>
  );
}