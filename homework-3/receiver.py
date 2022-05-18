from datetime import datetime
from time import sleep

import requests

def print_message(message):
    t = message['time']
    dt = datetime.fromtimestamp(t)
    print(dt.strftime('%Y-%m-%d %H:%M:%S'), message['name'])
    if type(message['text']) == dict:
        dct = message['text']
        for k, v in dct.items():
            print("{}: {}".format(k, v))
    else:
        print(message['text'])


after = 0
while True:
    response = requests.get(
        'http://127.0.0.1:5000/messages',
                            params={'after': after})
    messages = response.json()['messages']
    for message in messages:
        print_message(message)
        after = message['time']
    sleep(1)