# Multi-Cloud DevOps Project
![Architecture_Diagram](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/0d1c4513-ad73-44a3-a6d0-1ae72cd95008)


## OpenShift Deployment Automation with Jenkins

This repository contains comprehensive documentation for deploying a Java web application on OpenShift using tools such as Terraform, Ansible, Jenkins, and more.

### Tools Used
- Bash scripting
- Git
- SonarQube
- Docker
- Terraform
- AWS
- Ansible
- Jenkins
- OpenShift

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Manual Testing, Building, and Running Procedures](#manual-testing-building-and-running-procedures)
3. [Infrastructure Provisioning with Terraform](#infrastructure-provisioning-with-terraform)
4. [Ansible Playbook for Configuration](#ansible-playbook-for-configuration)
5. [Jenkins Pipeline](#jenkins-pipeline)
6. [OpenShift Deployment](#openshift-deployment)
7. [Monitoring and Logging OpenShift Cluster](#monitoring-and-logging-openshift-cluster)

## Prerequisites

Ensure the following tools are installed:
- Terraform
- Ansible
- OpenShift CLI (`oc`)

## Manual Testing, Building, and Running Procedures

This section provides a comprehensive guide to the manual steps required before automating the deployment process.

### 1. Execute Unit Tests

Run the following command to execute unit tests:
```sh
./gradlew test
```
To access test results, navigate to the following path and open the `index.html` file:
```sh
cd build/reports/tests/test/
```
![Test Results](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/8fb82928-67da-4922-bdca-abf93edfdcee)

### 2. Perform SonarQube Analysis

Ensure your SonarQube project is configured with the necessary project key and login token. Run the following command:
```sh
./gradlew sonar \
-Dsonar.projectKey=<project_key> \
-Dsonar.host.url=<host_server_url> \
-Dsonar.login=<login_token>
```
![SonarQube Analysis](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/ad77cfa2-58ea-4035-8c20-5b97dd965c36)

### 3. Build and Run Application

Build the application:
```sh
./gradlew build --stacktrace
```
Run the application:
```sh
java -jar demo.jar
```
Access the application locally at `http://localhost:8081`.
![Application Running Locally](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/16975e1d-fbd5-43d4-9241-521aee03db58)

### 4. Build Docker Image and Run Container

Build the Docker image:
```sh
docker build -t <image_name> .
```
Run the Docker container:
```sh
docker run --name=<container_name> -d -p 8081:8081 <image_name>
```
![Docker Container](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/54b66cbd-213a-44bf-a41c-d286f97dd1f3)

## Infrastructure Provisioning with Terraform

This section provides comprehensive instructions for deploying infrastructure using Terraform. The project includes modules for VPC, subnet, EC2, and CloudWatch.

### Overview

- **main.tf:** Configures and defines the cloud provider and calls Terraform modules.
- **variables.tf:** Sets variables that need to be defined in the `terraform.tfvars` file.
- **terraform.tfvars:** Defines values for the necessary variables.
- **Remote Backend:** Stores Terraform state remotely using S3 and DynamoDB.

![Terraform Infrastructure](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/028a4a29-6abd-443c-8d66-2e70dae1e319)

### VPC Module

Provisions a Virtual Private Cloud (VPC) with an internet gateway for public access.
- **Files:** `vpc/main.tf`, `vpc/variables.tf`, `vpc/outputs.tf`

![VPC Module](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/ed4a38d4-323f-4d61-affe-c87fb7df0977)

### Subnet Module

Defines a public subnet and route table.
- **Files:** `subnet/main.tf`, `subnet/variables.tf`, `subnet/outputs.tf`

![Subnet Module](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/6fef00e9-5941-4587-8736-c5b268ab284c)

### EC2 Module

Creates an EC2 instance with the necessary security group.
- **Files:** `ec2/main.tf`, `ec2/variables.tf`, `ec2/outputs.tf`

![EC2 Module](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/d7672b74-3d90-416d-9899-f089b3e6306d)

### CloudWatch Module

Sets up CloudWatch resources for monitoring and SNS resources for sending emails for alarms.
- **Files:** `cloudwatch/main.tf`, `cloudwatch/variables.tf`, `cloudwatch/outputs.tf`

![CloudWatch Module](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/ce6136fa-5116-4843-9188-e0f07c4b1f49)

### Usage

1. Update values in the `terraform.tfvars` file.
2. Initialize and apply Terraform configurations:
    ```sh
    terraform init
    terraform apply
    ```
3. Follow on-screen prompts to provision infrastructure.
4. To destroy the infrastructure:
    ```sh
    terraform destroy
    ```
![Terraform Apply](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/9b7714e7-3ffd-4c57-95e7-8bc44ceb920a)

## Ansible Playbook for Configuration

This section provides an overview of the Ansible playbook for installing and configuring Jenkins on an EC2 instance, along with additional roles for SonarQube, PostgreSQL, and Docker.

### Roles Structure and Details

- **Prerequisite Role:** Installs required packages on the EC2 instance.
- **Postgres Role:** Installs and configures PostgreSQL for SonarQube.
- **SonarQube Role:** Installs and configures SonarQube on the EC2 instance.
- **Git Role:** Installs Git on the EC2 instance.
- **Jenkins Role:** Installs and configures Jenkins on the EC2 instance, including setting admin credentials and installing necessary plugins.
- **Docker Role:** Installs and configures Docker on the EC2 instance.

### Usage

1. Use dynamic inventory to get the IP of the EC2 instance:
    ```sh
    python3 dynamic_inv.py
    ```
2. Update Jenkins admin credentials in `ansible/roles/jenkins/vars/main.yml`.
3. Run the Ansible playbook:
    ```sh
    ansible-playbook playbook.yml
    ```
![Ansible Playbook](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/465bf33a-9618-48a1-bb72-38fb22b51c41)

## Jenkins Pipeline

This section provides detailed steps to set up and configure Jenkins for orchestrating an OpenShift deployment automation pipeline using a Jenkins shared library.

### Prerequisite

#### 1. Jenkins Shared Library

Contains reusable functions for the Jenkins pipeline:
- `checkoutRepo.groovy`: Checks out GitHub source code.
- `runUnitTests.groovy`: Runs unit test commands.
- `runSonarQubeAnalysis.groovy`: Runs SonarQube commands.
- `buildandPushDockerImage.groovy`: Builds Docker images and pushes them to DockerHub.
- `deployOnOpenShift.groovy`: Logs into the OpenShift cluster and deploys files.

#### 2. OpenShift Service Account

Create a service account for Jenkins with the necessary permissions to access the OpenShift cluster:
```sh
oc create sa <serviceaccount_name> -n <project_name>
oc create clusterrolebinding <rolebinding_name> --clusterrole=edit --serviceaccount=<project_name>:<serviceaccount_name>
oc serviceaccounts get-token <serviceaccount_name> -n <project_name>
```

#### 3. SonarQube Project

Create a SonarQube project and generate a secure user token.
![Screenshot 2024-06-13 032440](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/c88b3667-570c-47c8-92a6-a0e37eda05a4)

### Usage

1. **Set Jenkins Credentials**
    Configure Jenkins credentials for GitHub, DockerHub, SonarQube Token, and OpenShift Token.
   ![Screenshot 2024-06-13 013011](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/0f177111-3cdb-49aa-b162-4cfdd1a963cd)

3. **Make Shared Library Available Globally**
    Push the shared library file to a separate GitHub repository and configure it to be globally available in Jenkins.
4. **Manage SonarQube Plugin**
    Configure SonarQube settings in Jenkins.
5. **Open Jenkins and Create a New Pipeline**
6. **Update Variables in Jenkinsfile
Sure, here's the continuation and completion of the answer:

### Jenkins Pipeline

This section provides detailed steps to set up and configure Jenkins for orchestrating an OpenShift deployment automation pipeline using a Jenkins shared library.


#### Usage

1. **Set Jenkins Credentials**

   Configure Jenkins credentials for GitHub, DockerHub, SonarQube Token, and OpenShift Token.
   ![Jenkins Credentials](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/6922e404-e499-421f-be93-cf25fff587b8)

2. **Make Shared Library Available Globally**

   Push the shared library file to a separate GitHub repository and configure it to be globally available in Jenkins.

3. **Manage SonarQube Plugin**

   Configure SonarQube settings in Jenkins.

4. **Open Jenkins and Create a New Pipeline**

   Configure a new pipeline job in Jenkins using a `Jenkinsfile` from your repository.
   ![Jenkins Pipeline](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/cb085313-e9ba-4934-87b6-10a8137fe4f6)

5. **Update Variables in Jenkinsfile**

   Customize the `Jenkinsfile` by updating variables to match the specifics of your project and environment.

6. **Configure the Pipeline with the Jenkinsfile in Your Repository**

   Define the stages and tasks in your `Jenkinsfile` for building, testing, and deploying your application on OpenShift.

7. **Trigger the Pipeline**

   Initiate the execution of the pipeline in Jenkins. Monitor the pipeline output for build status, test results, and deployment logs.
   ![Jenkins Output](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/d9640734-8f9a-4fe9-91c8-e7fcd2d753b3)

### OpenShift Deployment

This section demonstrates the deployment of a Java web application on OpenShift, covering various aspects like deployment configurations, services, routes, and persistent volume claims for data persistence.

#### OpenShift Manifests

- **Deployment Configuration:** Defines the deployment configuration for the Java web application. (`openshift/deployment.yml`)
- **Service:** Exposes the application within the OpenShift cluster. (`openshift/service.yml`)
- **Route:** Exposes the application externally. (`openshift/route.yml`)

To verify that the application is running:
```sh
oc get all
```
![OpenShift Deployment](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/f56e3624-b1c1-46cc-b37e-155e1fdfcbf3)
![image](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/21d3a461-f534-4956-a6aa-0adc097faabe)

testing the app 


### Monitoring and Logging OpenShift Cluster

This section highlights the Logging Operator, a tool tailored for managing EFK (Elasticsearch, Fluentd, and Kibana) clusters in Kubernetes and OpenShift.

#### Setup Using Helm Tool

1. **Add the Helm Chart Repository**

   ```sh
   helm repo add ot-helm https://ot-container-kit.github.io/helm-charts/
   ```

2. **Deploy the Logging Operator**

   ```sh
   helm upgrade logging-operator ot-helm/logging-operator --install --namespace ot-operators
   ```

3. **Testing Operator**

   ```sh
   helm test logging-operator --namespace ot-operators
   ```

4. **List Pods and Status**

   ```sh
   oc get pods -n ot-operators -l name=logging-operator
   ```

#### Elasticsearch Setup

1. **Adding Helm Repository**

   ```sh
   helm repo add ot-helm https://ot-container-kit.github.io/helm-charts/
   ```

2. **Updating Helm Repository**

   ```sh
   helm repo update
   ```

3. **Install Elasticsearch Helm Chart**

   ```sh
   helm install elasticsearch ot-helm/elasticsearch --namespace ot-operators --set esMaster.storage.storageClass=do-block-storage --set esData.storage.storageClass=do-block-storage
   ```

4. **Verify Pod Status**

   ```sh
   oc get pods --namespace ot-operators -l 'role in (master,data,ingestion,client)'
   ```

5. **Verify Secret Value**

   ```sh
   oc get secrets -n ot-operators elasticsearch-password -o jsonpath="{.data.password}" | base64 -d
   ```

6. **List Elasticsearch Cluster**

   ```sh
   oc get elasticsearch -n ot-operators
   ```

These sections collectively provide a comprehensive guide for setting up a Multi-Cloud DevOps project, including provisioning infrastructure, configuring applications with Ansible, automating deployments with Jenkins pipelines, deploying applications on OpenShift, and managing monitoring/logging with the Logging Operator on OpenShift.
