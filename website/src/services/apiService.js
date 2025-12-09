// API service for chatbot communication
// In Docusaurus, we can't use process.env, so we'll use a default or window-based approach
const API_BASE_URL = typeof window !== 'undefined'
  ? window.ENV?.REACT_APP_API_URL || 'http://localhost:8000'
  : 'http://localhost:8000';

class ApiService {
  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  // Method to send a chat message and get a response
  async sendMessage(query, sessionId = null) {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          session_id: sessionId
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

  // Method to stream chat responses using fetch and handling server-sent events
  async streamMessage(query, sessionId = null, onChunk) {
    return new Promise((resolve, reject) => {
      // Create the request payload
      const payload = JSON.stringify({
        query,
        session_id: sessionId
      });

      // Use fetch to POST the query and then handle the streaming response
      fetch(`${this.baseUrl}/api/v1/chat/stream`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: payload
      })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        // Handle the streaming response
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        function read() {
          reader.read().then(({ done, value }) => {
            if (done) {
              resolve();
              return;
            }

            // Decode the chunk
            const chunk = decoder.decode(value, { stream: true });
            buffer += chunk;

            // Process complete lines from the buffer
            let lineEndIndex;
            while ((lineEndIndex = buffer.indexOf('\n')) >= 0) {
              const line = buffer.substring(0, lineEndIndex);
              buffer = buffer.substring(lineEndIndex + 1);

              // Process server-sent event line
              if (line.startsWith('data: ')) {
                try {
                  const data = JSON.parse(line.slice(6)); // Remove 'data: ' prefix
                  if (data.content) {
                    // Call the provided callback with the content chunk
                    if (onChunk) {
                      onChunk(data.content);
                    }
                  } else if (data.error) {
                    console.error('Streaming error:', data.error);
                    reject(new Error(data.error));
                    return;
                  }
                } catch (e) {
                  console.error('Error parsing stream data:', e);
                }
              }
            }

            // Continue reading
            read();
          }).catch(err => {
            console.error('Error reading stream:', err);
            reject(err);
          });
        }

        read();
      })
      .catch(error => {
        console.error('Error initiating stream:', error);
        reject(error);
      });
    });
  }

  // Health check method
  async healthCheck() {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  // Method to generate embeddings (for future use)
  async generateEmbeddings(text) {
    try {
      const response = await fetch(`${this.baseUrl}/api/v1/embeddings`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error generating embeddings:', error);
      throw error;
    }
  }
}

export default new ApiService();