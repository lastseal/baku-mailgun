# -*- coding: utf-8 -*

import requests
import logging
import klaviyo
import json
import os

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_KEY = os.getenv("MAILGUN_KEY")

def send(config, data=None):

    logging.info("sending mail to %s", config['to'])

    if 'template' in config:
        config["html"]=klaviyo.donwload(config['template'], data)

    elif data is not None and 'text' in config:
        config['text'] = config['text'].format(**data)
        logging.debug("%s", config['text'])

    res = requests.post(f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_KEY),
        data=config
    )

    if res.status_code >= 400:
        raise Exception(f"{res.status_code}: {res.text}")

    data = res.json()

    logging.debug("mailgun res: %s", data)

    return data['message']
