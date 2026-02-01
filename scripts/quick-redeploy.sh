#!/bin/bash
cd /home/dev
PACKAGE=$(ls -t as2-deploy-*.tar.gz | head -1)
echo "Using package: $PACKAGE"
mkdir -p paomi-as2-new
tar -xzf $PACKAGE -C paomi-as2-new
cd paomi-as2 && docker-compose down
cd /home/dev
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mv paomi-as2 paomi-as2-backup-${TIMESTAMP}
mv paomi-as2-new paomi-as2
cd paomi-as2
docker-compose build
docker-compose up -d
sleep 25
docker-compose ps
echo "Deployment complete!"
echo "Dashboard: http://192.168.1.200:8001"
echo "Dashboard (direct): http://192.168.1.200:3000"
