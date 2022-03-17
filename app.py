#!/usr/bin/env python3

import json

from aws_cdk.core import Environment, Tags, App
from infra.pipeline_stack import PipelineStack

app = App()

with open('./tags.json', 'r') as file:
    tags = json.loads(file.read())

for key, value in tags.items():
    Tags.of(app).add(key, value)

codeaccount = app.node.try_get_context("codeaccount")
infraaccount = app.node.try_get_context("infraaccount")

ENV_CODE = Environment(account=codeaccount, region="us-east-1") # Account for Code Pipelines
ENV_APP = Environment(account=infraaccount, region="us-east-1") # Account for Infrastucture

app = App()

# Deploys a new pipeline into the shared Codecommit account
PipelineStack(app, "githubtrigger","pipeline","Sandbox",ENV_APP, env=ENV_CODE)

with open('./tags.json', 'r') as file:
    tags = json.loads(file.read())

for key, value in tags.items():
    Tags.of(app).add(key, value)

app.synth()
