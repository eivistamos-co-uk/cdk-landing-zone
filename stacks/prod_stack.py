from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct


class ProdStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ---------------------------
        # S3 Bucket (Prod)
        # ---------------------------
        self.prod_bucket = s3.Bucket(
            self,
            "ProdBucket",
            bucket_name="cdk-mini-prod-bucket",
            removal_policy=RemovalPolicy.RETAIN,
            versioned=True,  # keep versions in prod
        )

        # ---------------------------
        # IAM Role (Prod Environment Scoped)
        # ---------------------------
        self.prod_role = iam.Role(
            self,
            "ProdRole",
            assumed_by=iam.AccountRootPrincipal(),  # replace with proper user/role
            role_name="ProdEnvironmentRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            ],
        )

        # ---------------------------
        # Optional EC2 (Prod)
        # ---------------------------
        self.prod_instance = ec2.Instance(
            self,
            "ProdInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
        )

        # ---------------------------
        # Outputs
        # ---------------------------
        CfnOutput(self, "ProdBucketName", value=self.prod_bucket.bucket_name)
        CfnOutput(self, "ProdRoleARN", value=self.prod_role.role_arn)
        CfnOutput(self, "ProdInstanceId", value=self.prod_instance.instance_id)
