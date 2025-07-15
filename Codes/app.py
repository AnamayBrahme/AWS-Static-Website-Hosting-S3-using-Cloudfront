#!/usr/bin/env python3
import os

import aws_cdk as cdk
from iactemp.task1 import StaticWebsiteStack
from iactemp.task2 import Task2Stack


app = cdk.App()
StaticWebsiteStack(app, "StaticWebsiteStack")
Task2Stack(app, "Task2Stack")
#Task2Stack(app, "Task2Stack")


app.synth()
