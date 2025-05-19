pipeline {
    agent any

    stages {
        // Этап 1: Запуск QEMU
        stage('Start QEMU') {
            steps {
                script {
                    sh 'chmod +x qemu_start.sh && ./qemu_start.sh'
                    sleep(time: 30, unit: 'SECONDS')
                }
            }
        }

        // Этап 2: Тесты авторизации
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

        // Этап 3: Web-тесты
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

        // Этап 4: Нагрузочное тестирование
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

    // Глобальный post-обработчик
    post {
        always {
            sh 'pkill -f qemu-system-arm || true'
        }
    }
}
