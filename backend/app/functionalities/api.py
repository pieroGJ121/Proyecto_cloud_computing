#!/usr/bin/env python3

import requests


def do_request_api(body, path):
    headers = {
        "Client-ID": "pr04ecrkpf9xqs3k79jvubif7rsjq5",
        "Authorization": "Bearer syu5zrqkuatzh7njg8bbuc6ifpk6n2",
        "Accept": "application/json",
    }
    url = "https://api.igdb.com/v4/" + path

    response = requests.post(url, headers=headers, data=body)
    return response
