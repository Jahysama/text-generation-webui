from loguru import logger
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json


class Dict2Args(object):

    def __init__(self, json_path: str, json_merge: str = None):
        with open(json_path, 'r') as config_file:
            dict1 = json.load(config_file)
        if json_merge:
            with open(json_merge, 'r') as config_file:
                dict2 = json.load(config_file)
            dict1.update(dict2)
        for key in dict1:
            setattr(self, key, dict1[key])


config = Dict2Args('configs/slack_config.json')

slack_token = config.slack_token
channel = config.channel
client = WebClient(token=slack_token)


def send_notification_to_slack(type: str, message: str, prompt=None):
    try:
        if prompt:
            prompt = f'Error Explanation: `{prompt}`'
        else:
            prompt = ""
        response = client.chat_postMessage(
            channel=channel,
            text=f"{prompt}\n"
                 f"*{type}:*"
                 "```"
                 f"{message}"
                 "```"
        )
    except SlackApiError as e:
        logger.error(e.response["error"])
