import React from 'react';
import styles from './styles.module.css';

const Message = ({ message }) => {
  const isUser = message.sender === 'user';

  return (
    <div className={`${styles.message} ${isUser ? styles.userMessage : styles.agentMessage}`}>
      <div className={styles.messageContent}>
        {message.text}
      </div>
      <div className={styles.messageTimestamp}>
        {message.timestamp ? new Date(message.timestamp).toLocaleTimeString() : ''}
      </div>
    </div>
  );
};

export default Message;