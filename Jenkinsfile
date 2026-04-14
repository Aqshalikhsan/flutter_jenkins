pipeline {
    agent any

    options {
        timeout(time: 60, unit: 'MINUTES')  // ⏱️ Total timeout 60 menit
        timestamps()
        disableConcurrentBuilds()
        // Retry jika build gagal karena transient error
        retry(2)
    }

    environment {
        FLUTTER_HOME = '/opt/flutter'
        ANDROID_HOME = '/opt/android-sdk'
        ANDROID_SDK_ROOT = '/opt/android-sdk'
    }

    stages {
        stage('🔍 Verify Environment') {
            steps {
                sh '''
                    echo "Flutter: $(${FLUTTER_HOME}/bin/flutter --version | head -1)"
                    echo "Android SDK: ${ANDROID_HOME}"
                    ls -la ${ANDROID_HOME}/cmdline-tools/latest/bin/sdkmanager
                '''
            }
        }

        stage('📦 Get Dependencies') {
            steps {
                dir('register_system/backend/flutter_app') {
                    sh '${FLUTTER_HOME}/bin/flutter pub get'
                }
            }
        }

        stage('🔨 Build APK Release') {
            options {
                timeout(time: 45, unit: 'MINUTES')  // Build bisa lama
            }
            steps {
                dir('register_system/backend/flutter_app') {
                    sh '''
                        set +e  // Jangan exit on error untuk debugging
                        
                        # Export environment
                        export FLUTTER_HOME="${FLUTTER_HOME}"
                        export ANDROID_HOME="${ANDROID_HOME}"
                        export ANDROID_SDK_ROOT="${ANDROID_SDK_ROOT}"
                        export PATH="${FLUTTER_HOME}/bin:${ANDROID_HOME}/cmdline-tools/latest/bin:${ANDROID_HOME}/platform-tools:$PATH"
                        
                        echo "🧹 Cleaning..."
                        ${FLUTTER_HOME}/bin/flutter clean
                        
                        echo "📦 Getting dependencies..."
                        ${FLUTTER_HOME}/bin/flutter pub get
                        
                        echo "🔨 Building APK (may take 10-20 minutes)..."
                        echo "💡 Do NOT restart Jenkins during this step!"
                        
                        # Build dengan verbose
                        ${FLUTTER_HOME}/bin/flutter build apk --release --verbose
                        BUILD_EXIT_CODE=$?
                        
                        if [ $BUILD_EXIT_CODE -ne 0 ]; then
                            echo "❌ Build failed with exit code: $BUILD_EXIT_CODE"
                            exit $BUILD_EXIT_CODE
                        fi
                        
                        echo "✅ Build complete!"
                        ls -lh build/app/outputs/flutter-apk/*.apk
                    '''
                }
            }
        }

        stage('📤 Archive APK') {
            steps {
                archiveArtifacts artifacts: 'register_system/backend/flutter_app/build/app/outputs/flutter-apk/*.apk', 
                                 allowEmptyArchive: false,
                                 fingerprint: true
            }
        }
    }

    post {
        success {
            echo '✅ Build SUCCESS! Download APK dari Artifacts section.'
        }
        failure {
            echo '❌ Build FAILED! Cek console output untuk detail.'
            echo '💡 Jika Jenkins restart, cek memory dengan: free -h && sudo dmesg | grep -i oom'
        }
        always {
            dir('register_system/backend/flutter_app') {
                sh '${FLUTTER_HOME}/bin/flutter clean || true'
            }
        }
    }
}