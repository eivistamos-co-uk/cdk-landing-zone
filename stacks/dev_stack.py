from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct

class DevStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # S3 Bucket
        self.dev_bucket = s3.Bucket(
            self,
            "DevBucket",
            bucket_name="cdk-landing-zone-dev-bucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # IAM Role
        self.dev_role = iam.Role(
            self,
            "DevRole",
            assumed_by=iam.AccountRootPrincipal(),
            role_name="DevEnvironmentRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            ],
        )

        # Optional EC2
        self.dev_instance = ec2.Instance(
            self,
            "DevInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
        )

        # Outputs
        CfnOutput(self, "DevBucketName", value=self.dev_bucket.bucket_name)
        CfnOutput(self, "DevRoleARN", value=self.dev_role.role_arn)
        CfnOutput(self, "DevInstanceId", value=self.dev_instance.instance_id)
