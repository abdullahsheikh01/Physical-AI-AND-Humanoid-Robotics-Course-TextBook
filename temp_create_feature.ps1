$description = @"
Add Specs for the integration of RAG(Retrieval-Augmented-Generation) Chatbot which have following specs:

## Frontend:
- Chatbot Widget Component at the right bottom of website.
- Chatbot Widget Component should have pop-up and close functionality.
- Chatbot Widget Component should have clean and modern design which suits to website's theme.
- Pop Up Button of Chatbot Widget Component Should Visible as Ask me Button.

## Backend:
- Cohere for generating embeddings
- Qdrant as the vector database for retrieving relevant chunks
- Gemini 2.0 Flash model (via OpenAI-compatible API) for generating answers
- A custom Agent that must always retrieve context before answering, this Agent Should made by using [OpenAI Agents SDK Python](https://openai.github.io/openai-agents-python/).
- The agent should give answer in streaming using  `Runner.run_streamed` method of [OpenAI Agents SDK Python](https://openai.github.io/openai-agents-python/).

## Connectivity:
The Connectivity of Frontend and Backend Should done by [FastAPI]
"@

& ".specify/scripts/powershell/create-new-feature.ps1" -Json -Number 1 -ShortName "rag-chatbot-integration" -Description $description