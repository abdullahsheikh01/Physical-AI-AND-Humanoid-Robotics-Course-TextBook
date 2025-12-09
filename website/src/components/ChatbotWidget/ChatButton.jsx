import React from 'react';
import styles from './styles.module.css';

const ChatButton = ({ onClick, isOpen }) => {
  return (
    <button
      className={`${styles.chatButton} ${isOpen ? styles.hidden : styles.visible}`}
      onClick={onClick}
      aria-label={isOpen ? "Close chat" : "Open chat"}
    >
      <span className={styles.buttonText}>Ask me</span>
    </button>
  );
};

export default ChatButton;