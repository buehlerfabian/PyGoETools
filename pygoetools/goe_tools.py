import requests
import json
import config


def get_status():
    dat = requests.get(f'{config.goe_url}/api/status').text
    js = json.loads(dat)
    return js
