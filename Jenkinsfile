pipeline {
    agent any
    environment {
        GITHUB_WEBHOOK_URL = 'https://bbc0-115-76-50-187.ngrok-free.app/github-webhook/'
        REPO_URL = 'https://github.com/phuc-blt/Jenkins_test.git'
        BRANCH_NAME = 'main'
        DOCKER_IMAGE = 'fastapi-app'
        CONTAINER_NAME = 'fastapi-app-container'
    }
    triggers {
        GenericTrigger(
            genericVariables: [
                [key: 'WEBHOOK_TRIGGER', value: '$.trigger', defaultValue: '']
            ],
            causeString: 'Triggered by webhook',
            token: 'push_here',
            printContributedVariables: true,
            printPostContent: true
        )
    }
    options {
        skipDefaultCheckout() // Prevent automatic checkout
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    githubChecks(name: 'Checkout', status: 'IN_PROGRESS', summary: 'Cloning repository...')
                }
                git branch: env.BRANCH_NAME, url: env.REPO_URL
                script {
                    githubChecks(name: 'Checkout', status: 'COMPLETED', conclusion: 'SUCCESS', summary: 'Repository cloned successfully.')
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    githubChecks(name: 'Build Docker Image', status: 'IN_PROGRESS', summary: 'Building Docker image...')
                }
                sh "docker build -t ${env.DOCKER_IMAGE} ."
                script {
                    githubChecks(name: 'Build Docker Image', status: 'COMPLETED', conclusion: 'SUCCESS', summary: 'Docker image built successfully.')
                }
            }
        }
        stage('Run Docker Container') {
            steps {
                script {
                    githubChecks(name: 'Run Docker Container', status: 'IN_PROGRESS', summary: 'Starting Docker container...')
                }
                sh """
                docker stop ${env.CONTAINER_NAME} || true
                docker rm ${env.CONTAINER_NAME} || true
                docker run -d -p 8080:8080 --name ${env.CONTAINER_NAME} ${env.DOCKER_IMAGE}
                """
                script {
                    githubChecks(name: 'Run Docker Container', status: 'COMPLETED', conclusion: 'SUCCESS', summary: 'Docker container started successfully.')
                }
            }
        }
        stage('Notify GitHub via Webhook') {
            steps {
                script {
                    githubChecks(name: 'Notify GitHub', status: 'IN_PROGRESS', summary: 'Notifying GitHub via webhook...')
                }
                sh """
                curl -X POST -H "Content-Type: application/json" \
                -d '{"state": "success", "description": "Pipeline is running", "context": "ci/jenkins"}' \
                ${env.GITHUB_WEBHOOK_URL}
                """
                script {
                    githubChecks(name: 'Notify GitHub', status: 'COMPLETED', conclusion: 'SUCCESS', summary: 'GitHub notified successfully.')
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    githubChecks(name: 'Run Tests', status: 'IN_PROGRESS', summary: 'Running tests...')
                }
                sh """
                docker exec ${env.CONTAINER_NAME} pytest /app/tests/
                """
                script {
                    githubChecks(name: 'Run Tests', status: 'COMPLETED', conclusion: 'SUCCESS', summary: 'Tests completed successfully.')
                }
            }
        }
    }
    post {
        always {
            withChecks('Run FastAPI App') {
                publishChecks name: 'Run FastAPI App', status: 'COMPLETED', conclusion: 'NEUTRAL',
                             summary: 'Pipeline has completed execution.'
            }
        }
    }
}
