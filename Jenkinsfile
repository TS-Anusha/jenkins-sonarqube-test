pipeline {
  agent any

 environment {
  VENV_DIR = '.venv'
  OPENAI_API_KEY = credentials('OPENAI_API_KEY') 
  SONARQUBE_SCANNER = tool 'sonarqube scanner'  /
}

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/TS-Anusha/jenkins-sonarqube-test', branch: 'main'
      }
    }

    stage('Setup Python Env') {
      steps {
        sh '''
          python3 -m venv $VENV_DIR
          source $VENV_DIR/bin/activate
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Lint') {
      steps {
        sh '''
          source $VENV_DIR/bin/activate
          pip install pylint
          pylint Summarizer.py
        '''
      }
    }

    stage('SonarQube Analysis') {
      steps {
        withSonarQubeEnv('LocalSonarQube') {
          sh '''
            source $VENV_DIR/bin/activate
            ${SONARQUBE_SCANNER}/bin/sonar-scanner \
              -Dsonar.projectKey=jenkins-sonarqube-test \
              -Dsonar.sources=. \
              -Dsonar.python.version=3.8 \
              -Dsonar.login=$sonarqube-auth-token
          '''
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

    stage('Run Code') {
      steps {
        sh '''
          source $VENV_DIR/bin/activate
          python Summarizer.py
        '''
      }
    }
  }
}
