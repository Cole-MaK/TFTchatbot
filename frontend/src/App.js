import { useState, useEffect, useRef } from 'react';
import './App.css';

// Define suggested messages here - easy to change later
const SUGGESTED_MESSAGES = [
  "What traits are good with 6 vanguard?",
  "What front line champions do you play with 3 star Twisted Fate?",
  "Does Viego or Renekton have a higher win rate with 7 anima squad?",
  "What are good non boom bot champions to play in 6 boom bots?",
  "Is 4 techie or 4 strategist better with 7 street demon?"
];

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [shouldAutoScroll, setShouldAutoScroll] = useState(true);
  const chatContainerRef = useRef(null);
  
  // Auto-scroll to bottom when messages change if shouldAutoScroll is true
  useEffect(() => {
    if (shouldAutoScroll && chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, isLoading, shouldAutoScroll]);

  // Handle scroll events to determine if user has manually scrolled up
  const handleScroll = () => {
    if (chatContainerRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = chatContainerRef.current;
      // If the user is near the bottom (within 100px), enable auto-scrolling
      const isNearBottom = scrollHeight - scrollTop - clientHeight < 100;
      setShouldAutoScroll(isNearBottom);
    }
  };

  const sendMessage = async (messageText) => {
    if (!messageText.trim()) return;
    
    // Add user message
    const userMessage = { text: messageText, isUser: true };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInput('');
    setIsLoading(true);
    
    // Enable auto-scrolling when sending a new message
    setShouldAutoScroll(true);
    
    try {
      // Send message to backend
      const response = await fetch('http://localhost:5000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_message: messageText })
      });
      
      const data = await response.json();
      
      // Add bot response
      const botMessage = { text: data.message, isUser: false };
      setMessages(prevMessages => [...prevMessages, botMessage]);
      
    } catch (error) {
      console.error('Error:', error);
      const errorMessage = { text: 'Error: Could not reach the server.', isUser: false };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await sendMessage(input);
  };

  const handleSuggestionClick = async (suggestion) => {
    setInput(suggestion); // Set the input field (not necessary but gives visual feedback)
    await sendMessage(suggestion);
  };

  return (
    <div className="app">
      <header>
        <h1>TFT Chatbot</h1>
      </header>
      
      <div 
        className="chat-container" 
        ref={chatContainerRef}
        onScroll={handleScroll}
      >
        {messages.map((message, index) => (
          <div 
            key={index} 
            className={`message ${message.isUser ? 'user-message' : 'bot-message'}`}
          >
            {message.text}
          </div>
        ))}
        {isLoading && (
          <div className="message bot-message loading">
            Thinking...
          </div>
        )}
      </div>
      
      <div className="suggestion-container">
        {SUGGESTED_MESSAGES.map((suggestion, index) => (
          <button 
            key={index}
            className="suggestion-bubble"
            onClick={() => handleSuggestionClick(suggestion)}
            disabled={isLoading}
          >
            {suggestion}
          </button>
        ))}
      </div>
      
      <form className="input-form" onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message here..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          Send
        </button>
      </form>
    </div>
  );
}

export default App;
