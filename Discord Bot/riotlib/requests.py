"""
# Riot Library - Requests
Houses functions for retrieving information from the Riot API.
This library is intended to work with API's from Riot as of 12/23/2024
"""
from requests import get, post
from typing import Union, Literal
from urllib.parse import quote_plus
from os import path
import requests
import json

# riotlib modules
from exceptions import *
from dtos import *

# getting values from config file
ENDPOINTS = {}
if __name__ == "__main__":
    from os.path import exists
    endpoint_file_path = "Discord Bot/riot-endpoints.json"
    if not exists(endpoint_file_path):
        raise Exception("riot endpoint json file not found!")
    else:
        with open(endpoint_file_path) as f:
            ENDPOINTS = json.load(f)

def init_endpoints(endpoint_file_path: str = path.join(path.dirname(path.abspath(__file__)), "..", "riot-endpoints.json")) -> None:
    """Initializes library functions using the Riot API. This function must be called before using any other functions from the library.

    Args:
        target_path (str, optional): Path to the file containing Riot API endpoints. Defaults to "riot-endpoints.json".
    """
    global ENDPOINTS
    with open(endpoint_file_path) as f:
        ENDPOINTS = json.load(f)

# helper functions
def assert_response_status(response_code: int) -> None:
    """Validates the status of a Riot API response.

    Args:
        response_code (int): The status code of the Riot API response.

    Raises:
        ApiException: Malformed or invalid request.
        BadKeyException: Invalid Riot API key.
        NotFoundException: The requested information was not found.
        RateLimitExceededException: API key rate limit exceeded.
        ServerErrorException: An error occured after contacting the server.
    """
    if response_code >= 400:
        if response_code == 400 or response_code == 405 or response_code == 415:
            raise ApiException("Bad request. Are the request method, headers, and endpoints correct?")
        elif response_code == 401 or response_code == 403: # not sure about this, need to test if it's one or the other- it's not both. -Kyle
            raise BadKeyException()
        elif response_code == 404:
            raise NotFoundException()
        elif response_code == 429:
            raise RateLimitExceededException()
        elif response_code >= 500:
            raise ServerErrorException()

def construct_request(endpoint_category: Literal["lol", "riot"], endpoint_type: str, endpoint: str, region_code: str = None) -> str:
    """Builds a url to a Riot API endpoint.

    Args:
        endpoint_category ("lol", "riot"): The category of the endpoint.
        endpoint_type (str): The type of endpoint within the category.
        endpoint (str): The endpoint to request from. Can contain multiple subpaths.
        region_code (str, optional): The region code of the endpoint to request from. Defaults to the "default-region-code" value specified in endpoint file.
    
    Raises:
        Exception: Invalid region code.

    Returns:
        str: A constructed url to the endpoint.
    """
    # default region code
    if not region_code:
        region_code = ENDPOINTS["default-region-code"]

    # idiot proofing
    endpoint = endpoint.strip("/")
    if region_code not in ENDPOINTS["platform_routing_values"].keys():
        raise Exception("Invalid region code: %s" % region_code)

    url = "https://"
    # Match region name to platform code if needed
    if ENDPOINTS["routing_value"][endpoint_category][endpoint_type] == "platform":
        url += ENDPOINTS["platform_routing_values"][region_code]
    else:
        region_name = ENDPOINTS["platform-region"][region_code]
        url += ENDPOINTS["region_routing_values"][region_name]

    url = "/".join((
        url, # https prefiex + hostname
        endpoint_category, 
        endpoint_type,
        "v" + str(ENDPOINTS["version"][endpoint_category][endpoint_type]), # api version number
        endpoint
    ))
    return url

def construct_headers(api_key: str) -> dict:
    """Builds authorization headers for making requests to the Riot API.

    Args:
        api_key (str): A Riot API key.

    Returns:
        dict: A dictionary containing the Riot Token authentication header to use in an API request.
    """
    return { "X-Riot-Token" : api_key }

