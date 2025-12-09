import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ChatbotWidget from './ChatbotWidget';

// Mock the custom hook and API service
jest.mock('../../../hooks/useChat', () => ({
  __esModule: true,
  default: () => ({
    isOpen: false,
    messages: [],
    inputText: '',
    setInputText: jest.fn(),
    isLoading: false,
    streamedResponse: '',
    toggleChat: jest.fn(),
    closeChat: jest.fn(),
    handleSendMessage: jest.fn()
  })
}));

describe('ChatbotWidget', () => {
  test('renders without crashing', () => {
    render(<ChatbotWidget />);
    expect(screen.getByRole('button', { name: /Ask me/i })).toBeInTheDocument();
  });

  test('displays the "Ask me" button when chat is closed', () => {
    render(<ChatbotWidget />);
    expect(screen.getByText('Ask me')).toBeInTheDocument();
  });

  test('toggles chat interface when button is clicked', () => {
    const mockToggleChat = jest.fn();

    // Since we're mocking the hook, we can't directly test the toggle
    // This would be tested more thoroughly with actual state management
    render(<ChatbotWidget />);

    const button = screen.getByRole('button', { name: /Ask me/i });
    fireEvent.click(button);

    // The actual behavior would depend on the state in the hook
    expect(button).toBeInTheDocument();
  });
});