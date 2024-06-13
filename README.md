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
- [infra.sh](#infrash)
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

### VPC Module:

- **Purpose:** Provision a Virtual Private Cloud (VPC) with internet gateway for public access.
- **Files:** `vpc/main.tf`, `vpc/variables.tf`, `vpc/outputs.tf`

### Subnet Module:

- **Purpose:** Define public subnet, route table.
- **Files:** `subnet/main.tf`, `subnet/variables.tf`, `subnet/outputs.tf`

### EC2 Module:

- **Purpose:** Create an EC2 instance with necessary security group.
- **Files:** `ec2/main.tf`, `ec2/variables.tf`, `ec2/outputs.tf`

### CloudWatch Module:

- **Purpose:** Set up CloudWatch resources for monitoring and SNS resources for sending emails for alarms.
- **Files:** `cloudwatch/main.tf`, `cloudwatch/variables.tf`, `cloudwatch/outputs.tf`

### Usage

1. Update values in `terraform.tfvars` file

    ```hcl
    region          = "us-east-1"
    vpc_cidr        = "10.0.0.0/16"
    subnet_cidr     = "10.0.0.0/24"
    availability_zone = "us-east-1a"
    public_key_path = "<path_to_file>"
    ec2_ami_id      = "ami-0abcdef1234567890"
    ec2_type        = "m5.large"
    sns_email       = "<your_email@example.com>"
    ```

2. Initialize and apply Terraform configurations:

    ```sh
    terraform init
    terraform apply
    ```

3. Follow on-screen prompts to provision infrastructure.

4. Destroy the infrastructure

    ```sh
    terraform destroy
    ```

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

1. Update `ansible_host` & `ansible_ssh_private_key_file` in `inventory.ini`.
2. Update `Jenkins admin credentials` in `ansible/roles/jenkins/vars/main.yml`.
3. Run Ansible playbook

    ```sh
    ansible-playbook -i inventory.ini playbook.yml
    ```

## infra.sh

This Bash script is designed to streamline the setup of the project's infrastructure. It executes `Terraform` commands, updates the `ansible_host` in the `inventory.ini` file with EC2 public IP, and finally runs the Ansible playbook on the EC2 instance.

### Usage

1. Update Terraform and Ansible directories paths in `infra.sh`

    ```sh
    vim infra.sh
    ```

2. Make script executable

    ```sh
    chmod +x infra.sh
    ```

3. Run script

    ```sh
    ./infra.sh
    ```

## OpenShift Deployment

This document demonstrates the deployment of a Java web application on OpenShift. The orchestrated process includes setting up a deployment configuration for efficient scaling, establishing an internal service, implementing network policies for enhanced security, configuring routes for external access, and utilizing persistent volume claims to ensure data persistence and storage reliability.

### OpenShift Manifests

- **Deployment:** Define the deployment configuration for Java web-app. `openshift/deployment.yml`
- **Service:** Expose the application within the OpenShift cluster. `openshift/service.yml`
- **Network Policy:** Define network policies for secure communication. `openshift/networkpolicy.yml`
- **Route:** Expose the application externally. `openshift/route.yml`
- **Persistent Volume Claim (PVC):** Manage persistent storage for the application. `openshift/pvc.yml`

### Usage

1. Navigate to OpenShift directory

    ```sh
    cd OpenShift
    ```

2. Apply OpenShift deployment configurations

    ```sh
    oc apply -f .
    ```

3. Verify the deployment status

    ```sh
    oc get pods
    ```

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

    ```sh
    oc cluster-info
    ```

2. **Make Shared Library Available Globally**

    Push the shared library file to a separate GitHub repository and configure it to be globally available in Jenkins.

3. **Manage SonarQube Plugin**

    Configure SonarQube settings in Jenkins.

4. **Open Jenkins and Create a New Pipeline Job**

    Set up a new pipeline job in Jenkins.

5. **Update Variables in Jenkinsfile**

    Customize the

 Jenkinsfile by updating variables to match the specifics of your project and environment.

6. **Configure the Pipeline with the Jenkinsfile in Your Repository**

7. **Trigger the Pipeline**

    Initiate the execution of the pipeline in Jenkins.

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

References:

- [Logging Operator Overview](https://ot-logging-operator.netlify.app/docs/overview/)
- [Getting Started with Logging Operator](https://ot-logging-operator.netlify.app/docs/getting-started/installation/)
- [Elasticsearch Setup](https://ot-logging-operator.netlify.app/docs/getting-started/elasticsearch-setup/)
- [Elasticsearch Configuration](https://ot-logging-operator.netlify.app/docs/configuration/elasticsearch-config/)

By following these detailed steps, you will establish a comprehensive CI/CD pipeline integrating Jenkins, SonarQube, Docker, and OpenShift.
```
