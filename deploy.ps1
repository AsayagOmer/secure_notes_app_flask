Write-Host "Starting Build and Deploy Process..." -ForegroundColor Cyan

Write-Host "Building Docker image (secure-notes-app:dev)..." -ForegroundColor Yellow
docker build -t secure-notes-app:dev .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed! Check your code and try again." -ForegroundColor Red
    exit 1
}

Write-Host "Restarting Kubernetes deployment..." -ForegroundColor Yellow
kubectl rollout restart deployment notes-app-deployment

Write-Host "Waiting for new pods to be ready..." -ForegroundColor Yellow
kubectl rollout status deployment notes-app-deployment

Write-Host "Deployment Successful! Your app is updated." -ForegroundColor Green
kubectl get pods