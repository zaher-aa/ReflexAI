# ReflexAI - Advanced Text Analysis Tool

A comprehensive, privacy-focused text analysis platform that provides deep insights into writing style, linguistic patterns, and content themes using advanced NLP techniques. Perfect for writers, researchers, and content analysts who want professional-grade text analysis without compromising data privacy.

## ✨ Key Features

### 📊 **Advanced Keyness Analysis**
- **Enhanced Keyness Chart**: Interactive D3.js visualization showing both positive and negative keyness
- **Effect Size Visualization**: Horizontal bar chart displaying words that are over/under-represented compared to reference corpus
- **Statistical Significance**: Log-likelihood calculations with confidence metrics
- **Color-coded Results**: Blue bars for positive keyness, red bars for negative keyness

### 🎯 **Interactive Semantic Clustering**
- **Dynamic Cluster Visualization**: Interactive scatter plots with Plotly.js
- **Multiple Clustering Algorithms**: K-means clustering with optimized cluster count
- **Word Relationship Mapping**: Visualize semantic relationships between terms
- **Cluster Statistics**: Detailed metrics for each semantic group

### 💭 **Comprehensive Sentiment Analysis** 
- **Multi-dimensional Analysis**: Overall sentiment scoring with positive/negative/neutral breakdown
- **Visual Sentiment Display**: Pie charts and donut charts showing sentiment distribution
- **Confidence Scoring**: Reliability metrics for sentiment predictions

### 📈 **Detailed Text Statistics**
- **Comprehensive Metrics**: Word count, sentence count, average sentence length
- **Readability Analysis**: Multiple readability scores and complexity metrics  
- **Vocabulary Analysis**: Type-token ratio, lexical diversity measures

### 🔒 **Privacy-First Architecture**
- **Zero Data Retention**: All text deleted immediately after analysis
- **Local Processing**: Core analysis runs locally without external API calls
- **Optional AI Integration**: Ollama integration for enhanced insights (fully local)

### 📊 **Professional Export Options**
- **Multi-format Export**: JSON, PNG, PDF export capabilities
- **Print-ready Charts**: High-quality visualizations for reports
- **Complete Analysis Package**: Export all results with charts and statistics

### 🎨 **Modern User Experience**
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Interactive Visualizations**: Hover tooltips, zoom, pan functionality
- **Real-time Analysis**: Fast processing with progress indicators
- **Clean UI**: Modern interface built with Tailwind CSS

## 🛠️ Technology Stack

### Frontend
- **React 18** with TypeScript for type-safe development
- **D3.js** for advanced custom visualizations  
- **Plotly.js** for interactive scientific charts
- **Chart.js** with react-chartjs-2 for standard charts
- **Tailwind CSS** for responsive styling
- **React Dropzone** for file upload handling
- **Vite** for fast development and building
- **HTML2Canvas & jsPDF** for export functionality

### Backend
- **FastAPI** for high-performance async API
- **Advanced NLP Stack**:
  - **NLTK** for natural language processing
  - **spaCy** for advanced linguistic analysis  
  - **scikit-learn** for machine learning and clustering
  - **Gensim** for topic modeling and word embeddings
  - **TextBlob** for sentiment analysis
- **Data Processing**:
  - **NumPy** & **Pandas** for numerical computing
  - **Matplotlib** & **Seaborn** for data visualization
- **Optional AI Integration**:
  - **Ollama** for local AI model integration
  - **HTTPX** for async HTTP requests

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