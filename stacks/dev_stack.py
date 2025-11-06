from aws_cdk import (
    NestedStack,
    aws_s3 as s3,
    aws_ec2 as ec2,
    aws_iam as iam,
    CfnOutput,
    RemovalPolicy,
)
from constructs import Construct

# Defining this stack as a nested stack
class DevStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 1. Creating S3 bucket for the developers
        self.dev_bucket = s3.Bucket(
            self,
            "DevBucket",
            bucket_name="cdk-landing-zone-dev-bucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # 2. Creating a role to be applied to the EC2 instance
        self.instance_role = iam.Role(
            self,
            "DevInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            role_name=f"{construct_id}-InstanceRole",
        )

        # 2.1 Creating a custom permissions policy to be applied to the EC2 instance role. Allowing some S3 actions
        self.instance_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                ],
                resources=[self.dev_bucket.arn_for_objects("*")],
            )
        )

        # 2.2 Creating the EC2 instance to be added to the Private Subnet of the Dev network (VPC)
        self.dev_instance = ec2.Instance(
            self,
            "DevInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            role=self.instance_role,
        )

        #6 Output some of the resources deployed from this stack
        self.output_arns()
    
    def output_arns(self):        
        CfnOutput(self, "DevBucketName", value=self.dev_bucket.bucket_name)
        CfnOutput(self, "DevInstanceId", value=self.dev_instance.instance_id)
