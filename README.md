# Sample HTML App with Kubernetes

A simple HTML application deployed on Kubernetes using Kind cluster and Argo CD.

## Project Structure

```
.
├── index.html          # Main HTML file
├── server.js           # Node.js server
├── package.json        # Node.js dependencies
├── Dockerfile          # Container image definition
├── k8s-deployment.yaml # Kubernetes manifests
├── kind-config.yaml    # Kind cluster configuration
└── argocd-app.yaml     # Argo CD application manifest
```

## Prerequisites

- Node.js
- Docker
- Kind (Kubernetes in Docker)
- kubectl
- Argo CD

## Local Development

1. Install dependencies:
   ```bash
   npm install
   ```

2. Run locally:
   ```bash
   npm start
   ```

## Kubernetes Deployment

1. Create Kind cluster:
   ```bash
   kind create cluster --config kind-config.yaml
   ```

2. Build and load Docker image:
   ```bash
   docker build -t sample-app:latest .
   kind load docker-image sample-app:latest
   ```

3. Deploy to Kubernetes:
   ```bash
   kubectl apply -f k8s-deployment.yaml
   ```

4. Access the application:
   ```
   http://localhost:30080
   ```

## Argo CD Integration

1. Apply the Argo CD application manifest:
   ```bash
   kubectl apply -f argocd-app.yaml
   ```

2. Check application status:
   ```bash
   python check_argo_status.py
   ```

## Environment Variables

For Argo CD status check script:
- ARGOCD_SERVER
- ARGOCD_USERNAME
- ARGOCD_PASSWORD
- ARGOCD_APP_NAME (optional, defaults to 'sample-html-app') 