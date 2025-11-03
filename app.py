#!/usr/bin/env python3
from aws_cdk import (
    App,
    Stack,
    Tags,
)

from constructs import Construct

from stacks.core_stack import CoreStack
from stacks.network_stack import NetworkStack
from stacks.dev_stack import DevStack
from stacks.prod_stack import ProdStack

app = App()

# ----------------------
# DEFINE VARIABLES BELOW
# ----------------------

env = {
    "account": "149536475647", 
    "region": "eu-west-2"
    }
owner = "Eivis"
project_name = "CDKLandingZone"

class RootStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        # Tag all project resources with the following:
        Tags.of(app).add("Owner", owner)
        Tags.of(app).add("Project", project_name)

        # Core Stack: Central services (logging, sns, kms)
        core_stack = CoreStack(self, "CoreStack")
        Tags.of(core_stack).add("Environment", "Core") 

        # Network Stack: Isolated environments (dev, prod VPCs)
        network_stack = NetworkStack(self, "NetworkStack")
        Tags.of(network_stack).add("Environment", "Network") 

        # Dev Stack: Dev environment (bucket, role, instance)
        dev_stack = DevStack(self, "DevStack", vpc=network_stack.dev_vpc)
        Tags.of(dev_stack).add("Environment", "Dev") 

        # Prod Stack: Prod environment (bucket, role, instance)
        prod_stack = ProdStack(self, "ProdStack", vpc=network_stack.prod_vpc)
        Tags.of(prod_stack).add("Environment", "Prod") 

RootStack(app, "LandingZoneRoot", env=env)
app.synth()
