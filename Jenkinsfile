pipeline {
  agent any

  tools {
    git 'Default Git'
  }

  environment {
    SONARQUBE_SCANNER_HOME = tool 'SonarScanner'
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/TS-Anusha/jenkins-sonarqube-test'
      }
    }

    stage('Lint') {
      steps {
        sh 'pip install pylint'
        sh 'pylint Summarizer.py || true' // Continue even if lint fails
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('LocalSonarQube') {
          sh "${SONARQUBE_SCANNER_HOME}/bin/sonar-scanner"
        }
      }
    }

    stage('Quality Gate') {
      steps {
        timeout(time: 1, unit: 'MINUTES') {
          waitForQualityGate abortPipeline: true
        }
      }
    }
  }
}
