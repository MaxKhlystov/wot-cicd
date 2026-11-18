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
                bat '''
                    set BUILD_ID=dontKillMe
                    taskkill /F /FI "WINDOWTITLE eq tankworld-server" 2>nul
                    start "tankworld-server" /min cmd /c "%PYTHON% manage.py runserver 0.0.0.0:8000"
                '''
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
