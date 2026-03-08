Write-Host "1. Building image with tag 'latest'..." -ForegroundColor Yellow
docker build -t secure-notes-app:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "2. Forcing Kubernetes to reload 'latest'..." -ForegroundColor Yellow
# Strong way to "wake up"
kubectl rollout restart deployment notes-app-deployment

Write-Host "3. Waiting for deployment..." -ForegroundColor Yellow
kubectl rollout status deployment notes-app-deployment

Write-Host "Done! Go refresh the page." -ForegroundColor Green