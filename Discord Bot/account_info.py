from utils import file
import requests
from urllib.parse import urlencode
import json
# INTENTION:
# Retrieve a User's PUUID from their game name using ACCOUNT-V1
# i.e. "SirSamTheWise#ADC" --> "827439587698345764"
# PUUID is used to pull other data from other riot API endpoints, more versatile than summoner ID (Which is depreciated)


# For testing, remove on deploy
def main():
    configs = file.getConfig()
    region_code = configs["default-region-code"] if "default-region-code" in configs.keys() else None
    print(getAccountInfo("ImplatonicEye", "NA1", region_code))

# Keep on Deploy
def getAccountInfo(summoner_name = None, tag_Line = None, region = None):
    if not summoner_name:
        summoner_name = input("Summoner Name: ").casefold()
    elif not tag_Line:
        tag_Line = input("Tag Line: ")
    headers = {
        "X-Riot-Token" : file.getRiotKey()
    }
    api_url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_Line}"
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to retrieve data from API: {e}")
        return None

# For testing, remove on deploy
if __name__ == "__main__":
    main()