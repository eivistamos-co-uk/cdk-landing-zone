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

        account_id = Stack.of(self).account

        # S3 Bucket
        self.prod_bucket = s3.Bucket(
            self,
            "ProdBucket",
            bucket_name="cdk-landing-zone-prod-bucket",
            removal_policy=RemovalPolicy.DESTROY, #DESTROY during Testing, RETAIN when project complete!
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED, # SSE-KMS
        )

        self.instance_role = iam.Role(
            self,
            "ProdInstanceRole",
            assumed_by=iam.ServicePrincipal("ec2.amazonaws.com"),
            role_name=f"{construct_id}-InstanceRole",
        )

        self.instance_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "s3:GetObject",
                    "s3:PutObject",
                ],
                resources=[self.prod_bucket.arn_for_objects("*")],
            )
        )

        #EC2 Instance
        self.prod_instance = ec2.Instance(
            self,
            "ProdInstance",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            role=self.instance_role,
        )

        # Outputs
        CfnOutput(self, "ProdBucketName", value=self.prod_bucket.bucket_name)
        CfnOutput(self, "ProdInstanceId", value=self.prod_instance.instance_id)
