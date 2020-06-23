import os
import requests
import json

ListenAPI_Key = os.environ.get("X_LISTENAPI_KEY")


def search_podcast(search_param):
    url = "https://listen-api.listennotes.com/api/v2/search?q=" + str(search_param)

    # payload = (('q', search_params),)
    headers = {
        'X-ListenAPI-Key': ListenAPI_Key
    }
    response = requests.request('GET', url, headers=headers)
    response = json.loads(response.text)
    return(response)


def get_podcast(podcast_id):
    url = "https://listen-api.listennotes.com/api/v2/podcasts/" + str(podcast_id)
    headers = {
        'X-ListenAPI-Key': ListenAPI_Key
    }
    response = requests.request("GET", url, headers=headers)
    response = json.loads(response.text)
    return(response)
