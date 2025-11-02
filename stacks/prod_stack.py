from aws_cdk import (
    Stack,
    NestedStack,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct

class ProdStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # S3 Bucket
        self.prod_bucket = s3.Bucket(
            self,
            "ProdBucket",
            bucket_name="cdk-landing-zone-prod-bucket",
            removal_policy=RemovalPolicy.RETAIN, #DESTROY during Testing, RETAIN when project complete!
            versioned=True,
        )

        # IAM Role
        self.prod_role = iam.Role(
            self,
            "ProdRole",
            assumed_by=iam.AccountRootPrincipal(),
            role_name="ProdEnvironmentRole",
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"),
            ],
        )

        # Optional EC2
        self.prod_instance = ec2.Instance(
            self,
            "ProdInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
        )

        # Outputs
        CfnOutput(self, "ProdBucketName", value=self.prod_bucket.bucket_name)
        CfnOutput(self, "ProdRoleARN", value=self.prod_role.role_arn)
        CfnOutput(self, "ProdInstanceId", value=self.prod_instance.instance_id)
