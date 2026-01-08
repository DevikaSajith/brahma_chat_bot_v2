'use client';

import { useState, useRef, useEffect } from 'react';

// 1. Define the Message interface
interface Message {
  role: 'bot' | 'user';
  text: string;
}

export default function Home() {
  // 2. Add type annotation to State
  const [messages, setMessages] = useState<Message[]>([
    { role: 'bot', text: 'Welcome to Brahma \'26. How can I assist you?' }
  ]);
  const [input, setInput] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  
  // 3. Add type annotation to Ref (HTMLDivElement for a div)
  const scrollRef = useRef<HTMLDivElement>(null);

  // Convert newlines to <br> and make URLs clickable
  const formatMessage = (text: string): string => {
    // Convert \n to <br>
    let formatted = text.replace(/\n/g, '<br>');
    
    // Make URLs clickable - match http:// or https:// but exclude closing parentheses
    formatted = formatted.replace(
      /(https?:\/\/[^\s<)]+)/g,
      '<a href="$1" target="_blank" rel="noopener noreferrer" style="color: #00d4ff; font-weight: bold; text-decoration: underline; cursor: pointer;">$1</a>'
    );
    
    return formatted;
  };

  // Auto-scroll
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    // Use a temporary variable for the user message before formatting
    const userMsgText = input;
    const userMsg: Message = { role: 'user', text: userMsgText };
    
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
        // Ensure process.env variable is typed as string (or undefined)
        const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
        
        const res = await fetch(
          `${backendUrl}/chat`,
          {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMsg.text }),
          }
        );

      const data = await res.json();
      // Format the bot's reply
      const formattedReply = formatMessage(data.reply);
      setMessages((prev) => [...prev, { role: 'bot', text: formattedReply }]);
    } catch (e) {
      setMessages((prev) => [...prev, { role: 'bot', text: 'Error: System Offline' }]);
    } finally {
      setLoading(false);
    }
  };

  // 4. Add type annotation for keyboard events
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
          {/* Ensure the image path is correct in your public folder */}
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
            {/* Using dangerouslySetInnerHTML to render the clickable links/br tags */}
            <div dangerouslySetInnerHTML={{ __html: msg.text }} />
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
