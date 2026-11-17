pipeline {
    agent any

    environment {
        APP_NAME = "tankworld"
        APP_PORT = "8000"
        PYTHON = "C:\\Users\\maksi\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"
    }

    options {
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

        stage('Install dependencies') {
            steps {
                bat '"%PYTHON%" -m pip install -r requirements.txt'
            }
        }

        stage('Migrate DB') {
            steps {
                bat '"%PYTHON%" manage.py migrate'
            }
        }

        stage('Test') {
            steps {
                bat '"%PYTHON%" -m pytest --junitxml=reports/junit.xml'
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'reports/junit.xml'
                }
            }
        }

        stage('Deploy') {
            when { branch 'main' }
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
            echo "Pipeline finished OK for branch ${env.BRANCH_NAME}"
        }
        failure {
            echo "Pipeline FAILED for branch ${env.BRANCH_NAME} --- see logs above"
        }
    }
}
