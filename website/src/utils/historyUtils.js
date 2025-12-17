/**
 * Utility functions for managing chat history
 */

/**
 * Validates that the history follows the required format:
 * [{"role":"user","content":"..."},{"role":"assistant","content":"..."}]
 * @param {Array} history - The chat history array to validate
 * @returns {boolean} - True if valid, false otherwise
 */
export const validateHistoryFormat = (history) => {
  if (!Array.isArray(history)) {
    return false;
  }

  for (const item of history) {
    if (
      typeof item !== 'object' ||
      typeof item.role !== 'string' ||
      typeof item.content !== 'string' ||
      !['user', 'assistant'].includes(item.role)
    ) {
      return false;
    }
  }

  return true;
};

/**
 * Formats messages from the internal format to the required API format
 * Internal format: {text, sender, timestamp}
 * API format: {content, role}
 * @param {Array} messages - Array of messages in internal format
 * @returns {Array} - Array of messages in API format
 */
export const formatHistoryForAPI = (messages) => {
  return messages.map(msg => ({
    role: msg.sender === 'user' ? 'user' : 'assistant',
    content: msg.text
  }));
};

/**
 * Formats messages from API format to internal format
 * API format: {content, role}
 * Internal format: {text, sender, timestamp}
 * @param {Array} history - Array of messages in API format
 * @returns {Array} - Array of messages in internal format
 */
export const formatHistoryFromAPI = (history) => {
  return history.map(item => ({
    text: item.content,
    sender: item.role === 'user' ? 'user' : 'agent',
    timestamp: new Date().toISOString()
  }));
};

/**
 * Sanitizes history to prevent injection attacks
 * @param {Array} history - The history to sanitize
 * @returns {Array} - Sanitized history
 */
export const sanitizeHistory = (history) => {
  if (!Array.isArray(history)) {
    return [];
  }

  return history.map(item => ({
    role: typeof item.role === 'string' ? item.role : 'user',
    content: typeof item.content === 'string' ? item.content : ''
  }));
};

/**
 * Limits history length to prevent performance issues
 * @param {Array} history - The history to limit
 * @param {number} maxLength - Maximum number of items (default: 50)
 * @returns {Array} - Limited history
 */
export const limitHistoryLength = (history, maxLength = 50) => {
  if (!Array.isArray(history)) {
    return [];
  }

  // Return the most recent messages up to maxLength
  return history.slice(-maxLength);
};

/**
 * Serializes history for storage (localStorage, etc.)
 * @param {Array} history - The history to serialize
 * @returns {string} - JSON string of the history
 */
export const serializeHistory = (history) => {
  try {
    return JSON.stringify(history);
  } catch (error) {
    console.error('Error serializing history:', error);
    return JSON.stringify([]);
  }
};

/**
 * Deserializes history from storage
 * @param {string} serializedHistory - The serialized history string
 * @returns {Array} - Deserialized history array
 */
export const deserializeHistory = (serializedHistory) => {
  try {
    if (typeof serializedHistory !== 'string' || serializedHistory === '') {
      return [];
    }
    const parsed = JSON.parse(serializedHistory);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    console.error('Error deserializing history:', error);
    return [];
  }
};

/**
 * Gets history from localStorage
 * @param {string} key - The localStorage key (default: 'chatbotMessages')
 * @returns {Array} - History from localStorage or empty array
 */
export const getHistoryFromStorage = (key = 'chatbotMessages') => {
  if (typeof window === 'undefined') {
    return [];
  }

  const serializedHistory = localStorage.getItem(key);
  return deserializeHistory(serializedHistory);
};

/**
 * Saves history to localStorage
 * @param {Array} history - The history to save
 * @param {string} key - The localStorage key (default: 'chatbotMessages')
 */
export const saveHistoryToStorage = (history, key = 'chatbotMessages') => {
  if (typeof window === 'undefined') {
    return;
  }

  const serializedHistory = serializeHistory(history);
  localStorage.setItem(key, serializedHistory);
};