def send_request(url: str, headers: dict = None, query_params: dict = None, method: Literal["get", "post"] = "get") -> requests.Response:
    """Sends an http request.

    Args:
        url (str): The URL to send the request to.
        headers (dict, optional): The headers to send with the request. Defaults to None.
        query_params (dict, optional): The query parameters to send with the request. Defaults to None.
        method (str, optional): The method to use for sending the request. Defaults to "get". 

    Returns:
        requests.Response: A Response object from the executed request.
    """
    if method == "get":
        return requests.get(url = url, params = query_params, headers = headers)
    elif method == "post":
        return requests.post(url = url, params = query_params, headers = headers)
    else: # defualt to get, too lazy to setup error handling here
        return requests.get(url = url, params = query_params, headers = headers)

# getting data directly from riot api
def get_raw_match(match_id: str, api_key: str) -> dict:
    """Get a League match with the specified ID.

    Args:
        match_id (str): The ID of the match to retrieve.
        api_key (str): A Riot API key.

    Raises:
        NotFoundException: A Match with the gien match_id does not exist.

    Returns:
        dict: A JSON body representing a Riot API MatchDto Object.
    """
    url = construct_request("lol", "match", "matches/%s" % match_id)
    headers = construct_headers(api_key)
    response = send_request(url, headers)
    assert_response_status(response.status_code)
    return json.loads(response.content)

def get_raw_match_timeline(match_id: str, api_key: str) -> dict:
    """Get a League match timeline with the specified ID.

    Args:
        match_id (str): The ID of the match to retrieve.
        api_key (str): A Riot API key.

    Returns:
        dict: A JSON body representing a Riot API TimelineDto Object.
    """
    url = construct_request("lol", "match", "matches/%s/timeline" % match_id)
    headers = construct_headers(api_key)
    response = send_request(url, headers)
    assert_response_status(response.status_code)
    return json.loads(response.content)

def get_raw_summoner_data(puuid: str, api_key: str) -> dict:
    """Get a summoner with the specified PUUID.

    Args:
        puuid (str): The PUUID of the summoner to retrieve.
        api_key (str): A Riot API key.

    Returns:
        dict: A JSON body representing a Riot API SummonerDTO Object.
    """
    url = construct_request("lol", "summoner", "summoners/by-puuid/%s" % puuid)
    headers = construct_headers(api_key)
    response = send_request(url, headers)
    assert_response_status(response.status_code)
    return json.loads(response.content)

# handling data, or returning anything from api that isn't the raw response
def get_summoner_puuid_by_name(name: str, tag: str, api_key: str) -> str:
    """Retrieve a player's puuid from their League summoner name and tag.

    Args:
        name (str): The summoner name of the player.
        tag (str): The tag line of the player (after the hashtag).
        api_key (str): A Riot API key.

    Returns:
        str: The puuid of a player with the matching name and tag.
    """
    # idiot proofing
    tag = tag.lstrip("#")
    url = construct_request(
        "riot",
        "account",
        "accounts/by-riot-id/%s/%s"
            % (
                quote_plus(name),
                quote_plus(tag)
            ),
    )
    headers = construct_headers(api_key)
    response = send_request(url, headers)
    assert_response_status(response.status_code)
    AccountDto = json.loads(response.content)
    # reference for AccountDto: https://developer.riotgames.com/apis#account-v1/GET_getByRiotId
    return AccountDto["puuid"]

def get_summoner_name_by_puuid(puuid: str, api_key: str) -> list[str, str]:
    """Retrieve the League summoner name and tag of a player with the given puuid.

    Args:
        puuid (str): The puuid of the player to retrieve.
        api_key (str): A Riot API key.

    Returns:
        list[str, str]: The summoner name, and tag of a player with the matching puuid.
    """
    url = construct_request("riot", "account", "accounts/by-puuid/%s" % puuid)
    headers = construct_headers(api_key)
    response = send_request(url, headers)
    assert_response_status(response.status_code)
    # reference for AccountDto: https://developer.riotgames.com/apis#account-v1/GET_getByPuuid
    AccountDto = json.loads(response.content)
    return [AccountDto["gameName"], AccountDto["tagLine"]]