import React, { useEffect, useRef } from 'react';
import styles from './styles.module.css';
import Message from './Message';

const ChatWindow = ({ messages, onClose, onSendMessage, inputText, setInputText, isLoading, streamedResponse }) => {
  const messagesEndRef = useRef(null);
  const chatMessagesRef = useRef(null);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSendMessage();
    }
  };

  // Scroll to bottom whenever messages change or streamed response updates
  useEffect(() => {
    if (chatMessagesRef.current) {
      chatMessagesRef.current.scrollTop = chatMessagesRef.current.scrollHeight;
    }
  }, [messages, streamedResponse]);

  return (
    <div className={`${styles.chatWindow} ${styles.open}`}>
      <div className={styles.chatHeader}>
        <span className={styles.chatTitle}>Physical AI & Robotics Assistant</span>
        <button className={styles.closeButton} onClick={onClose} aria-label="Close chat">
          ×
        </button>
      </div>

      <div className={styles.chatMessages} ref={chatMessagesRef}>
        {messages.map((message, index) => (
          <Message key={index} message={message} />
        ))}
        {streamedResponse && (
          <div className={`${styles.message} ${styles.agentMessage}`}>
            <div className={styles.messageContent}>
              {streamedResponse}
              <div className={styles.typingIndicator}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        {isLoading && !streamedResponse && (
          <div className={styles.message + ' ' + styles.agentMessage}>
            <div className={styles.messageContent}>
              <div className={styles.typingIndicator}>
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className={styles.chatInputArea}>
        <textarea
          className={styles.chatInput}
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask about Physical AI or Humanoid Robotics..."
          rows={1}
          disabled={isLoading}
        />
        <button
          className={styles.sendButton}
          onClick={onSendMessage}
          disabled={isLoading || !inputText.trim()}
        >
          Send
        </button>
      </div>
    </div>
  );
};

export default ChatWindow;