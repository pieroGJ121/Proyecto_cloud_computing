#!/usr/bin/env python3

import requests


def do_request_api(body, path):
    headers = {
        "Client-ID": "inixjoprq3bs2tmtlolxsjyqbx5blx",
        "Authorization": "Bearer mnjptwsceihsx8jhik5s2sebezz2i6",
        "Accept": "application/json",
    }
    url = "https://api.igdb.com/v4/" + path

    response = requests.post(url, headers=headers, data=body)
    return response
