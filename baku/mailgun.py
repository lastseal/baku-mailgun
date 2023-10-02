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

def send(config, data=None, files=None):

    logging.info("sending mail to %s", config['to'])

    config['subject'] = config['subject'].format(**data)

    if data is not None and 'template' in config:
        
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
        
        res = requests.post("https://a.klaviyo.com/api/template-render/", json=payload, headers=headers)
        
        if res.status_code >= 400:
            raise Exception({"status": res.status_code, "message": res.text})
        
        config["html"]=res.json()['data']['attributes']['html']
        del config["template"]

    elif data is not None and 'text' in config:
        config['text'] = config['text'].format(**data)
        logging.debug("%s", config['text'])
        
    attachment = config.get("attachment", 0)
    
    if attachment > 0 and files is not None:
        logging.info("files: %s", files)
        files = [("attachment", (files[name].filename, files[name].read())) for name in files]

    res = requests.post(f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
        auth=("api", MAILGUN_KEY),
        data=config,
        files=files
    )

    if res.status_code >= 400:
        raise Exception({"status": res.status_code, "message": res.text})

    data = res.json()

    logging.debug("mailgun res: %s", data)

    return data['message']
