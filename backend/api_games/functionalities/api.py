#!/usr/bin/env python3

import requests
from datetime import datetime


def do_request_api(body, path):
    headers = {
        "Client-ID": "pr04ecrkpf9xqs3k79jvubif7rsjq5",
        "Authorization": "Bearer 7yezqyxid5s4dhbbceddb3bj5vlh0l",
        "Accept": "application/json",
    }
    url = "https://api.igdb.com/v4/" + path

    response = requests.post(url, headers=headers, data=body)
    return response


def get_game_info_api(id):
    fields = "fields summary, name, first_release_date, genres.name, platforms.name, involved_companies.company.name, cover.image_id;"
    body = fields + " where id = " + str(id) + ";"
    data = do_request_api(body, "games").json()[0]
    return {
        'api_id': id,
        'name': data["name"],
        'release_year': datetime.utcfromtimestamp(data["first_release_date"]).strftime('%d-%m-%Y'),
        'genres': [i["name"] for i in data["genres"]],
        'platforms': [i["name"] for i in data["platforms"]],
        'summary': data["summary"],
        'involved_companies': [i["company"]["name"] for i in data["involved_companies"]],
        'cover': "https://images.igdb.com/igdb/image/upload/t_1080p/" + data["cover"]["image_id"] + ".jpg",
    }
