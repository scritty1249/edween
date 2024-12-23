"""This module intereacts with the local filesystem."""

from os import path
import json

TOKEN_KEY_FILE_FIELDS = {
    "discord": "DISCORD_TOKEN",
    "riot": "RIOT_API_KEY",
}

def validateTokenKeyFile(target_path = "../token-keys.json") -> None:
    """Validates the token-key file at a given path

    Args:
        target_path (str, optional): Path to token-key JSON file. Defaults to "../token-keys.json".

    Raises:
        Exception: Invalid token-key file, missing fields.
        Exception: Invalid token-key file path, file does not exist.
    """    
    fields = set(TOKEN_KEY_FILE_FIELDS)
    if path.exists(target_path):
        with open(target_path) as tokenFile:
            tokenFileKeys = json.load(tokenFile).keys()
            if set(tokenFileKeys) != fields:
                raise Exception("Invalid token-key file: One or more mismatching fields from \"%s\"" % "\", \"".join(tokenFileKeys))
    else:
        raise Exception("Invalid token-key file path: \"%s\" does not exist" % target_path)

def getDiscordKey(target_path = "../token-keys.json") -> str:
    """Retrieves the Discord Token from the specified token-key file

    Args:
        target_path (str, optional): Path to token-key JSON file. Defaults to "../token-keys.json".

    Returns:
        str: Discord Token from the specified file.
    """
    validateTokenKeyFile(target_path)
    with open(target_path) as tokenFile:
        return json.load(tokenFile)[TOKEN_KEY_FILE_FIELDS["discord"]]
    
def getRiotKey(target_path = "../token-keys.json") -> str:
    """Retrieves the Riot API Key from the specified token-key file

    Args:
        target_path (str, optional): Path to token-key JSON file. Defaults to "../token-keys.json".

    Returns:
        str: Riot API key from the specified file.
    """
    validateTokenKeyFile(target_path)
    with open(target_path) as tokenFile:
        return json.load(tokenFile)[TOKEN_KEY_FILE_FIELDS["riot"]]