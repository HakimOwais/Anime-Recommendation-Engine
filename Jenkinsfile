pipeline {
    agent any 

    environment {
        VENV_DIR = 'venv'
    }

    stages{

        stage("Cloning code from Github Repo ..."){
            steps{
                script{
                    echo "Cloning code from Github Repo ..."
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/HakimOwais/Recommendation-Engine.git']])
                }
            }
        }

        stage("Creating Virtual env ..."){
            steps{
                script{
                    echo "Creating Virtual env ..."
                    sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -e .
                    pip install dvc
                    '''
                    }
            }
        }

        stage('DVC Pull'){
            steps{
                withCredentials([file(credentialsId:'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]){
                    script{
                        echo 'DVC Pull ...'
                        sh '''
                        . ${VENV_DIR}/bin/activate
                        dvc pull
                        '''
                    }
                }
            }
        }
    }
}