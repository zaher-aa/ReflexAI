#!/bin/bash

# Start Ollama in background
ollama serve &

# Wait for Ollama to start
sleep 10

# Pull the model in background
(ollama pull llama3.2:1b &)

# Start supervisor to manage both services
exec /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf