from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_iam as iam,
    CfnOutput,
)
from constructs import Construct


class StaticWebsiteStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        bucket_name = f'static-website-{self.region}-{self.account}'

        # 1. Private S3 bucket
        website_bucket = s3.Bucket(self, "WebsiteBucket",
            bucket_name=bucket_name,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            encryption=s3.BucketEncryption.S3_MANAGED,
            versioned=True
        )

        # 2. CloudFront Origin Access Control
        oac = cloudfront.CfnOriginAccessControl(self, "WebsiteOAC",
            origin_access_control_config=cloudfront.CfnOriginAccessControl.OriginAccessControlConfigProperty(
                name="WebsiteOAC",
                description="OAC for private S3 website bucket",
                origin_access_control_origin_type="s3",
                signing_behavior="always",
                signing_protocol="sigv4"
            )
        )

        # 3. CloudFront Distribution with Geo Restriction
        distribution = cloudfront.CfnDistribution(self, "CloudFrontDistribution",
            distribution_config=cloudfront.CfnDistribution.DistributionConfigProperty(
                enabled=True,
                default_root_object="index.html",
                price_class="PriceClass_100",  # US, Europe, Japan
                http_version="http2",
                origins=[
                    cloudfront.CfnDistribution.OriginProperty(
                        id="S3Origin",
                        domain_name=website_bucket.bucket_regional_domain_name,
                        s3_origin_config=cloudfront.CfnDistribution.S3OriginConfigProperty(
                            origin_access_identity=""
                        ),
                        origin_access_control_id=oac.ref
                    )
                ],
                default_cache_behavior=cloudfront.CfnDistribution.DefaultCacheBehaviorProperty(
                    target_origin_id="S3Origin",
                    viewer_protocol_policy="redirect-to-https",
                    allowed_methods=["GET", "HEAD"],
                    cached_methods=["GET", "HEAD"],
                    compress=True,
                    forwarded_values=cloudfront.CfnDistribution.ForwardedValuesProperty(
                        query_string=False,
                        cookies=cloudfront.CfnDistribution.CookiesProperty(forward="none")
                    )
                ),
                viewer_certificate=cloudfront.CfnDistribution.ViewerCertificateProperty(
                    cloud_front_default_certificate=True
                ),
                restrictions=cloudfront.CfnDistribution.RestrictionsProperty(
                    geo_restriction=cloudfront.CfnDistribution.GeoRestrictionProperty(
                        restriction_type="whitelist",
                        locations=[
                            "US", "JP", "DE", "FR", "IT", "ES", "GB", "NL", "SE", "CH"
                        ]
                    )
                )
            )
        )

        # 4. S3 Bucket Policy to allow CloudFront OAC to read
        website_bucket.add_to_resource_policy(iam.PolicyStatement(
            sid="AllowCloudFrontServicePrincipalReadOnly",
            actions=["s3:GetObject"],
            resources=[f"{website_bucket.bucket_arn}/*"],
            principals=[iam.ServicePrincipal("cloudfront.amazonaws.com")],
            conditions={
                "StringEquals": {
                    "AWS:SourceArn": f"arn:aws:cloudfront::{self.account}:distribution/{distribution.ref}"
                }
            }
        ))

        # 5. Outputs
        CfnOutput(self, "WebsiteURL",
            description="CloudFront Distribution URL",
            value=f"https://{distribution.attr_domain_name}"
        )

        CfnOutput(self, "S3BucketName",
            description="Private S3 Bucket Name",
            value=website_bucket.bucket_name
        )
