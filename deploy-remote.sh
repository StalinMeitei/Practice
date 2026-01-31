#!/bin/bash
# Deploy AS2 Dashboard to Remote Server (192.168.1.200)
# Bash script for Linux/Mac or Git Bash on Windows

SERVER_IP="192.168.1.200"
USERNAME="dev"
REMOTE_DIR="/home/dev/paomi-as2"

echo "============================================================"
echo "  Deploy AS2 Dashboard to $SERVER_IP"
echo "============================================================"
echo ""

# Check if rsync is available
if ! command -v rsync &> /dev/null; then
    echo "⚠ rsync not found, using scp instead"
    USE_SCP=true
else
    USE_SCP=false
fi

# Step 1: Create deployment package
echo "[1/6] Creating deployment package..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
PACKAGE_NAME="as2-dashboard-${TIMESTAMP}.tar.gz"

tar -czf $PACKAGE_NAME \
    docker-compose.yml \
    Dockerfile \
    nginx.conf \
    init-db.sh \
    init_as2_config.py \
    init_pgedge_agentic.py \
    api_views.py \
    generate_certificates.py \
    P1/ \
    P2/ \
    frontend/ \
    *.pem 2>/dev/null || true

echo "  ✓ Package created: $PACKAGE_NAME"

# Step 2: Upload package
echo ""
echo "[2/6] Uploading package to server..."
scp -o StrictHostKeyChecking=no $PACKAGE_NAME ${USERNAME}@${SERVER_IP}:/home/dev/

if [ $? -eq 0 ]; then
    echo "  ✓ Package uploaded"
else
    echo "  ✗ Upload failed"
    exit 1
fi

# Step 3: Deploy on server
echo ""
echo "[3/6] Deploying on server..."

ssh -o StrictHostKeyChecking=no ${USERNAME}@${SERVER_IP} << 'ENDSSH'
cd /home/dev

# Extract package
PACKAGE=$(ls -t as2-dashboard-*.tar.gz | head -1)
echo "=== Extracting $PACKAGE ==="
mkdir -p paomi-as2-new
tar -xzf $PACKAGE -C paomi-as2-new

# Stop existing containers
echo "=== Stopping existing containers ==="
cd paomi-as2 2>/dev/null && docker-compose down || true

# Backup old deployment
echo "=== Backing up old deployment ==="
cd /home/dev
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mv paomi-as2 paomi-as2-backup-${TIMESTAMP} 2>/dev/null || true
mv paomi-as2-new paomi-as2

# Build and start containers
echo "=== Building containers ==="
cd /home/dev/paomi-as2
docker-compose build --no-cache

echo "=== Starting containers ==="
docker-compose up -d

# Wait for services
echo "=== Waiting for services to start ==="
sleep 15

# Check status
echo "=== Container status ==="
docker-compose ps

echo "=== Deployment complete ==="
ENDSSH

# Step 4: Verify deployment
echo ""
echo "[4/6] Verifying deployment..."
sleep 5

# Test endpoints
echo "  Testing Dashboard..."
curl -s -o /dev/null -w "  Dashboard: %{http_code}\n" http://${SERVER_IP}:3000 || echo "  Dashboard: Not accessible yet"

echo "  Testing P1 Admin..."
curl -s -o /dev/null -w "  P1 Admin: %{http_code}\n" http://${SERVER_IP}:8001/admin/ || echo "  P1 Admin: Not accessible yet"

echo "  Testing API..."
curl -s -o /dev/null -w "  API: %{http_code}\n" http://${SERVER_IP}:8001/api/stats/ || echo "  API: Not accessible yet"

# Step 5: Cleanup
echo ""
echo "[5/6] Cleaning up..."
rm -f $PACKAGE_NAME
echo "  ✓ Cleanup complete"

# Step 6: Display info
echo ""
echo "[6/6] Deployment summary"
echo ""
echo "============================================================"
echo "  Deployment Complete!"
echo "============================================================"
echo ""
echo "Access Points:"
echo "  Dashboard:    http://${SERVER_IP}:3000"
echo "  P1 Admin:     http://${SERVER_IP}:8001/admin/"
echo "  P2 Admin:     http://${SERVER_IP}:8001/p2/admin/"
echo "  API:          http://${SERVER_IP}:8001/api/"
echo ""
echo "Credentials:"
echo "  Admin:        admin / admin123"
echo "  Database:     postgres / postgres"
echo ""
echo "SSH Access:"
echo "  ssh ${USERNAME}@${SERVER_IP}"
echo ""
echo "Useful Commands (on server):"
echo "  cd /home/dev/paomi-as2"
echo "  docker-compose ps"
echo "  docker-compose logs -f"
echo "  docker-compose logs frontend -f"
echo "  docker-compose restart frontend"
echo ""
echo "============================================================"
echo ""
