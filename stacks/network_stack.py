from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput,
)
from constructs import Construct

class NetworkStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # ---------------------
        # DEV VPC (Single AZ)
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

        # ---------------------
        # PROD VPC (Multi-AZ)
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

        # ---------------------
        # Outputs (optional)
        # ---------------------
        CfnOutput(self, "DevVpcId", value=self.dev_vpc.vpc_id)
        CfnOutput(self, "ProdVpcId", value=self.prod_vpc.vpc_id)
