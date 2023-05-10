# -*- coding: utf-8 -*

import requests
import logging
import json
import os

MAILGUN_DOMAIN = os.getenv("MAILGUN_DOMAIN")
MAILGUN_KEY = os.getenv("MAILGUN_KEY")
KLAVIYO_API_KEY = os.getenv("KLAVIYO_API_KEY")

##
#

def send(config, data=None):

    logging.info("sending mail to %s", config['to'])

    if data is not None and 'template' in config:
        url = f"https://a.klaviyo.com/api/template-render/
        
        payload = {
            "data": {
                "id": config["template"],
                "type": "template",
                "attributes": {"context": data}
            }
        }
        
        headers = {
            "accept": "application/json",
            "revision": "2023-02-22",
            "content-type": "application/json",
            "Authorization": f"Klaviyo-API-Key {KLAVIYO_API_KEY}"
        }
        
        res = requests.post(url, json=payload, headers=headers)
        
        if res.status_code >= 400:
            raise Exception(f"{res.status_code}: {res.text}")
        
        config["html"]=res.json()['data']['attributes']['html']
        del config["template"]

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
