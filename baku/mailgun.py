# -*- coding: utf-8 -*

import requests
import logging
import json
import os

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_KEY = os.getenv("MAILGUN_KEY")

KLAVIYO_TEMPLATE_ID = os.getenv("KLAVIYO_TEMPLATE_ID")
KLAVIYO_API_KEY = os.getenv("KLAVIYO_API_KEY")

##
#

def send(config, data=None):

    logging.info("sending mail to %s", config['to'])

    if data is not None and 'template' in config:
        url = f"https://a.klaviyo.com/api/v1/email-template/{KLAVIYO_TEMPLATE_ID}/render?api_key={KLAVIYO_API_KEY}"
        res = requests.post(url, data=data, headers={
            "accept": "application/json",
            "content-type": "application/x-www-form-urlencoded"
        })
        
        if res.status_code >= 400:
            raise Exception(f"{res.status_code}: {res.text}")
        
        config["html"]=res.text

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
