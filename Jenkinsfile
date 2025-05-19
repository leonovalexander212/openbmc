pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', 
                    url: 'https://github.com/leonovalexander212/openbmc.git'
            }
        }
        
        stage('Start QEMU') {
            steps {
                script {
                    sh 'chmod +x qemu_start.sh'
                    sh 'Xvfb :99 -screen 0 1024x768x24 &'  
                    sh './qemu_start.sh &'
                    
                    def maxAttempts = 33
                    def waitTime = 3
                    def attempts = 0
                    def bmcAvailable = false
                    
                    echo "Ожидание доступности OpenBMC..."
                    
                    while (attempts < maxAttempts && !bmcAvailable) {
                        attempts++
                        try {
                            def status = sh(
                                script: 'curl -k -s -o /dev/null -w "%{http_code}" https://localhost:2443/redfish/v1',
                                returnStdout: true
                            ).trim()
                            
                            if (status == "200") {
                                bmcAvailable = true
                                echo "OpenBMC доступен после ${attempts * waitTime} секунд"
                            } else {
                                sleep(waitTime)
                            }
                        } catch (Exception e) {
                            sleep(waitTime)
                        }
                    }
                    
                    if (!bmcAvailable) {
                        error("OpenBMC не стал доступен после ${maxAttempts * waitTime} секунд ожидания")
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'romulus/*.mtd', allowEmptyArchive: true
                }
            }
        }

        stage('Check OpenBMC Availability') {
            steps {
                script {
                    sh '''
                    echo "Проверяем доступность OpenBMC..."
                    if curl -k https://localhost:2443; then
                        echo "OpenBMC доступен!"
                    else
                        echo "Ошибка: OpenBMC не отвечает на localhost:2443"
                        exit 1
                    fi
                    '''
                }
            }
        }

        stage('Auth Tests') {
            steps {
                sh '/opt/venv/bin/pytest tests/auth/ --junitxml=auth-results.xml'
            }
            post {
                always {
                    junit 'auth-results.xml'
                    archiveArtifacts artifacts: 'auth-results.xml'
                }
            }
        }

        stage('Web Tests') {
            steps {
                sh 'xvfb-run /opt/venv/bin/pytest tests/webui/ --junitxml=webui-results.xml'
            }
            post {
                always {
                    junit 'webui-results.xml'
                    archiveArtifacts artifacts: 'webui-results.xml'
                }
            }
        }

        stage('Load Test') {
            steps {
                sh '/opt/venv/bin/locust -f tests/load/locustfile.py --headless -u 100 -r 10 --run-time 1m --host=https://localhost:2443 --html report.html'
            }
            post {
                always {
                    archiveArtifacts artifacts: 'report.html'
                }
            }
        }
    }

    post {
        always {
            sh 'pkill -f qemu-system-arm || true'
            sh 'pkill -f Xvfb || true'
        }
    }
}
