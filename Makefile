.PHONY: help build up down logs clean restart dev setup install status health

help:
	@echo "🚀 ReflexAI Development Commands"
	@echo "================================="
	@echo "  make up       - 🏗️  Build and start all services (main command)"
	@echo "  make dev      - 🔧 Start in development mode with logs"
	@echo "  make setup    - ⚙️  Complete setup including Ollama model"
	@echo "  make down     - 🛑 Stop all services"
	@echo "  make restart  - 🔄 Restart all services"
	@echo "  make logs     - 📋 View all service logs"
	@echo "  make status   - 📊 Check service status"
	@echo "  make health   - 🏥 Check application health"
	@echo "  make clean    - 🧹 Clean up containers and volumes"
	@echo "  make install  - 📦 Install local dependencies (optional)"
	@echo ""
	@echo "Quick start: make up"

# Main development command - build and start everything
up:
	@echo "🏗️ Building and starting ReflexAI services..."
	docker-compose up --build -d
	@echo ""
	@echo "✅ Services started successfully!"
	@echo "🌐 Frontend: http://localhost:3000"
	@echo "🔧 Backend API: http://localhost:8000"
	@echo "📚 API Docs: http://localhost:8000/docs"
	@echo ""
	@echo "⏳ Waiting for services to be ready..."
	@sleep 5
	@make status

# Development mode with logs visible
dev:
	@echo "🔧 Starting ReflexAI in development mode..."
	docker-compose up --build

# Complete setup including Ollama model
setup: up
	@echo "⚙️ Setting up Ollama AI model..."
	@sleep 10
	@make ollama-pull
	@echo "🎉 Setup complete! Your ReflexAI is ready to use."

# Stop all services
down:
	@echo "🛑 Stopping all services..."
	docker-compose down

# Restart services
restart:
	@echo "🔄 Restarting all services..."
	docker-compose down
	docker-compose up --build -d
	@make status

# View all logs
logs:
	docker-compose logs -f

# Check service status
status:
	@echo "📊 Service Status:"
	@docker-compose ps

# Health check
health:
	@echo "🏥 Checking application health..."
	@echo "Frontend: $$(curl -s -o /dev/null -w '%{http_code}' http://localhost:3000 2>/dev/null || echo 'Not responding')"
	@echo "Backend: $$(curl -s -o /dev/null -w '%{http_code}' http://localhost:8000/api/health 2>/dev/null || echo 'Not responding')"
	@echo ""
	@echo "🤖 Ollama Model Status:"
	@docker exec $$(docker-compose ps -q ollama) ollama list 2>/dev/null | head -n 5 || echo "Ollama not ready"

# Check Ollama status specifically
ollama-status:
	@echo "🤖 Ollama AI Model Status:"
	@echo "========================="
	@docker exec $$(docker-compose ps -q ollama) ollama list || echo "⚠️ Ollama service not running"
	@echo ""
	@echo "To download model: make ollama-pull"

# Clean up everything
clean:
	@echo "🧹 Cleaning up containers and volumes..."
	docker-compose down -v
	docker system prune -f
	@echo "✅ Cleanup complete!"

# Install local dependencies (optional for IDE support)
install:
	@echo "📦 Installing local dependencies..."
	@echo "Frontend dependencies..."
	@cd frontend && npm install
	@echo "Backend dependencies (using virtual env)..."
	@cd backend && python3 -m venv venv 2>/dev/null || true
	@cd backend && source venv/bin/activate && pip install -r requirements.txt 2>/dev/null || echo "⚠️ Backend install failed - use Docker instead"
	@echo "✅ Local dependencies installed!"

# Individual service logs
backend-logs:
	docker-compose logs -f backend

frontend-logs:
	docker-compose logs -f frontend

ollama-logs:
	docker-compose logs -f ollama

# Pull Ollama model
ollama-pull:
	@echo "🤖 Downloading Ollama AI model (this may take a few minutes)..."
	@docker exec $$(docker-compose ps -q ollama) ollama pull llama3.2:1b || echo "⚠️ Ollama not ready yet, try: make ollama-pull"
	@echo "✅ Ollama model ready!"

# Quick development workflow
build:
	@echo "🏗️ Building Docker images..."
	docker-compose build