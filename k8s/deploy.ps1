$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

function Assert-Success {
    param([string]$Message)
    if ($LASTEXITCODE -ne 0) {
        throw $Message
    }
}

function Invoke-Migration {
    param(
        [string]$Service,
        [string]$Image,
        [string]$Database
    )

    $pod = "$Service-migrate"
    kubectl delete pod $pod -n tankworld --ignore-not-found | Out-Null
    kubectl run $pod `
        -n tankworld `
        --image="${Image}:latest" `
        --image-pull-policy=Never `
        --restart=Never `
        --env="DB_HOST=postgres" `
        --env="DB_PORT=5432" `
        --env="DB_NAME=$Database" `
        --env="DB_USER=tankworld" `
        --env="DB_PASSWORD=tankworld-password" `
        --command -- python manage.py migrate
    Assert-Success "Could not create the migration pod for $Service."

    for ($attempt = 0; $attempt -lt 90; $attempt++) {
        $phase = kubectl get pod $pod -n tankworld -o jsonpath='{.status.phase}' 2>$null
        if ($phase -eq "Succeeded") {
            kubectl logs $pod -n tankworld
            return
        }
        if ($phase -eq "Failed") {
            kubectl logs $pod -n tankworld
            throw "$Service migration failed."
        }
        Start-Sleep -Seconds 2
    }
    kubectl logs $pod -n tankworld
    throw "$Service migration timed out."
}

kubectl apply -f "$PSScriptRoot/00-namespace.yaml"
kubectl apply -f "$PSScriptRoot/01-postgres.yaml"
kubectl rollout status deployment/postgres -n tankworld --timeout=180s
Assert-Success "PostgreSQL did not become ready."

Invoke-Migration "catalog" "tankworld-catalog" "catalog_db"
Invoke-Migration "community" "tankworld-community" "community_db"
Invoke-Migration "battle" "tankworld-battle" "battle_db"

kubectl apply -f "$PSScriptRoot/10-catalog.yaml"
kubectl apply -f "$PSScriptRoot/11-community.yaml"
kubectl apply -f "$PSScriptRoot/12-battle.yaml"
kubectl apply -f "$PSScriptRoot/20-frontend.yaml"

foreach ($deployment in @("catalog-service", "community-service", "battle-service", "frontend")) {
    kubectl rollout restart "deployment/$deployment" -n tankworld
    Assert-Success "Could not restart $deployment."
}

foreach ($deployment in @("catalog-service", "community-service", "battle-service", "frontend")) {
    kubectl rollout status "deployment/$deployment" -n tankworld --timeout=180s
    Assert-Success "$deployment did not become ready."
}

kubectl get pods -n tankworld
kubectl get services -n tankworld
Write-Host "TankWorld is available at http://localhost:30080" -ForegroundColor Green