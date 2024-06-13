@Library('Jenkins-Shared-Library')_
pipeline {
    agent any
    
    environment {
    dockerHubCredentialsID	    = 'DockerHub'  		    			// DockerHub credentials ID.
    imageName   		        = 'mostafayounis0/spring-boot-app'     			        // DockerHub repo/image name.
	openshiftCredentialsID	    = 'openshift'	    				// KubeConfig credentials ID.   
	nameSpace                   = 'mostafayounis'
	clusterUrl                  = 'https://api.ocp-training.ivolve-test.com:6443'
	gitRepoName 	            = 'Multi_Cloud_DevOps_project'
    gitUserName 	            = 'mostafayouni'
	gitUserEmail                = 'mostafayounis053@gmail.com'
	githubToken                 = 'GitHub'
	sonarqubeUrl                = 'http://54.226.112.27:9000'
	sonarTokenCredentialsID     = 'sonar-token'
 	k8sCredentialsID	        = 'kubernetes'
	
    }
    
    stages {       

        stage('Run Unit Test') {
            steps {
                script {
                    dir('App') {	
                	         runUnitTests()
                    }
        	}
    	    }
	}
	stage('Build') {
            steps {
                script {
                	dir('App') {
                	         build()	
                    }
        	}
            }
        }
	stage('SonarQube Analysis') {
            steps {
                script {
                    dir('App') {
                                sonarQubeAnalysis()	
                        }
            }
        }
    }

    stage('Build and Push Docker Image') {
        steps {
            script {
                dir('App') {
                        buildandPushDockerImage("${dockerHubCredentialsID}", "${imageName}")
                }	
            }
        }
    }
     stage('Edit new image in deployment.yaml file') {
            steps {
                script { 
                    
                    editNewImage("${githubToken}", "${imageName}", "${gitUserEmail}", "${gitUserName}", "${gitRepoName}")
                
                }
            }
        }

    stage('Deploy on OpenShift Cluster') {
        steps {
            script { 
                dir('oc') {
                            
                    deployOnOc("${openshiftCredentialsID}", "${nameSpace}", "${clusterUrl}")
                }
            }
        }
    }
    }

    post {
        success {
            echo "${JOB_NAME}-${BUILD_NUMBER} pipeline succeeded"
        }
        failure {
            echo "${JOB_NAME}-${BUILD_NUMBER} pipeline failed"
        }
    }
}
