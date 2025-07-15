from aws_cdk import (
    Stack,
    Duration,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2,
    aws_elasticloadbalancingv2_targets as targets,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct


class Task2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # VPC (10.0.0.0/16 with 2 public subnets)
        vpc = ec2.Vpc(
            self, "Task2VPC",
            ip_addresses=ec2.IpAddresses.cidr("10.0.0.0/16"),
            max_azs=2,
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24
                )
            ],
            nat_gateways=0,
            restrict_default_security_group=False
        )
        
        lambda_role = iam.Role.from_role_arn(
            self, "ImportedLambdaRole",
            role_arn="arn:aws:iam::528316341503:role/LabRole",
            mutable=False  # set to True if you plan to modify the role with CDK
        )

        # Lambda Function
        bucket = s3.Bucket.from_bucket_name(self, "LambdaBucket", "task2-lambda-bucket-s3")

        # Lambda Function using code from S3 bucket
        payment_lambda = _lambda.Function(
            self, "PaymentLambda",
            runtime=_lambda.Runtime.PYTHON_3_11,
            handler="payment_handler.lambda_handler",
            code=_lambda.Code.from_bucket(bucket, "lambda-code.zip"),
            timeout=Duration.seconds(10),
            role=lambda_role
        )

        # Security Group for ALB
        alb_sg = ec2.SecurityGroup(
            self, "ALBSecurityGroup",
            vpc=vpc,
            description="Allow HTTP traffic",
            allow_all_outbound=True
        )

        alb_sg.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow HTTP traffic from anywhere"
        )

        # Application Load Balancer
        alb = elbv2.ApplicationLoadBalancer(
            self, "PaymentALB",
            vpc=vpc,
            internet_facing=True,
            security_group=alb_sg,
            vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PUBLIC)
        )

        # Listener on port 80
        listener = alb.add_listener(
            "Listener",
            port=80,
            open=True
        )

        # Target: Lambda function
        lambda_target = targets.LambdaTarget(payment_lambda)

        # Add Lambda target to listener
        listener.add_targets(
            "LambdaTargetGroup",
            targets=[lambda_target],
            health_check=elbv2.HealthCheck(
                enabled=True,
                healthy_http_codes="200"
            )
        )

        # Permission: Allow ALB to invoke Lambda
        payment_lambda.add_permission(
            "AllowALBInvoke",
            principal=iam.ServicePrincipal("elasticloadbalancing.amazonaws.com"),
            action="lambda:InvokeFunction",
            source_arn=listener.listener_arn
        )

        # Output the ALB DNS for testing
        CfnOutput(
            self, "ALBUrl",
            value=f"http://{alb.load_balancer_dns_name}",
            description="Public URL to access the Lambda behind ALB"
        )
