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
- Node.js 18+
- Python 3.9+
- npm or yarn

### Installation

1. Clone the repository:
```bash
git clone [repo]
cd ReflexAI

# Build everything
make build

# Start the application
make up

# View logs if needed
make logs