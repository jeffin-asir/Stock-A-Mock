pipeline {
  agent any

  options {
    timestamps()
    disableConcurrentBuilds()
    buildDiscarder(logRotator(numToKeepStr: '15'))
  }

  environment {
    TEST_COMPOSE = 'docker compose -p stock-ci -f docker-compose.test.yml'
    DEPLOY_COMPOSE = 'docker compose -p stock-cd -f docker-compose.yml'
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
        sh 'git rev-parse --short HEAD'
      }
    }

    stage('Build') {
      steps {
        sh '''
          mkdir -p reports
          ${TEST_COMPOSE} build
        '''
      }
    }

    stage('Selenium Tests') {
      steps {
        sh '''
          ${TEST_COMPOSE} up --abort-on-container-exit --exit-code-from selenium-tests
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'reports/*.xml'
          archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
          sh '${TEST_COMPOSE} down -v || true'
        }
      }
    }

    stage('Deploy') {
      when {
        anyOf {
          branch 'main'
          branch 'master'
        }
      }
      steps {
        sh '''
          ${DEPLOY_COMPOSE} up -d --build
          ${DEPLOY_COMPOSE} ps
        '''
      }
    }
  }

  post {
    failure {
      echo 'Pipeline failed. Faulty code was not deployed.'
    }
    success {
      echo 'Pipeline completed successfully.'
    }
  }
}
