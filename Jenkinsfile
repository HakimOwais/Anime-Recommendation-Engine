pipeline {
    agent any 

    stages{
        stage("Cloning code from Github Repo ..."){
            steps{
                script{
                    echo "Cloning code from Github Repo ..."
                    checkout scmGit(branches: [[name: '*/main']], extensions: [], userRemoteConfigs: [[credentialsId: 'github-token', url: 'https://github.com/HakimOwais/Recommendation-Engine.git']])
                }
            }
        }
    }
}