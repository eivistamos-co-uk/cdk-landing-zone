#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.core_stack import CoreStack
from stacks.network_stack import NetworkStack
from stacks.dev_stack import DevStack
from stacks.prod_stack import ProdStack

app = cdk.App()

# Core + Network
core_stack = CoreStack(app, "CoreStack")
network_stack = NetworkStack(app, "NetworkStack")

# Environment Stacks
dev_stack = DevStack(
    app,
    "DevStack",
    vpc_id=network_stack.dev_vpc,
    env={"account": "149536475647", "region": "eu-west-2"},  # adjust account/region
)

prod_stack = ProdStack(
    app,
    "ProdStack",
    vpc_id=network_stack.prod_vpc,
    env={"account": "149536475647", "region": "eu-west-2"},
)

app.synth()
