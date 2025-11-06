from aws_cdk import (
    NestedStack,
    aws_ec2 as ec2,
    CfnOutput,
    Tags,
)
from constructs import Construct

# Defining this stack as a nested stack
class NetworkStack(NestedStack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ---------------------
        # 1. DEV VPC (Single AZ) - Creating an isolated dev network within a single availability zone
        # ---------------------
        self.dev_vpc = ec2.Vpc(
            self,
            "DevVPC",
            vpc_name="DevVPC",
            max_azs=1,
            ip_addresses=ec2.IpAddresses.cidr("10.10.0.0/16"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
            ],
        )

        # 1.1 Tagging DEV VPC resources
        Tags.of(self.dev_vpc).add("Environment", "Dev")

        # ---------------------
        # 2. PROD VPC (Multi-AZ) - Creating an isolated production network within multiple availability zones for higher availability
        # ---------------------
        self.prod_vpc = ec2.Vpc(
            self,
            "ProdVPC",
            vpc_name="ProdVPC",
            max_azs=2,
            ip_addresses=ec2.IpAddresses.cidr("10.20.0.0/16"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="PublicSubnet",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
                ec2.SubnetConfiguration(
                    name="PrivateSubnet",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                ),
            ],
        )

        # 2.1 Tagging PROD VPC resources
        Tags.of(self.prod_vpc).add("Environment", "Prod")

        #3 Output the resources deployed from this stack
        self.output_arns()
    
    def output_arns(self):  
        CfnOutput(self, "DevVpcId", value=self.dev_vpc.vpc_id)
        CfnOutput(self, "ProdVpcId", value=self.prod_vpc.vpc_id)
