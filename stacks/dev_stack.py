from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
)
from constructs import Construct

class DevStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc, core_resources, env_name, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkLandingZoneQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )