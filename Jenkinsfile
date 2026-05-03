pipeline {
    agent any

    environment {
        JAVA_HOME = "/usr/lib/jvm/java-21-openjdk-amd64"
        ANDROID_HOME = "/var/lib/jenkins/Android/Sdk"
        ANDROID_SDK_ROOT = "/var/lib/jenkins/Android/Sdk"
        PATH = "${env.PATH}:${JAVA_HOME}/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/cmdline-tools/latest/bin"
    }

    stages {

        stage('Build Flutter APK') {
            steps {
                dir('register_system/backend/flutter_app') {

                    sh 'flutter clean'
                    sh 'flutter pub get'
                    sh 'flutter build apk --release'

                }
            }
        }

        stage('Archive APK') {
            steps {
                archiveArtifacts artifacts: 'register_system/backend/flutter_app/build/app/outputs/flutter-apk/*.apk'
            }
        }

    }

    post {
        success {
            echo 'Flutter APK build success'
        }
    }
}