#!/bin/bash

# Script to import MLB API Proxy Docker image tar file and prepare for Portainer deployment

set -e  # Exit on error

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Prompt the user for the version
read -p "Enter the version of the mlb-api-proxy image to deploy (e.g., 1.2026.1): " VERSION

# Validate that version was provided
if [ -z "$VERSION" ]; then
    echo "Error: Version cannot be empty. Please provide a version."
    exit 1
fi

# Set the tar file path in docker_images folder (relative to script location)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAR_FILE="$SCRIPT_DIR/docker_images/mlb-api-proxy-$VERSION.tar"

# Validate that the tar file exists
if [ ! -f "$TAR_FILE" ]; then
    echo "Error: Tar file not found at $TAR_FILE"
    echo "Please ensure the image file is located in docker_images/ folder"
    echo ""
    echo "Expected file: mlb-api-proxy-$VERSION.tar"
    exit 1
fi

echo ""
echo "======================================"
echo "MLB API Proxy Docker Image Deployment"
echo "======================================"
echo "Loading image: $TAR_FILE"
echo "File size: $(du -h "$TAR_FILE" | cut -f1)"
echo ""

# Load the image into Docker
if docker load -i "$TAR_FILE"; then
    echo ""
    echo "======================================"
    echo "SUCCESS! Image Loaded"
    echo "======================================"
    
    # Verify the image was loaded
    if docker images mlb-api-proxy:$VERSION --format "{{.Repository}}:{{.Tag}}" | grep -q "mlb-api-proxy:$VERSION"; then
        echo "✓ Verified: mlb-api-proxy:$VERSION"
        echo ""
        echo "Image details:"
        docker images mlb-api-proxy:$VERSION --format "  Size: {{.Size}}\n  Created: {{.CreatedSince}}"
        echo ""
    fi
    
    echo "======================================"
    echo "Deployment Options:"
    echo "======================================"
    echo ""
    echo "1. Direct Docker run:"
    echo "   docker run -d -p 8000:8000 \\"
    echo "     --name mlb-api-proxy \\"
    echo "     --restart unless-stopped \\"
    echo "     -e PROXY_API_KEY=your-api-key \\"
    echo "     -e MLB_BASE_URL=https://statsapi.mlb.com \\"
    echo "     -e LOG_LEVEL=INFO \\"
    echo "     -e WORKERS=4 \\"
    echo "     -e UPSTREAM_TIMEOUT_SECONDS=30.0 \\"
    echo "     mlb-api-proxy:$VERSION"
    echo ""
    echo "2. Using Docker Compose:"
    echo "   docker-compose up -d"
    echo ""
    echo "3. Using Portainer:"
    echo "   - Go to Portainer Images"
    echo "   - Verify mlb-api-proxy:$VERSION is listed"
    echo "   - Create new Stack from docker-compose.yml"
    echo "   - Set environment variables in Portainer"
    echo ""
    echo "======================================"
    echo "Health check endpoint: http://localhost:8000/health"
    echo "======================================"
else
    echo ""
    echo "Error: Failed to load Docker image from tar file"
    exit 1
fi
