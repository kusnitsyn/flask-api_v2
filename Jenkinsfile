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
                    args '-u root:root'
                  }
            }
            steps {
                sh 'git clone -b main https://github.com/kusnitsyn/flask-api_v2.git  && cd flask-api_v2/'
                sh 'pip install -r requirements.txt'
                sh 'nohup python app.py &'
                sh 'python test.py'
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
