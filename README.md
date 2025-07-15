# AWS Static Website Hosting using S3 and CloudFront

This project demonstrates how to host a secure and globally available static website using AWS services like S3, CloudFront, and IAM policies—all deployed via AWS CDK (Infrastructure as Code).
### Main Architecture Diagram

<img width="1012" height="771" alt="Architecture-Task-1 Full Implementation drawio" src="https://github.com/user-attachments/assets/40ff7d92-4568-4963-851f-7f66a6ffa149" />

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


