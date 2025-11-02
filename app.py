#!/usr/bin/env python3
from aws_cdk import (
    App,
    Stack,
)

from constructs import Construct

from stacks.core_stack import CoreStack
from stacks.network_stack import NetworkStack
from stacks.dev_stack import DevStack
from stacks.prod_stack import ProdStack

app = App()
stack = Stack()

# Account ID and Region
env = {
    "account": "149536475647", 
    "region": "eu-west-2"
    }

class RootStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Core Stack: Central services (logging, sns, kms)
        core_stack = CoreStack(self, "CoreStack") 

        # Network Stack: Isolated environments (dev, prod VPCs)
        network_stack = NetworkStack(self, "NetworkStack")

        # Dev Stack: Dev environment (bucket, role, instance)
        dev_stack = DevStack(self, "DevStack", vpc=network_stack.dev_vpc)

        # Prod Stack: Prod environment (bucket, role, instance)
        prod_stack = ProdStack(self, "ProdStack", vpc=network_stack.prod_vpc)

RootStack(app, "LandingZoneRoot", env=env)
app.synth()
