pipeline {
    agent none
    stages {
        stage('Disable Blue') {
            agent any
            steps {
               ansiblePlaybook credentialsId: 'private-key', installation: 'ansibleCD', inventory: '/opt/ansible/inventory/aws_ec2.yaml', playbook: '/etc/ansible/roles/green/nginx_green.yml' 
            }
        }
        stage ('Testing inside Docker') {
            agent {
                dockerfile {
                    args '-u root:root'
                    filename 'Dockerfile'
                    dir '/home/ubuntu/project'
                }
            }
            steps {
                sh 'rm -Rf flask-api_v2/'
                sh 'git clone -b main https://github.com/kusnitsyn/flask-api_v2.git  && cd flask-api_v2/'
                sh 'su - postgres -c "initdb -D /var/lib/postgresql/data && pg_ctl start -D /var/lib/postgresql/data -l /var/lib/postgresql/log.log && createuser python && createdb python"'
                sh 'pip install -r requirements.txt'
                sh 'pg_isready -U postgres'
                sh 'nohup python3 app.py >> app.log &'
                sh 'python3 test.py'
            }
            post {
                success {
                    script {
                        withCredentials([string(credentialsId: 'telegramToken', variable: 'TOKEN'), string(credentialsId: 'telegramChatId', variable: 'CHAT_ID')]) {
                        sh '''
                        curl -s -X POST https://api.telegram.org/bot$TOKEN/sendMessage -d chat_id=$CHAT_ID -d text="All tests passed\
                        Build: $BUILD_TAG\
                        Branch: main"
                        '''
                        }
                    }
                }
                failure {
                    script {
                        withCredentials([string(credentialsId: 'telegramToken', variable: 'TOKEN'), string(credentialsId: 'telegramChatId', variable: 'CHAT_ID')]) {
                        sh '''
                        curl -s -X POST https://api.telegram.org/bot$TOKEN/sendMessage -d chat_id=$CHAT_ID -d text="Tests failed\
                        Build: $BUILD_TAG\
                        Branch: main"
                        '''
                        }
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
        stage ('Free up some space') {
            agent any
            steps {
                sh 'docker container prune -f'
            }
        }
    }
}