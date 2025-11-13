pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building project...'
                sh 'exit 1'  // simulate failure
            }
        }
    }

    post {
        failure {
            script {
                def incident = [
                    build_name: env.JOB_NAME,
                    status: "FAILED",
                    error_message: currentBuild.description ?: "Build failed"
                ]
                def payload = groovy.json.JsonOutput.toJson(incident)

                sh """
                curl -X POST \
                -H "Content-Type: application/json" \
                -d '${payload}' \
                https://abcd1234.execute-api.ap-south-1.amazonaws.com/log
                """
            }
        }
    }
}
