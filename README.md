# AWS Static Website Hosting using S3 and CloudFront

This project demonstrates how to host a secure and globally available static website using AWS services like S3, CloudFront, and IAM policies—all deployed via AWS CDK (Infrastructure as Code).
### Main Architecture Diagram
![!\[alt text\](<Architecture-Task-1 Full Implementation.drawio.png>)](<Architecture-Task-1 Full Implementation.drawio.png>)

## 📌 Task 1: Private S3 Static Website Hosting

### ✅ Objective

- Host static website assets (HTML, CSS, JS) in a **private** S3 bucket.
- **Restrict public access** to the bucket.
- Use OAC (Origin Access Control) for secure access via CloudFront.

### ✅ AWS Resources Deployed

- `AWS::S3::Bucket` – Website storage
- `AWS::S3::BucketPolicy` – Deny public access
- `AWS::CloudFront::OriginAccessControl` – Allow CloudFront-only access
- `CDKMetadata` – CDK tracking metadata

### Methodology
- Deployed phase wise deployment of resources for testing and debugging purposes.


### 📸 Screenshots

## 📌 Task 2: Backend - ALB + Lambda

### ✅ Objective

- Create a **CloudFront Distribution** as a secure and globally available entry point.
- Add an **Application Load Balancer** in front of a **Lambda function**.
- Simulate a **payment approval backend** using a Lambda function triggered via ALB.

### ✅ AWS Resources Deployed

- `AWS::CloudFront::Distribution` – CDN for global content delivery
- `AWS::ElasticLoadBalancingV2::LoadBalancer` – ALB to trigger Lambda
- `AWS::ElasticLoadBalancingV2::Listener` – HTTP listener on port 80
- `AWS::ElasticLoadBalancingV2::TargetGroup` – Lambda integration
- `AWS::Lambda::Function` – Simulated payment approval backend
- `AWS::Lambda::Permission` – Allow invocation by ALB
- `AWS::EC2::SecurityGroup` – ALB access control

### 🧪 Methodology

#### ✅ Phase 1: Creating a Basic Functional Web Application
- Launched an EC2 instance to host a Node.js-based web application.
- Verified that the application was running and accessible via the instance's public IP.

#### ✅ Phase 2: Creating and Configuring the Amazon RDS Database
- Provisioned an Amazon RDS instance with MySQL engine.
- Configured security groups to allow secure access from the EC2 instance.
- Connected the web application to RDS using environment variables and verified database connectivity.

#### ✅ Phase 3: Provisioning a New Instance for the Web Server & Migrating the Database
- Created a new EC2 instance and replicated the application environment.
- Migrated the database connection to the RDS instance and ensured consistent application behavior.
- Applied proper IAM roles and security groups for the instance.

#### ✅ Phase 4: Implementing High Availability and Scalability
- Created an Application Load Balancer (ALB) to distribute incoming traffic.
- Configured Auto Scaling Group with a custom AMI containing the application.
- Ensured the setup used multiple Availability Zones for high availability.
- Verified ALB integration and automatic scaling based on CPU utilization.



