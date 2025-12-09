import React from 'react';
import ChatButton from './ChatButton';
import ChatWindow from './ChatWindow';
import useChat from '../../hooks/useChat';
import styles from './styles.module.css';

const ChatbotWidget = () => {
  const {
    isOpen,
    messages,
    inputText,
    setInputText,
    isLoading,
    streamedResponse,
    toggleChat,
    closeChat,
    handleSendMessage
  } = useChat();

  return (
    <div className={styles.chatbotContainer}>
      {!isOpen && <ChatButton onClick={toggleChat} isOpen={isOpen} />}
      {isOpen && (
        <ChatWindow
          messages={messages}
          onClose={closeChat}
          onSendMessage={handleSendMessage}
          inputText={inputText}
          setInputText={setInputText}
          isLoading={isLoading}
          streamedResponse={streamedResponse}
        />
      )}
    </div>
  );
};

export default ChatbotWidget;