#!/bin/bash

# Quick start script for local testing
# Usage: ./start-local.sh

set -e

echo "========================================="
echo "Starting paomi-as2 locally with Docker"
echo "========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "Error: docker-compose is not installed."
    exit 1
fi

# Stop any existing containers
echo "Stopping existing containers..."
docker-compose down

# Build and start containers
echo "Building Docker images..."
docker-compose build

echo "Starting containers..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 15

# Check status
echo ""
echo "Checking container status..."
docker-compose ps

# Show logs
echo ""
echo "Recent logs:"
docker-compose logs --tail=20

echo ""
echo "========================================="
echo "✓ Services started successfully!"
echo "========================================="
echo ""
echo "Access Points:"
echo "  - P1 Admin: http://localhost/admin/ (admin/admin123)"
echo "  - P2 Admin: http://localhost/p2/admin/ (admin/admin123)"
echo "  - P1 AS2: http://localhost/pyas2/as2receive"
echo "  - P2 AS2: http://localhost/p2/pyas2/as2receive"
echo ""
echo "Useful Commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop: docker-compose down"
echo "  - Restart: docker-compose restart"
echo ""
