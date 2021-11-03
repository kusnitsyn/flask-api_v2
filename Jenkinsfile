pipeline {
    agent none
    stages {
        stage('Disable Blue') {
            agent any
            steps {
               ansiblePlaybook credentialsId: 'private-key', installation: 'ansibleCD', inventory: '/opt/ansible/inventory/aws_ec2.yaml', playbook: '/etc/ansible/roles/green/nginx_green.yml' 
            }
        }
        stage('Test') {
            agent { 
                dockerfile { 
                    filename 'Dockerfile'
                    dir '/home/ubuntu/project'
                    args '-u root:root'
                }
            }
            steps {
                git branch: 'main', url: 'https://github.com/kusnitsyn/flask-api_v2.git'
                sh 'pip3 install -r requirements.txt'
                sh 'nohup python3 app.py &'
                sh 'python3 test.py'
            }
        }
        stage('Push Notification') {
            agent any
            steps {
                script {
                    withCredentials([string(credentialsId: 'telegramToken', variable: 'TOKEN'), string(credentialsId: 'telegramChatId', variable: 'CHAT_ID')]) {
                    sh '''
                    curl -s -X POST https://api.telegram.org/bot$TOKEN/sendMessage -d chat_id=$CHAT_ID -d text="All tests passed\
                    Build: $BUILD_TAG\
                    Branch: $GIT_BRANCH"
                    '''
                    }
                }
            }
        }
         stage('Enable Blue') {
             agent any
             steps{
                 ansiblePlaybook credentialsId: 'private-key', installation: 'ansibleCD', inventory: '/opt/ansible/inventory/aws_ec2.yaml', playbook: '/etc/ansible/roles/blue/blue.yml'
             }
        }
    }
}
