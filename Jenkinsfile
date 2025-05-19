pipeline {
    agent any

    stages {
        // Этап 0: Проверка содержимого репозитория
        stage('Debug: Check Files') {
            steps {
                sh '''
                    echo "Current directory: $(pwd)"
                    ls -la
                    echo "Checking qemu_start.sh..."
                    ls -l qemu_start.sh || true
                '''
            }
        }

        // Этап 1: Запуск QEMU
        stage('Start QEMU') {
            steps {
                script {
                    sh '''
                        dos2unix qemu_start.sh || true  # Исправляем формат
                        chmod 755 qemu_start.sh
                        ./qemu_start.sh
                    '''
                }
            }
        }

        // Остальные этапы остаются без изменений
        stage('Auth Tests') {
            steps {
                sh '/opt/venv/bin/pytest tests/auth/ --junitxml=auth-results.xml'
            }
            post {
                always {
                    junit 'auth-results.xml'
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
        }
    }
}
