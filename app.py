#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.core_stack import CoreStack
from stacks.network_stack import NetworkStack
from stacks.dev_stack import DevStack
from stacks.prod_stack import ProdStack

app = cdk.App()

# Core shared services

core = CoreStack(app, "CoreStack")
network_stack = NetworkStack(app, "NetworkStack")

app.synth()
