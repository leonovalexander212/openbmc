pipeline {
    agent any

    stages {
        stage('Start QEMU') {
            steps {
                sh 'chmod +x qemu_start.sh && ./qemu_start.sh'
                sleep(time: 30, unit: 'SECONDS')  // Ожидание запуска
            }
        }

	stage('Auth Tests') {
	    steps {
		sh '/opt/venv/bin/pytest tests/auth/ --junitxml=auth-results.xml'
	    }
	}

	stage('Web Tests') {
	    steps {
		sh 'xvfb-run /opt/venv/bin/pytest tests/webui/'
	    }
	}

	stage('Load Test') {
	    steps {
		sh '/opt/venv/bin/locust -f tests/load/locustfile.py ...'
	    }
	}
