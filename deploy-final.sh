#!/bin/bash
cd /home/dev
echo '=== Extracting package ==='
PACKAGE=$(ls -t as2-deploy-*.tar.gz | head -1)
mkdir -p paomi-as2-new
tar -xzf $PACKAGE -C paomi-as2-new

echo '=== Stopping existing containers ==='
cd paomi-as2 2>/dev/null && docker-compose down || true

echo '=== Backing up old deployment ==='
cd /home/dev
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mv paomi-as2 paomi-as2-backup-${TIMESTAMP} 2>/dev/null || true
mv paomi-as2-new paomi-as2

echo '=== Building containers ==='
cd /home/dev/paomi-as2
docker-compose build

echo '=== Starting containers ==='
docker-compose up -d

echo '=== Waiting for services ==='
sleep 30

echo '=== Container status ==='
docker-compose ps

echo '=== Checking logs ==='
docker-compose logs --tail=20

echo '=== Deployment complete ==='
echo 'Access at:'
echo '  Dashboard: http://192.168.1.200:3000'
echo '  P1 Admin:  http://192.168.1.200:8001/admin/'
echo '  P2 Admin:  http://192.168.1.200:8001/p2/admin/'
