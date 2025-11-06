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
class ProdStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # 1. Creating S3 bucket for the production environment
        self.prod_bucket = s3.Bucket(
            self,
            "ProdBucket",
            bucket_name="cdk-landing-zone-prod-bucket",
            removal_policy=RemovalPolicy.DESTROY, #DESTROY during Testing, RETAIN when project complete
            versioned=True,
            encryption=s3.BucketEncryption.KMS_MANAGED, # SSE-KMS
        )

        # 2. Creating a role to be applied to the EC2 instance
        self.instance_role = iam.Role(
            self,
            "ProdInstanceRole",
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
                resources=[self.prod_bucket.arn_for_objects("*")],
            )
        )

        # ----------------------
        # 3. Creating multiple EC2 instances below
        # ----------------------        

        # Retrieving subnets created within PROD VPC from network stack - EC2 instances can be created in each
        private_subnets = vpc.select_subnets(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS).subnets

        # 3.1 Creating the first EC2 instance, to be placed in first private subnet
        self.prod_instance_1 = ec2.Instance(
            self,
            "ProdInstance1",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=[private_subnets[0]]),
            role=self.instance_role,
        )

        # 3.2 Creating the second EC2 instance, to be placed in second private subnet for higher availability
        self.prod_instance_2 = ec2.Instance(
            self,
            "ProdInstance2",
            instance_type=ec2.InstanceType("t3.micro"),
            machine_image=ec2.MachineImage.latest_amazon_linux2(),
            vpc=vpc,
            vpc_subnets=ec2.SubnetSelection(subnets=[private_subnets[1]]),
            role=self.instance_role,
        )

        #4 Output the resources deployed from this stack
        self.output_arns()
    
    def output_arns(self):  
        CfnOutput(self, "ProdBucketName", value=self.prod_bucket.bucket_name)
        CfnOutput(self, "ProdInstance1Id", value=self.prod_instance_1.instance_id)
        CfnOutput(self, "ProdInstance2Id", value=self.prod_instance_2.instance_id)        
