#!/usr/bin/env python3
import aws_cdk as cdk
from stacks.core_stack import CoreStack
from stacks.network_stack import NetworkStack
from stacks.dev_stack import DevStack
from stacks.prod_stack import ProdStack

app = cdk.App()

# Core shared services

core = CoreStack(app, "CoreStack")

# Network per environment

dev_network = NetworkStack(app, "DevNetworkStack", env_name="dev")
prod_network = NetworkStack(app, "ProdNetworkStack", env_name="prod")

# Environment resources

dev = DevStack(app, "DevStack",
               vpc=dev_network.vpc,
               core_resources=core,
               env_name="dev")

prod = ProdStack(app, "ProdStack",
                 vpc=prod_network.vpc,
                 core_resources=core,
                 env_name="prod")

app.synth()
