from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct

class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env_name: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if env_name == "dev":
            self.vpc = ec2.Vpc(self, "devVPC", max_azs=1)
        elif env_name == "prod":
            self.vpc = ec2.Vpc(self, "prodVPC", max_azs=2)
        else:
            self.vpc = ec2.Vpc(self, "defaultVPC", max_azs=1)
        