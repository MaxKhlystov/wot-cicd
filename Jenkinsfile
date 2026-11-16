pipeline {
    agent any

    environment {
        APP_NAME = "tankworld"
        APP_PORT = "8000"

        // Python, установленный на компьютере
        SYSTEM_PYTHON = "C:\\Users\\maksi\\AppData\\Local\\Programs\\Python\\Python313\\python.exe"

        // Виртуальное окружение, создаваемое Jenkins в рабочей папке
        VENV_PYTHON = ".jenkins-venv\\Scripts\\python.exe"

        // Node.js, установленный на компьютере
        NODE_HOME = "G:\\Apps\\Others\\node"

        // Добавляем Node.js в PATH внутри Jenkins Pipeline
        PATH+NODE = "G:\\Apps\\Others\\node"
    }

    options {
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '20'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm

                bat '''
                    echo Current branch: %BRANCH_NAME%
                    echo Workspace: %WORKSPACE%
                '''
            }
        }

        stage('Check environment') {
            steps {
                bat '''
                    echo Checking Python...
                    "%SYSTEM_PYTHON%" --version

                    echo Checking Git...
                    git --version

                    echo Checking Node.js...
                    "%NODE_HOME%\\node.exe" --version

                    echo Checking npm...
                    call "%NODE_HOME%\\npm.cmd" --version
                '''
            }
        }

        stage('Create Python environment') {
            steps {
                bat '''
                    if not exist "%VENV_PYTHON%" (
                        echo Creating Python virtual environment...
                        "%SYSTEM_PYTHON%" -m venv .jenkins-venv
                    ) else (
                        echo Python virtual environment already exists
                    )

                    "%VENV_PYTHON%" -m pip install --upgrade pip
                '''
            }
        }

        stage('Install backend dependencies') {
            steps {
                bat '''
                    echo Installing backend dependencies...
                    "%VENV_PYTHON%" -m pip install -r requirements.txt
                '''
            }
        }

        stage('Check Django project') {
            steps {
                bat '''
                    echo Running Django system check...
                    "%VENV_PYTHON%" manage.py check

                    echo Checking Django migrations...
                    "%VENV_PYTHON%" manage.py makemigrations --check --dry-run
                '''
            }
        }

        stage('Test backend') {
            steps {
                bat '''
                    echo Running backend tests...

                    if not exist reports (
                        mkdir reports
                    )

                    "%VENV_PYTHON%" -m pytest
                '''
            }
        }

        stage('Install frontend dependencies') {
            steps {
                dir('client') {
                    bat '''
                        echo Installing frontend dependencies...
                        call "%NODE_HOME%\\npm.cmd" ci
                    '''
                }
            }
        }

        stage('Build frontend') {
            steps {
                dir('client') {
                    bat '''
                        echo Building Vue frontend...
                        call "%NODE_HOME%\\npm.cmd" run build
                    '''
                }
            }
        }

        stage('Deploy main') {
            when {
                branch 'main'
            }

            steps {
                bat '''
                    echo Applying Django migrations...
                    "%VENV_PYTHON%" manage.py migrate

                    echo Stopping previous TankWorld server...
                    taskkill /F /FI "WINDOWTITLE eq tankworld-server" 2>nul || echo Previous server was not found

                    echo Starting TankWorld server...
                    set BUILD_ID=dontKillMe
                    set JENKINS_NODE_COOKIE=dontKillMe

                    start "tankworld-server" /min cmd /c %VENV_PYTHON% manage.py runserver 0.0.0.0:%APP_PORT%

                    echo TankWorld started on port %APP_PORT%
                '''
            }
        }
    }

    post {
        always {
            junit(
                allowEmptyResults: true,
                testResults: 'reports/junit.xml'
            )

            archiveArtifacts(
                allowEmptyArchive: true,
                artifacts: 'client/dist/**'
            )
        }

        success {
            echo "Pipeline completed successfully for branch ${env.BRANCH_NAME}"
        }

        failure {
            echo "Pipeline failed for branch ${env.BRANCH_NAME}. Check the stages and console output."
        }
    }
}