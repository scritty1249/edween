import requests
from urllib.parse import urlencode
import json
# INTENTION:
# Retrieve a User's PUUID from their game name using ACCOUNT-V1
# i.e. "SirSamTheWise#ADC" --> "82743SDFAsd45764"
# PUUID is used to pull other data from other riot API endpoints, more versatile than summoner ID (Which is depreciated)


def get_PUUID(riot_key, host, summoner_name, tag_Line):
    headers = {
        "X-Riot-Token" : riot_key
    }
    #  NEED TO FIX, THIS API ONLY ACCEPTS REGIONAL ROUTING VALUES
    api_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_Line}"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to retrieve data from API: {e}")
