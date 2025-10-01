#!/bin/bash

# OpenAI Agents with Opik - Quick Setup Script
echo "ðŸš€ Setting up OpenAI Agents with Opik Tracing..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "âŒ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env exists
if [ ! -f .env ]; then
    echo "ðŸ“‹ Creating .env file from template..."
    cp .env.example .env
    echo "âš ï¸  Please edit .env file with your Azure OpenAI credentials"
    echo "   Required: AZURE_OPENAI_KEY, AZURE_OPENAI_ENDPOINT, AZURE_DEPLOYMENT_NAME"
fi

# Build and start services
echo "ðŸ—ï¸  Building and starting services..."
docker-compose up --build -d

# Wait for services to be ready
echo "â³ Waiting for services to start..."
sleep 30

# Check service status
echo "ðŸ” Checking service status..."
docker-compose ps

echo ""
echo "âœ… Setup complete!"
echo ""
echo "ðŸŒ Access your application:"
echo "   App:   http://localhost:8501"
echo "   Opik:  http://localhost:5173"
echo ""
echo "ðŸ“‹ Next steps:"
echo "   1. Edit .env file with your Azure OpenAI credentials"
echo "   2. Restart services: docker-compose restart openai-agents-app"
echo "   3. Open http://localhost:8501 in your browser"
echo ""
echo "ðŸ›‘ To stop: docker-compose down"