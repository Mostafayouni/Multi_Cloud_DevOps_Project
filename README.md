<h1>Mult-Cloud-Devops-Project</h1>
```markdown
# OpenShift Deployment Automation with Jenkins

Comprehensive documentation for deploying a Java web app on OpenShift using Terraform, Ansible, Jenkins, and more.

**Tools:** Bash scripting, Git, SonarQube, Docker, Terraform, AWS, Ansible, Jenkins, and OpenShift.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Manual Testing, Building, and Running Procedures](#manual-testing-building-and-running-procedures)
- [Infrastructure Provisioning with Terraform](#infrastructure-provisioning-with-terraform)
- [Ansible Playbook for Configuration](#ansible-playbook-for-configuration)
- [OpenShift Deployment](#openshift-deployment)
- [Jenkins Pipeline](#jenkins-pipeline)
- [Monitoring and Logging OpenShift Cluster](#monitoring-and-logging-openshift-cluster)

## Prerequisites

Before you begin, ensure you have the following tools installed:

- Terraform
- Ansible
- OpenShift CLI ('oc')

## Manual Testing, Building, and Running Procedures

This document provides a comprehensive guide outlining the manual steps before automating the process.

### 1. Execute Unit Tests

```sh
./gradlew test
```
![1](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/e1908ef1-a5a7-4228-a2fa-4152bdaaef61)

Access Test Results:

Navigate to the following path and open the `index.html` file:

```sh
cd build/reports/tests/test/
```
![2](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/8fb82928-67da-4922-bdca-abf93edfdcee)

### 2. Perform SonarQube Analysis

Prerequisites:

Ensure SonarQube project is configured with the necessary project key and login token.

```sh
./gradlew sonar \
-Dsonar.projectKey=<project_key> \
-Dsonar.host.url=<host_server_url> \
-Dsonar.login=<login_token> \
```
![4-sonar](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/ad77cfa2-58ea-4035-8c20-5b97dd965c36)

### 3. Build and Run Application

Build Application:

```sh
./gradlew build --stacktrace
```
![5build](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/4d6fd6e6-f3db-450f-ba4f-c3ef880b18f0)

Run Application:

```sh
java -jar demo.jar
```
![44](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/f4256106-e0b5-440a-a2d5-686e14d5631d)

Access Application Locally:

Visit `http://localhost:8081`

![6-test build jar](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/16975e1d-fbd5-43d4-9241-521aee03db58)

### 4. Build Docker Image and Run Container

Build Docker Image:

```sh
docker build -t <image_name> .
```
![7-docker build -exec -test image](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/e571948d-98fc-4f9e-8fec-a2bad148b1d4)

Run Docker Container:

```sh
docker run --name=<container_name> -d -p 8081:8081 <image_name>
```
![7-docker image name ](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/54b66cbd-213a-44bf-a41c-d286f97dd1f3)

## Infrastructure Provisioning with Terraform

This document provides comprehensive instructions for deploying infrastructure using Terraform. The project encompasses four modules: vpc, subnet, ec2, and cloudwatch. The objective is to establish an environment comprising network infrastructure with subnet and Internet Gateway, an EC2 instance for running Jenkins and SonarQube, and CloudWatch for monitoring with alarms sent via SNS.

### Overview

- **main.tf:** Configure and define the cloud provider, call Terraform modules.
- **variables.tf:** Set variables that need to be defined in `terraform.tfvars` file.
- **terraform.tfvars:** Define values for the needed variables.
- **Remote Backend:** Store Terraform state remotely using S3 and DynamoDB.
- ![image](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/028a4a29-6abd-443c-8d66-2e70dae1e319)

![image](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/39479a91-a171-4424-8efd-5bab1d6eda3a)


### VPC Module:

- **Purpose:** Provision a Virtual Private Cloud (VPC) with internet gateway for public access.
- **Files:** `vpc/main.tf`, `vpc/variables.tf`, `vpc/outputs.tf`
![vpc](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/ed4a38d4-323f-4d61-affe-c87fb7df0977)

