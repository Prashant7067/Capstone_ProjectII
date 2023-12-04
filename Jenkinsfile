pipeline {
    agent any
    options {
        skipDefaultCheckout(true)
    }

    stages {
        stage('Git Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/Prashant7067/Capstone_ProjectII.git'
            }
        }
        
        stage('Build Images') {
            steps {
                script {
                    bat 'docker build -t prashantpandey103/capstone_project:code .'
                }
            }
        }

        stage('Push Images to Hub') {
            steps {
                withDockerRegistry([ credentialsId: "prashant-dockerhub", url: "" ]) {
                    bat 'docker push prashantpandey103/capstone_project:code'
                }
            }
        }
    }

    post {
        always {
            /* This block will always be executed, regardless of the build result */
            bat 'docker logout'
        }

        /* Uncomment the blocks below and adjust as needed */
        
        failure {
            emailext(
                attachLog: true,
                body: '''<html>
                        <p>The build failed. Please check the Jenkins console output for details.</p>
                        <p>Build URL: ${BUILD_URL}</p>
                        </html>''',
                subject: 'Build Failure',
                to: 'prashant.pandey20@st.niituniversity.in, yashwant.gudeti20@st.niituniversity.in,jammula.supriya20@st.niituniversity.in ',
                mimeType: 'text/html'
            )
        }

        success {
            emailext(
                attachLog: true,
                body: 'The build was successful.',
                subject: 'Build Success',
                to: 'prashant.pandey20@st.niituniversity.in, yashwant.gudeti20@st.niituniversity.in,jammula.supriya20@st.niituniversity.in',
                mimeType: 'text/html'
            )
        }
        
    }
}
