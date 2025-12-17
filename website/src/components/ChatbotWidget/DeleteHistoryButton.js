import React from 'react';
import styles from './DeleteHistoryButton.module.css';

const DeleteHistoryButton = ({ onDeleteHistory, disabled = false }) => {
  const handleClick = () => {
    if (!disabled) {
      onDeleteHistory();
    }
  };

  return (
    <button
      className={`${styles.deleteHistoryButton} ${disabled ? styles.disabled : ''}`}
      onClick={handleClick}
      title="Delete Chat History"
      disabled={disabled}
      aria-label="Delete chat history"
    >
      <svg
        className={styles.deleteIcon}
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M19 7L18.1327 19.1425C18.0579 20.1891 17.187 21 16.1378 21H7.86224C6.81296 21 5.94208 20.1891 5.86732 19.1425L5 7M10 11V17M14 11V17M15 7V4C15 3.44772 14.5523 3 14 3H10C9.44772 3 9 3.44772 9 4V7M4 7H20"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
      <span className={styles.buttonText}>Clear</span>
    </button>
  );
};

export default DeleteHistoryButton;