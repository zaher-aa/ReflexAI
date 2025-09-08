# ReflexAI (Text Analysis Tool for Creative Writers)

A privacy-focused text analysis tool that helps creative writers discover insights about their writing style, themes, and patterns without sharing their work with commercial AI models.

## Features

- 📊 **Keyness Analysis**: Identify the most distinctive words in your text
- 🎯 **Semantic Clustering**: Discover thematic patterns and word groups
- 💭 **Sentiment Analysis**: Understand emotional tones in your writing
- 🔒 **Privacy First**: Text is deleted immediately after analysis
- 📥 **Export Results**: Download your analysis as JSON
- 🎨 **Modern UI**: Clean, responsive interface with visualizations

## Tech Stack

### Frontend
- React 18 with TypeScript
- Tailwind CSS for styling
- Chart.js for data visualization
- React Dropzone for file uploads
- Vite for fast development

### Backend
- FastAPI (Python)
- NLTK for natural language processing
- scikit-learn for clustering
- TextBlob for sentiment analysis
- Optional: Ollama for AI insights

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Make (for easy commands)

### 🚀 One-Command Setup

```bash
# Start everything with one command:
make up

# For first-time setup (includes AI model):
make setup
```

### 📋 Available Commands

```bash
make up       # 🏗️  Build and start all services (main command)
make dev      # 🔧 Start in development mode with logs
make setup    # ⚙️  Complete setup including Ollama model  
make down     # 🛑 Stop all services
make restart  # 🔄 Restart all services
make logs     # 📋 View all service logs
make status   # 📊 Check service status
make health   # 🏥 Check application health
make clean    # 🧹 Clean up containers and volumes
```

### 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health