#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.core_stack import CoreStack
from stacks.network_stack import NetworkStack
from stacks.dev_stack import DevStack
from stacks.prod_stack import ProdStack

app = cdk.App()

env = {"account": "149536475647", "region": "eu-west-2"}

core_stack = CoreStack(app, "CoreStack", env=env)
network_stack = NetworkStack(app, "NetworkStack", env=env)
dev_stack = DevStack(app, "DevStack", vpc=network_stack.dev_vpc, env=env)
prod_stack = ProdStack(app, "ProdStack", vpc=network_stack.prod_vpc, env=env)

app.synth()
