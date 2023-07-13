#!/usr/bin/env python3

import aws_cdk as cdk
import os

from main.main import Main


app = cdk.App()
dev = cdk.Environment(
    account=os.getenv("DEPLOY_AWS_ACCOUNT_ID"),
    region="eu-west-2",
)

Main(app, "cdk-cr-dependency-issue", env=dev)

app.synth()
