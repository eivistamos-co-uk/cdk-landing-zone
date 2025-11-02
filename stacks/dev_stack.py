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

class DevStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        account_id = Stack.of(self).account

        # S3 Bucket
        self.dev_bucket = s3.Bucket(
            self,
            "DevBucket",
            bucket_name="cdk-landing-zone-dev-bucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        self.instance_role = iam.Role(
            self,
            "DevInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            role_name=f"{construct_id}-InstanceRole",
        )

        self.instance_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                ],
                resources=[self.dev_bucket.arn_for_objects("*")],
            )
        )

        # EC2 Instance
        self.dev_instance = ec2.Instance(
            self,
            "DevInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            role=self.instance_role,
        )


        # Outputs
        CfnOutput(self, "DevBucketName", value=self.dev_bucket.bucket_name)
        CfnOutput(self, "DevInstanceId", value=self.dev_instance.instance_id)
