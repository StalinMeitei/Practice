#!/bin/bash

# Simple deployment script using SSH config
# Usage: ./deploy-simple.sh

set -e

REMOTE_HOST="dev_192168_rsa"  # Using SSH config alias
REMOTE_DIR="/home/dev/paomi-as2"
PROJECT_NAME="paomi-as2"

echo "========================================="
echo "Deploying $PROJECT_NAME"
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

echo "Copying to server..."
scp ${PROJECT_NAME}.tar.gz ${REMOTE_HOST}:/tmp/

echo "Deploying on server..."
ssh ${REMOTE_HOST} << 'ENDSSH'
set -e
cd /home/dev
mkdir -p paomi-as2
cd paomi-as2

# Backup if exists
if [ -d "P1" ]; then
    echo "Creating backup..."
    BACKUP_DIR="../paomi-as2-backup-$(date +%Y%m%d-%H%M%S)"
    mkdir -p $BACKUP_DIR
    cp -r * $BACKUP_DIR/ 2>/dev/null || true
fi

# Extract
tar -xzf /tmp/paomi-as2.tar.gz
rm /tmp/paomi-as2.tar.gz

# Deploy with Docker
docker-compose down || true
docker-compose build
docker-compose up -d

sleep 10
docker-compose ps

echo ""
echo "Deployment complete!"
echo "Access: http://192.168.1.200/"
ENDSSH

rm ${PROJECT_NAME}.tar.gz
echo "Done!"
