#!/bin/bash

# Deployment script for paomi-as2 to remote server
# Usage: ./deploy.sh

set -e

# Configuration
REMOTE_HOST="192.168.1.200"
REMOTE_USER="dev"
REMOTE_PASSWORD="dev@2025"
REMOTE_DIR="/home/dev/paomi-as2"
PROJECT_NAME="paomi-as2"

echo "========================================="
echo "Deploying $PROJECT_NAME to $REMOTE_HOST"
echo "========================================="

# Create deployment package
echo "Creating deployment package..."
tar -czf ${PROJECT_NAME}.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='*.sqlite3' \
    --exclude='venv' \
    --exclude='*.log' \
    .

echo "Package created: ${PROJECT_NAME}.tar.gz"

# Copy to remote server using sshpass
echo "Copying files to remote server..."
sshpass -p "$REMOTE_PASSWORD" scp ${PROJECT_NAME}.tar.gz ${REMOTE_USER}@${REMOTE_HOST}:/tmp/

# Execute deployment on remote server
echo "Executing deployment on remote server..."
sshpass -p "$REMOTE_PASSWORD" ssh ${REMOTE_USER}@${REMOTE_HOST} << 'ENDSSH'
set -e

# Navigate to deployment directory
mkdir -p /home/dev/paomi-as2
cd /home/dev/paomi-as2

# Backup existing deployment if it exists
if [ -d "P1" ] || [ -d "P2" ]; then
    echo "Backing up existing deployment..."
    BACKUP_DIR="/home/dev/paomi-as2-backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p $BACKUP_DIR
    cp -r * $BACKUP_DIR/ 2>/dev/null || true
    echo "Backup created at: $BACKUP_DIR"
fi

# Extract new deployment
echo "Extracting deployment package..."
tar -xzf /tmp/paomi-as2.tar.gz -C /home/dev/paomi-as2/
rm /tmp/paomi-as2.tar.gz

# Stop existing containers
echo "Stopping existing containers..."
docker-compose down || true

# Build and start containers
echo "Building Docker images..."
docker-compose build

echo "Starting containers..."
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 10

# Check container status
echo "Checking container status..."
docker-compose ps

# Create superuser for P1 (if needed)
echo "Setting up P1 admin user..."
docker-compose exec -T p1 python manage.py shell << 'ENDPYTHON'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@p1.com', 'admin123')
    print("P1 admin user created")
else:
    print("P1 admin user already exists")
ENDPYTHON

# Create superuser for P2 (if needed)
echo "Setting up P2 admin user..."
docker-compose exec -T p2 python manage.py shell << 'ENDPYTHON'
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@p2.com', 'admin123')
    print("P2 admin user created")
else:
    print("P2 admin user already exists")
ENDPYTHON

echo "Deployment completed successfully!"
echo ""
echo "Access points:"
echo "  - P1 Admin: http://192.168.1.200/admin/ (admin/admin123)"
echo "  - P2 Admin: http://192.168.1.200/p2/admin/ (admin/admin123)"
echo "  - P1 AS2 Endpoint: http://192.168.1.200/pyas2/as2receive"
echo "  - P2 AS2 Endpoint: http://192.168.1.200/p2/pyas2/as2receive"
echo ""
echo "To view logs: docker-compose logs -f"
echo "To stop: docker-compose down"
ENDSSH

# Cleanup local package
rm ${PROJECT_NAME}.tar.gz

echo ""
echo "========================================="
echo "Deployment completed successfully!"
echo "========================================="
echo ""
echo "Access your application at:"
echo "  - http://192.168.1.200/"
echo "  - P1 Admin: http://192.168.1.200/admin/"
echo "  - P2 Admin: http://192.168.1.200/p2/admin/"
