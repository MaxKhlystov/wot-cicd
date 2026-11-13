pipeline {
    agent any

    environment {
        APP_NAME = "tankworld"
        APP_PORT = "8000"
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
                dir('backend') {
                    bat 'python -m pip install -r requirements.txt'
                }
            }
        }

        stage('Migrate DB') {
            steps {
                dir('backend') {
                    bat 'python manage.py migrate'
                }
            }
        }

        stage('Test') {
            steps {
                dir('backend') {
                    bat 'python -m pytest --junitxml=reports/junit.xml'
                }
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'backend/reports/junit.xml'
                }
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                dir('backend') {
                    bat '''
                        set BUILD_ID=dontKillMe
                        set JENKINS_NODE_COOKIE=dontKillMe
                        taskkill /F /FI "WINDOWTITLE eq tankworld-server" 2>nul || echo no-previous-process
                        start "tankworld-server" /min cmd /c "python manage.py runserver 0.0.0.0:%APP_PORT%"
                        echo Deployed on port %APP_PORT%
                    '''
                }
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
