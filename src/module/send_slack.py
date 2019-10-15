#!/usr/local/bin/python3
# coding: utf-8

import os
from slackclient import SlackClient

slack_token = os.getenv("SLACK_TOKEN")
client = SlackClient(slack_token)
