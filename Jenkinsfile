pipeline {
    agent none
    stages {
        stage('git') {
            agent {
                docker {
                    image 'python:3.9-alpine'
                    args '-u root:root'
                }
             }
            steps {
                git branch: 'main', url: 'https://github.com/kusnitsyn/flask-api_v2.git'
                sh 'apk update && apk add postgresql-dev gcc python3-dev musl-dev make libc-dev g++'
                sh 'pip install -r requirements.txt'
            }
         }
         stage('Ansible') {
             agent any
             steps{
                 ansiblePlaybook credentialsId: 'private-key', installation: 'ansibleCD', inventory: '/opt/ansible/inventory/aws_ec2.yaml', playbook: '/home/ubuntu/playbooks/blue.yml'
             }
        }
    }
}