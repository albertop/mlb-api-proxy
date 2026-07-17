#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Build and save MLB API Proxy Docker image
.DESCRIPTION
    This script builds the MLB API Proxy Docker image with a specified version
    and saves it as a tar file in the docker_images folder.
.EXAMPLE
    .\build_and_save_image.ps1
#>

# Script configuration
$ErrorActionPreference = "Stop"
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR
$DOCKER_IMAGES_DIR = Join-Path $PROJECT_ROOT "docker_images"

# Display header
Write-Host "`n======================================"
Write-Host "MLB API Proxy Image Builder"
Write-Host "======================================"

# Ask user to confirm Docker Desktop is running
Write-Host "`n[REQUIRED] Please ensure Docker Desktop is running before continuing."
$dockerConfirm = Read-Host "Is Docker Desktop running? (y/n)"

if ($dockerConfirm -ne 'y') {
    Write-Host "`n[INFO] Please start Docker Desktop and run this script again.`n" -ForegroundColor Yellow
    exit 0
}

# Verify Docker is actually running
Write-Host "`n[INFO] Checking Docker status..." -ForegroundColor Cyan
try {
    docker info | Out-Null
    Write-Host "[SUCCESS] Docker is running and accessible!`n" -ForegroundColor Green
} catch {
    Write-Host "`n[ERROR] Docker is not running or not accessible.`n" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again.`n"
    exit 1
}

# Prompt for version
$VERSION = Read-Host "`nEnter the version for mlb-api-proxy image (e.g., 1.2026.1)"

# Validate version input
if ([string]::IsNullOrWhiteSpace($VERSION)) {
    Write-Host "`n[ERROR] Version cannot be empty. Please provide a version.`n" -ForegroundColor Red
    exit 1
}

# Validate version format (basic check)
if ($VERSION -notmatch '^\d+\.\d+\.\d+$') {
    Write-Host "`n[WARNING] Version format should be X.Y.Z (e.g., 1.2026.1)" -ForegroundColor Yellow
    $continue = Read-Host "Continue anyway? (y/n)"
    if ($continue -ne 'y') {
        Write-Host "`nBuild cancelled.`n"
        exit 0
    }
}

$IMAGE_NAME = "mlb-api-proxy"
$IMAGE_TAG = "${IMAGE_NAME}:${VERSION}"
$TAR_FILE = Join-Path $DOCKER_IMAGES_DIR "${IMAGE_NAME}-${VERSION}.tar"
$DOCKERFILE = Join-Path $PROJECT_ROOT "api-service\Dockerfile"

Write-Host "`n======================================"
Write-Host "Build Configuration"
Write-Host "======================================"
Write-Host "Image Name:      $IMAGE_NAME"
Write-Host "Version:         $VERSION"
Write-Host "Full Tag:        $IMAGE_TAG"
Write-Host "Dockerfile:      $DOCKERFILE"
Write-Host "Output File:     $TAR_FILE"
Write-Host "======================================`n"

# Confirm build
$confirm = Read-Host "Proceed with build? (y/n)"
if ($confirm -ne 'y') {
    Write-Host "`nBuild cancelled.`n"
    exit 0
}

# Create docker_images directory if it doesn't exist
if (-not (Test-Path $DOCKER_IMAGES_DIR)) {
    Write-Host "[INFO] Creating docker_images directory..." -ForegroundColor Cyan
    New-Item -ItemType Directory -Path $DOCKER_IMAGES_DIR | Out-Null
}

# Build Docker image
Write-Host "`n======================================"
Write-Host "Step 1: Building Docker Image"
Write-Host "======================================`n"

try {
    # Change to project root for build context
    Push-Location $PROJECT_ROOT
    
    $buildArgs = @(
        "build",
        "-t", $IMAGE_TAG,
        "-f", $DOCKERFILE,
        "--build-arg", "APP_VERSION=$VERSION",
        "."
    )
    
    Write-Host "[INFO] Running: docker $($buildArgs -join ' ')`n" -ForegroundColor Cyan
    Write-Host "[INFO] Build context: $PROJECT_ROOT`n" -ForegroundColor Cyan
    
    & docker $buildArgs
    
    Pop-Location
    
    if ($LASTEXITCODE -ne 0) {
        throw "Docker build failed with exit code $LASTEXITCODE"
    }
    
    Write-Host "`n[SUCCESS] Docker image built successfully!`n" -ForegroundColor Green
    
} catch {
    Pop-Location
    Write-Host "`n[ERROR] Failed to build Docker image: $_`n" -ForegroundColor Red
    exit 1
}

# Verify image exists
Write-Host "======================================"
Write-Host "Step 2: Verifying Image"
Write-Host "======================================`n"

$imageCheck = docker images $IMAGE_TAG --format "{{.Repository}}:{{.Tag}}"
if ($imageCheck -eq $IMAGE_TAG) {
    Write-Host "[SUCCESS] Image verified: $IMAGE_TAG`n" -ForegroundColor Green
    
    # Display image details
    Write-Host "Image Details:"
    docker images $IMAGE_TAG --format "  Repository: {{.Repository}}`n  Tag:        {{.Tag}}`n  Size:       {{.Size}}`n  Created:    {{.CreatedSince}}"
    
} else {
    Write-Host "`n[ERROR] Image verification failed. Image not found.`n" -ForegroundColor Red
    exit 1
}

# Save Docker image to tar file
Write-Host "`n======================================"
Write-Host "Step 3: Saving Image to Tar File"
Write-Host "======================================`n"

try {
    Write-Host "[INFO] Saving image to: $TAR_FILE" -ForegroundColor Cyan
    Write-Host "[INFO] This may take a few moments...`n" -ForegroundColor Cyan
    
    docker save -o $TAR_FILE $IMAGE_TAG
    
    if ($LASTEXITCODE -ne 0) {
        throw "Docker save failed with exit code $LASTEXITCODE"
    }
    
    Write-Host "[SUCCESS] Image saved successfully!`n" -ForegroundColor Green
    
} catch {
    Write-Host "`n[ERROR] Failed to save Docker image: $_`n" -ForegroundColor Red
    exit 1
}

# Display tar file details
if (Test-Path $TAR_FILE) {
    $fileInfo = Get-Item $TAR_FILE
    $fileSizeMB = [math]::Round($fileInfo.Length / 1MB, 2)
    
    Write-Host "======================================"
    Write-Host "Build Complete!"
    Write-Host "======================================"
    Write-Host "Image Tag:       $IMAGE_TAG"
    Write-Host "Tar File:        $TAR_FILE"
    Write-Host "File Size:       $fileSizeMB MB"
    Write-Host "Created:         $($fileInfo.LastWriteTime)"
    Write-Host "======================================`n"
    
    Write-Host "[INFO] Deployment Options:" -ForegroundColor Cyan
    Write-Host "  1. Load image on another host:"
    Write-Host "     docker load -i $TAR_FILE`n"
    Write-Host "  2. Deploy with Docker Compose:"
    Write-Host "     Update IMAGE_VERSION=$VERSION in Portainer env vars"
    Write-Host "     docker-compose up -d`n"
    Write-Host "  3. Run directly:"
    Write-Host "     docker run -d -p 3002:8000 --name mlb-api-proxy \"
    Write-Host "       -e PROXY_API_KEY=your-key \"
    Write-Host "       -e WORKERS=4 \"
    Write-Host "       $IMAGE_TAG`n"
    
    Write-Host "[SUCCESS] All tasks completed successfully!`n" -ForegroundColor Green
    
} else {
    Write-Host "`n[ERROR] Tar file was not created: $TAR_FILE`n" -ForegroundColor Red
    exit 1
}
