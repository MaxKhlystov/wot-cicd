pipeline {
    agent any

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

        stage('Build Docker images') {
            steps {
                bat 'docker compose build'
            }
        }

        stage('Test backend in Docker') {
            steps {
                bat 'docker compose run --rm backend python -m pytest'
            }
        }

        stage('Deploy containers') {
            when {
                branch 'main'
            }
            steps {
                bat 'docker compose up -d --remove-orphans'
                bat 'docker compose ps'
            }
        }
    }

    post {
        success {
            echo "Docker pipeline finished successfully for ${env.BRANCH_NAME}"
        }

        failure {
            echo "Docker pipeline failed for ${env.BRANCH_NAME}"
        }
    }
}