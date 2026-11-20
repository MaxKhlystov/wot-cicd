pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\maksi\\AppData\\Local\\Programs\\Python\\Python313\\python.exe'
        KUBECONFIG = 'C:\\Users\\maksi\\.kube\\config'
    }

    options {
        skipDefaultCheckout(true)
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                bat 'echo Branch: %BRANCH_NAME%'
            }
        }

        stage('Install test dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install -r services\\catalog\\requirements.txt'
                bat '"%PYTHON%" -m pip install -r services\\community\\requirements.txt'
                bat '"%PYTHON%" -m pip install -r services\\battle\\requirements.txt'
                bat 'cd client && npm ci'
            }
        }

        stage('Test source before build') {
            steps {
                bat 'cd services\\catalog && "%PYTHON%" -m pytest -q'
                bat 'cd services\\community && "%PYTHON%" -m pytest -q'
                bat 'cd services\\battle && "%PYTHON%" -m pytest -q'
                bat 'cd client && npm run build'
            }
        }

        stage('Build Docker images') {
            steps {
                bat 'docker build -t tankworld-catalog:latest services\\catalog'
                bat 'docker build -t tankworld-community:latest services\\community'
                bat 'docker build -t tankworld-battle:latest services\\battle'
                bat 'docker build -t tankworld-frontend-k8s:latest client'
            }
        }

        stage('Verify Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                bat 'kubectl get nodes'
            }
        }

        stage('Deploy to Kubernetes') {
            when {
                branch 'main'
            }
            steps {
                bat 'powershell.exe -NoProfile -ExecutionPolicy Bypass -File k8s\\deploy.ps1'
            }
        }
    }

    post {
        success {
            echo "Kubernetes pipeline finished successfully for ${env.BRANCH_NAME}"
        }

        failure {
            echo "Pipeline stopped: tests, build or deployment failed for ${env.BRANCH_NAME}"
        }
    }
}
