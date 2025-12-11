import { useState, useRef, useEffect } from 'react';
import apiService from '../services/apiService';

const useChat = () => {
  // Initialize state with values from localStorage if available
  const [isOpen, setIsOpen] = useState(() => {
    if (typeof window !== 'undefined') {
      const savedOpen = localStorage.getItem('chatbotOpen');
      return savedOpen ? JSON.parse(savedOpen) : false;
    }
    return false; // Default value during SSR
  });

  const [messages, setMessages] = useState(() => {
    if (typeof window !== 'undefined') {
      const savedMessages = localStorage.getItem('chatbotMessages');
      return savedMessages ? JSON.parse(savedMessages) : [];
    }
    return []; // Default value during SSR
  });

  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const [sessionId, setSessionId] = useState(() => {
    if (typeof window !== 'undefined') {
      const savedSessionId = localStorage.getItem('chatbotSessionId');
      return savedSessionId || null;
    }
    return null; // Default value during SSR
  });

  const [streamedResponse, setStreamedResponse] = useState('');
  const fullResponseRef = useRef('');

  // Save state to localStorage whenever it changes
  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('chatbotOpen', JSON.stringify(isOpen));
    }
  }, [isOpen]);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      localStorage.setItem('chatbotMessages', JSON.stringify(messages));
    }
  }, [messages]);

  useEffect(() => {
    if (typeof window !== 'undefined' && sessionId) {
      localStorage.setItem('chatbotSessionId', sessionId);
    }
  }, [sessionId]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const closeChat = () => {
    setIsOpen(false);
  };

  const handleSendMessage = async () => {
    if (!inputText.trim()) return;

    // Generate session ID if not already set
    const currentSessionId = sessionId || `session-${Date.now()}`;
    if (!sessionId) {
      setSessionId(currentSessionId);
    }

    // Add user message to chat
    const userMessage = {
      text: inputText,
      sender: 'user',
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    setStreamedResponse(''); // Clear any previous streamed response
    fullResponseRef.current = ''; // Reset the ref

    try {
      // Try to use streaming API first
      await apiService.streamMessage(
        inputText,
        currentSessionId,
        (chunk) => {
          // Update the streamed response progressively
          setStreamedResponse(prev => prev + chunk);
          fullResponseRef.current += chunk; // Also update the ref for later use
        }
      );

      // After streaming is complete, add the final response to messages
      if (fullResponseRef.current) {
        const agentMessage = {
          text: fullResponseRef.current,
          sender: 'agent',
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, agentMessage]);
      }
    } catch (streamError) {
      console.error('Error with streaming, falling back to regular API:', streamError);

      try {
        // Fallback to regular API call
        const response = await apiService.sendMessage(inputText, currentSessionId);

        const agentMessage = {
          text: response.response.content,
          sender: 'agent',
          timestamp: new Date().toISOString()
        };

        setMessages(prev => [...prev, agentMessage]);
      } catch (regularError) {
        console.error('Error with regular API:', regularError);
        const errorMessage = {
          text: "Sorry, I encountered an error processing your request. Please try again.",
          sender: 'agent',
          timestamp: new Date().toISOString()
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } finally {
      setIsLoading(false);
      setStreamedResponse(''); // Clear the streamed response after completion
      fullResponseRef.current = ''; // Clear the ref
    }
  };

  const clearChat = () => {
    setMessages([]);
    setSessionId(null);
    if (typeof window !== 'undefined') {
      localStorage.removeItem('chatbotMessages');
      localStorage.removeItem('chatbotSessionId');
    }
  };

  return {
    isOpen,
    setIsOpen,
    messages,
    setMessages,
    inputText,
    setInputText,
    isLoading,
    sessionId,
    streamedResponse,
    toggleChat,
    closeChat,
    handleSendMessage,
    clearChat
  };
};

export default useChat;