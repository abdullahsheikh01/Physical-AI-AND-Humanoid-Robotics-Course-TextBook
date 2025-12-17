// API service for chatbot communication
// In Docusaurus, we can't use process.env, so we'll use a default or window-based approach
const API_BASE_URL = typeof window !== 'undefined'
  ? window.ENV?.REACT_APP_API_URL || 'https://physical-ai-and-humanoid-robotics-course-ha5u.onrender.com'
  : 'https://physical-ai-and-humanoid-robotics-course-ha5u.onrender.com';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Method to send a chat message and get a response
  async sendMessage(query, sessionId = null, history = []) {
    try {
      // Format history to the required format [{"role":"user","content":"..."}]
      const formattedHistory = history.map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text
      }));

      const response = await fetch(`${this.baseUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          conversation_id: sessionId,
          history: formattedHistory
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  // Method to simulate streaming chat responses using the regular chat endpoint
  async streamMessage(query, sessionId = null, onChunk, history = []) {
    return new Promise(async (resolve, reject) => {
      try {
        // Since the backend doesn't support streaming, we'll call the regular endpoint
        // and simulate streaming by calling the onChunk callback with the full response
        const response = await this.sendMessage(query, sessionId, history);

        if (response && response.response) {
          // Simulate streaming by sending the full response as one chunk
          if (onChunk) {
            onChunk(response.response);
          }
        }

        resolve();
      } catch (error) {
        console.error('Error in streamMessage:', error);
        reject(error);
      }
    });
  }

  // Health check method
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseUrl}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  // Method to generate embeddings (for future use)
  async generateEmbeddings(text) {
    try {
      // For now, this endpoint doesn't exist in the backend, so we'll return an error
      throw new Error('generateEmbeddings endpoint not implemented in backend');
    } catch (error) {
      console.error('Error generating embeddings:', error);
      throw error;
    }
  }
}

export default new ApiService();