### Subnet Module:

- **Purpose:** Define public subnet, route table.
- **Files:** `subnet/main.tf`, `subnet/variables.tf`, `subnet/outputs.tf`
![subnet](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/6fef00e9-5941-4587-8736-c5b268ab284c)

### EC2 Module:

- **Purpose:** Create an EC2 instance with necessary security group.
- **Files:** `ec2/main.tf`, `ec2/variables.tf`, `ec2/outputs.tf`
![ec2-instance](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/d7672b74-3d90-416d-9899-f089b3e6306d)
### sequrity group:
monitor traffic from and to the instance
![security-group](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/bf00f36b-35ea-433c-943f-04aeadd9d301)

### CloudWatch Module:

- **Purpose:** Set up CloudWatch resources for monitoring and SNS resources for sending emails for alarms.
- **Files:** `cloudwatch/main.tf`, `cloudwatch/variables.tf`, `cloudwatch/outputs.tf`
![Screenshot 2024-06-13 001541](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/ce6136fa-5116-4843-9188-e0f07c4b1f49)

### Usage

1. Update values in `terraform.tfvars` file
   ```

2. Initialize and apply Terraform configurations:

    ```sh
    terraform init
    terraform apply
    ```
![image](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/9b7714e7-3ffd-4c57-95e7-8bc44ceb920a)

3. Follow on-screen prompts to provision infrastructure.

4. Destroy the infrastructure

    ```sh
    terraform destroy
    ```
![image](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/d072e2bb-f537-4d91-9bf8-81f2e7c08834)

## Ansible Playbook for Configuration

This document provides an overview of the Ansible playbook for installing and configuring Jenkins on an EC2 instance, along with additional roles for SonarQube, PostgreSQL, and Docker.

### Roles Structure and Details

- **Prerequisite Role:** Install required packages on the EC2 instance.
- **Postgres Role:** Install and configure PostgreSQL for SonarQube.
- **SonarQube Role:** Install and configure SonarQube on the EC2 instance.
- **Git Role:** Install Git on the EC2 instance.
- **Jenkins Role:** Install and configure Jenkins on the EC2 instance, including setting admin credentials and installing necessary plugins.
- **Docker Role:** Install and configure Docker on the EC2 instance.

### Usage

1. Using dynamic inventory to get ip of ec2 instance
        ```sh
      python3 dynamic_inv.py
    ```
2. Update `Jenkins admin credentials` in `ansible/roles/jenkins/vars/main.yml`.
3. Run Ansible playbook

    ```sh
    ansible-playbook  playbook.yml
    ```
![image](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/465bf33a-9618-48a1-bb72-38fb22b51c41)




## Jenkins Pipeline

This documentation provides detailed steps to set up and configure Jenkins for orchestrating an OpenShift deployment automation pipeline using Jenkins shared library. The setup includes configuring Jenkins credentials, making the Shared Library available globally, managing SonarQube integration, and creating a new pipeline job.

### Prerequisite

#### 1. Jenkins Shared Library

GitHub Repo files contain reusable functions for Jenkins pipeline:

- `checkoutRepo.groovy`: Check GitHub source code.
- `runUnitTests.groovy`: Run unit test command.
- `runSonarQubeAnalysis.groovy`: Run SonarQube command.
- `buildandPushDockerImage.groovy`: Build Docker image and push it to DockerHub.
- `deployOnOpenShift.groovy`: Login to OpenShift cluster and deploy files.

#### 2. OpenShift Service Account

Create a service account for Jenkins with the necessary permissions to access the OpenShift cluster for deployment process.

```sh
oc create sa <serviceaccount_name> -n <project_name>
oc create clusterrolebinding <rolebinding_name> --clusterrole=edit --serviceaccount=<project_name>:<serviceaccount_name>
oc get secrets -n <project_name> -o jsonpath='{.items[?(@.metadata.annotations.kubernetes\.io/service-account\.name=="<serviceaccount_name>")].data.token}' | base64 -d
```

#### 3. SonarQube Project

Create a SonarQube project and generate a secure user token.

### Usage

1. **Set Jenkins Credentials**

    Configure Jenkins credentials for GitHub, DockerHub, SonarQube Token, and OpenShift Token.
![Screenshot 2024-06-13 013011](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/6922e404-e499-421f-be93-cf25fff587b8)


2. **Make Shared Library Available Globally**

    Push the shared library file to a separate GitHub repository and configure it to be globally available in Jenkins.

3. **Manage SonarQube Plugin**

    Configure SonarQube settings in Jenkins.

4. **Open Jenkins and Create a New Pipeline**

    ![Screenshot 2024-06-13 014018](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/cb085313-e9ba-4934-87b6-10a8137fe4f6)


5. **Update Variables in Jenkinsfile**

    Customize the

 Jenkinsfile by updating variables to match the specifics of your project and environment.

6. **Configure the Pipeline with the Jenkinsfile in Your Repository**

7. **Trigger the Pipeline**

    Initiate the execution of the pipeline in Jenkins.
![jenkins output](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/d9640734-8f9a-4fe9-91c8-e7fcd2d753b3)
![sonar](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/5f9098b3-c4e6-4d69-8092-d0dc2a23fc8f)

## OpenShift Deployment

This document demonstrates the deployment of a Java web application on OpenShift. The orchestrated process includes setting up a deployment configuration for efficient scaling, establishing an internal service, implementing network policies for enhanced security, configuring routes for external access, and utilizing persistent volume claims to ensure data persistence and storage reliability.

### OpenShift Manifests

- **Deployment:** Define the deployment configuration for Java web-app. `openshift/deployment.yml`
- **Service:** Expose the application within the OpenShift cluster. `openshift/service.yml`
- **Route:** Expose the application externally. `openshift/route.yml`
  
### Usage
 ```sh
    oc get all
    ```
![image](https://github.com/Mostafayouni/Multi_Cloud_DevOps_project/assets/105316729/f56e3624-b1c1-46cc-b37e-155e1fdfcbf3)
to vaerify that the app running


## Monitoring and Logging OpenShift Cluster

This document highlights the Logging Operator, a Golang-based tool tailored for orchestrating EFK (Elasticsearch, Fluentd, and Kibana) clusters in Kubernetes and OpenShift. The operator efficiently manages individual components of the EFK stack, simplifying deployment and maintenance in containerized environments.

### Usage
 

#### Setup using Helm tool

1. Add the helm chart

    ```sh
    helm repo add ot-helm https://ot-container-kit.github.io/helm-charts/
    ```

2. Deploy the Logging Operator

    ```sh
    helm upgrade logging-operator ot-helm/logging-operator --install --namespace ot-operators
    ```

3. Testing Operator

    ```sh
    helm test logging-operator --namespace ot-operators
    ```

4. List the pod and status of logging-operator

    ```sh
    oc get pods -n ot-operators -l name=logging-operator
    ```

#### Elasticsearch Setup

1. Adding helm repository

    ```sh
    helm repo add ot-helm https://ot-container-kit.github.io/helm-charts/
    ```

2. Updating ot-helm repository

    ```sh
    helm repo update
    ```

3. Install the helm chart of Elasticsearch

    ```sh
    helm install elasticsearch ot-helm/elasticsearch --namespace ot-operators --set esMaster.storage.storageClass=do-block-storage --set esData.storage.storageClass=do-block-storage
    ```

4. Verify the status of the pods

    ```sh
    oc get pods --namespace ot-operators -l 'role in (master,data,ingestion,client)'
    ```

5. Verify the secret value

    ```sh
    oc get secrets -n ot-operators elasticsearch-password -o jsonpath="{.data.password}" | base64 -d
    ```

6. List Elasticsearch cluster

    ```sh
    oc get elasticsearch -n ot-operators
    ```


