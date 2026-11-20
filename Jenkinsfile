pipeline {
    agent any

    environment {
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

        stage('Build microservice images') {
            steps {
                bat 'docker build -t tankworld-catalog:latest services\\catalog'
                bat 'docker build -t tankworld-community:latest services\\community'
                bat 'docker build -t tankworld-battle:latest services\\battle'
                bat 'docker build -t tankworld-frontend-k8s:latest client'
            }
        }

        stage('Test microservices') {
            steps {
                bat 'docker run --rm tankworld-catalog:latest python -m pytest -q'
                bat 'docker run --rm tankworld-community:latest python -m pytest -q'
                bat 'docker run --rm tankworld-battle:latest python -m pytest -q'
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
            echo "Kubernetes pipeline failed for ${env.BRANCH_NAME}"
        }
    }
}