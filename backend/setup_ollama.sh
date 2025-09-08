#!/bin/bash
echo "Setting up Ollama with Llama 3.1 model..."

# Wait for Ollama to be ready
sleep 5

# Pull the model
docker exec reflexai-ollama ollama pull llama3.2:1b

echo "Ollama setup complete!"