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


def get_game_info_api(id):
    fields = "fields name, first_release_year, genres.name, platforms.name, involved_companies.company.name, cover.image_id;"
    body = fields + " where id = " + id + ";"
    data = do_request_api(body, "games").json()[0]
    return {
        'api_id': id,
        'name': data["name"],
        'release_year': data["first_release_year"],
        'genres': data["genres"],
        'platforms': data["platforms"],
        'summary': data["summary"],
        'involved_companies': data["involved_companies"],
        'cover': "https:" + data["cover"],
    }
