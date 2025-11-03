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

        # Get private subnets in the VPC
        private_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnets

        # First EC2 instance in first private subnet
        self.prod_instance_1 = ec2.Instance(
            self,
            "ProdInstance1",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=[private_subnets[0]]),
            role=self.instance_role,
        )

        # Second EC2 instance in second private subnet (high availability)
        self.prod_instance_2 = ec2.Instance(
            self,
            "ProdInstance2",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=[private_subnets[1]]),
            role=self.instance_role,
        )

        # Outputs
        CfnOutput(self, "ProdBucketName", value=self.prod_bucket.bucket_name)
        CfnOutput(self, "ProdInstance1Id", value=self.prod_instance_1.instance_id)
        CfnOutput(self, "ProdInstance2Id", value=self.prod_instance_2.instance_id)        
