# Portainer Deployment Guide for MLB API Proxy

## Prerequisites
1. Docker image `mlb-api-proxy:1.2026.10` loaded on the target server
2. Portainer installed and accessible
3. Access to Portainer with stack creation permissions

## Deployment Steps

### Method 1: Using Portainer UI (Recommended)

1. **Load the Docker Image** (on target server):
   ```bash
   docker load -i mlb-api-proxy-1.2026.10.tar
   ```

2. **Verify Image**:
   ```bash
   docker images mlb-api-proxy:1.2026.10
   ```

3. **Access Portainer**:
   - Navigate to your Portainer instance (e.g., `http://your-server:9000`)
   - Login with your credentials

4. **Create Stack**:
   - Go to **Stacks** > **Add stack**
   - Name: `mlb-api-proxy`
   - Build method: Choose **Upload**
   - Upload the `docker-compose.yml` file

5. **Configure Environment Variables**:
   Click on **Environment variables** and add:
   ```
   IMAGE_VERSION=1.2026.10
   EXTERNAL_PORT=8000
   PROXY_API_KEY=your-secure-api-key-here
   MLB_BASE_URL=https://statsapi.mlb.com
   LOG_LEVEL=INFO
   WORKERS=4
   UPSTREAM_TIMEOUT_SECONDS=30.0
   ```

6. **Deploy**:
   - Click **Deploy the stack**
   - Wait for deployment to complete

7. **Verify Deployment**:
   - Go to **Containers** tab
   - Look for `mlb-api-proxy` container
   - Status should be "healthy" (green)

### Method 2: Using Repository (Git)

If your code is in a Git repository:

1. **Create Stack from Git Repository**:
   - Go to **Stacks** > **Add stack**
   - Name: `mlb-api-proxy`
   - Build method: **Repository**
   - Repository URL: Your Git URL
   - Repository reference: `main` or your branch
   - Compose path: `docker-compose.yml`

2. **Configure the same environment variables as Method 1**

3. **Deploy the stack**

## Post-Deployment Verification

### 1. Check Container Health
```bash
docker ps --filter name=mlb-api-proxy
```
Should show status "healthy"

### 2. Test Health Endpoint
```bash
curl http://localhost:8000/health
```
Expected response:
```json
{"status":"healthy","version":"1.2026.10","proxy":"ok","upstream":"ok"}
```

### 3. Check Logs in Portainer
- Go to **Containers** > `mlb-api-proxy` > **Logs**
- Should see: "Started server process" for 4 workers
- No error messages

## Updating the Deployment

### Update to New Version

1. Load new image on server:
   ```bash
   docker load -i mlb-api-proxy-1.2026.2.tar
   ```

2. In Portainer:
   - Go to **Stacks** > `mlb-api-proxy`
   - Click **Editor**
   - Update `IMAGE_VERSION` environment variable to new version
   - Click **Update the stack**
   - Enable **Re-pull image and redeploy**
   - Click **Update**

### Update Configuration Only

1. In Portainer:
   - Go to **Stacks** > `mlb-api-proxy`
   - Click **Editor**
   - Modify environment variables as needed
   - Click **Update the stack**

## Troubleshooting

### Container Won't Start
- Check logs in Portainer
- Verify `PROXY_API_KEY` is set
- Ensure port 8000 is not already in use

### Health Check Failing
- Check if MLB API is accessible: `curl https://statsapi.mlb.com/api/v1/sports`
- Verify network connectivity
- Check container logs for errors

### Performance Issues
- Increase `WORKERS` based on CPU cores (formula: 2 x cores + 1)
- Adjust resource limits in docker-compose.yml
- Monitor CPU/Memory usage in Portainer

## Security Best Practices

1. **Strong API Key**: Use a long, random string for `PROXY_API_KEY`
2. **Secrets Management**: Consider using Docker secrets or Portainer secrets
3. **Network Isolation**: Keep in isolated network if possible
4. **Reverse Proxy**: Use nginx/traefik with SSL for production
5. **Regular Updates**: Keep the image updated with latest security patches

## Monitoring

### In Portainer
- **Dashboard**: View resource usage
- **Containers**: Check health status
- **Logs**: Monitor application logs
- **Stats**: CPU/Memory graphs

### External Monitoring
Setup health check monitoring:
```bash
*/5 * * * * curl -f http://your-server:8000/health || echo "MLB API Proxy Down"
```

## Support

For issues or questions:
- Check container logs first
- Verify environment variables are set correctly
- Ensure Docker image is properly loaded
- Test health endpoint directly
