.PHONY: help build up down logs clean restart

help:
	@echo "Available commands:"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start all services"
	@echo "  make down     - Stop all services"
	@echo "  make logs     - View logs"
	@echo "  make clean    - Clean up containers and volumes"
	@echo "  make restart  - Restart all services"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Application is running!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	docker-compose down -v
	docker system prune -f

restart:
	docker-compose down
	docker-compose up -d

backend-logs:
	docker-compose logs -f backend

frontend-logs:
	docker-compose logs -f frontend

ollama-pull:
	docker exec -it $$(docker-compose ps -q ollama) ollama pull llama3.1