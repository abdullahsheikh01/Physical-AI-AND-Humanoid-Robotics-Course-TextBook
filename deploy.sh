#!/bin/bash

# Deployment script for RAG Chatbot Integration

set -e  # Exit on any error

echo "Starting RAG Chatbot deployment..."

# Backend deployment
echo "Deploying backend..."
cd backend

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run any necessary database migrations or setup
echo "Initializing vector database..."
python -c "from src.services.vector_db_service import vector_db_service; vector_db_service.initialize_collection()"

# Frontend deployment
echo "Deploying frontend..."
cd ../website

# Install dependencies
npm install

# Build the frontend
npm run build

echo "Deployment completed successfully!"
echo "To start the services:"
echo "1. Start backend: cd backend && uvicorn src.main:app --host 0.0.0.0 --port 8000"
echo "2. Serve frontend: cd website && npx serve -s build -l 3000"