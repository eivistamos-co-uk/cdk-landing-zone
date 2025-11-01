from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    CfnOutput,
)
from constructs import Construct

class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # ---------------------
        # DEV VPC (Single AZ)
        # 1 AZ:
        # 1 Public Subnet (for Bastions, ALBs, NAT Gateways)
        # 1 Private Subnet (with outbound-only Internet access)
        # ---------------------
        self.dev_vpc = ec2.Vpc(
            self,
            "DevVPC",
            vpc_name="DevVPC",
            max_azs=1, #single AZ
            cidr="10.10.0.0/16",
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
        # 2 AZs:
        # 2 Public Subnets (for Bastions, ALBs, NAT Gateways)
        # 2 Private Subnets (with outbound-only Internet access)
        # ---------------------
        self.prod_vpc = ec2.Vpc(
            self,
            "ProdVPC",
            vpc_name="ProdVPC",
            max_azs=2, #multi-AZ for HA
            cidr="10.20.0.0/16",
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
        # Outputs (for cross-stack reference)
        # ---------------------
        self._add_outputs()

    def _add_outputs(self):
        # Dev VPC
        CfnOutput(self, "DevVpcId", value=self.dev_vpc.vpc_id, export_name="DevVpcId")
        CfnOutput(self, "DevPublicSubnets", value=",".join([subnet.subnet_id for subnet in self.dev_vpc.public_subnets]))
        CfnOutput(self, "DevPrivateSubnets", value=",".join([subnet.subnet_id for subnet in self.dev_vpc.private_subnets]))

        # Prod VPC
        CfnOutput(self, "ProdVpcId", value=self.prod_vpc.vpc_id, export_name="ProdVpcId")
        CfnOutput(self, "ProdPublicSubnets", value=",".join([subnet.subnet_id for subnet in self.prod_vpc.public_subnets]))
        CfnOutput(self, "ProdPrivateSubnets", value=",".join([subnet.subnet_id for subnet in self.prod_vpc.private_subnets]))