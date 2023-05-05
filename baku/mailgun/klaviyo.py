# -*- coding: utf-8 -*-

import requests
import logging
import os

templateid = os.getenv("templateid")
apikey = os.getenv("apikey")

def donwload(data):

    url = f"https://a.klaviyo.com/api/v1/email-template/{templateid}/render?api_key={apikey}"
    
    logging.debug("klaviyo url: %s", url)

    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded"
    }

    res = requests.post(url, data=data, headers=headers)

    logging.debug("klaviyo text: %s", res.text)
    
    return res.text
