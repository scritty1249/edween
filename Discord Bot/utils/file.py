"""This module intereacts with the local filesystem."""

from os import path, getcwd
import json
CWD = getcwd()
TOKEN_KEY_FILE_FIELDS = {
    "discord": "DISCORD_TOKEN",
    "riot": "RIOT_API_KEY",
}

def validate_file(target_path: str) -> None:
    """Validates that a file exists at the given path.

    Args:
        target_path (str): Path to the file to verify.

    Raises:
        Exception: Invalid file path, file does not exist.
    """
    if not path.exists(target_path):
        raise Exception("Invalid file path: \"%s\" does not exist" % target_path)

def validate_token_key_file(target_path = path.join(CWD, "token-keys.json")) -> None:
    """Validates the token-key file at a given path

    Args:
        target_path (str, optional): Path to token-key JSON file. Defaults to "/token-keys.json".

    Raises:
        Exception: Invalid token-key file, missing fields.
        Exception: Invalid token-key file path, file does not exist.
    """    
    fields = set(TOKEN_KEY_FILE_FIELDS.values())
    try:
        validate_file(target_path)
    except Exception as e:
        raise Exception("Invalid token-key file path: \"%s\" does not exist" % target_path)
    with open(target_path) as tokenFile:
        tokenFileKeys = json.load(tokenFile).keys()
        if set(tokenFileKeys) != fields:
            raise Exception("Invalid token-key file: One or more mismatching fields from \"%s\"" % "\", \"".join(tokenFileKeys))        

def get_discord_key(target_path = path.join(CWD, "token-keys.json")) -> str:
    """Retrieves the Discord Token from the specified token-key file

    Args:
        target_path (str, optional): Path to token-key JSON file. Defaults to "/token-keys.json".

    Returns:
        str: Discord Token from the specified file.
    """
    validate_token_key_file(target_path)
    with open(target_path) as tokenFile:
        return json.load(tokenFile)[TOKEN_KEY_FILE_FIELDS["discord"]]
    
def get_riot_key(target_path = path.join(CWD, "token-keys.json")) -> str:
    """Retrieves the Riot API Key from the specified token-key file

    Args:
        target_path (str, optional): Path to token-key JSON file. Defaults to "/token-keys.json".

    Returns:
        str: Riot API key from the specified file.
    """
    validate_token_key_file(target_path)
    with open(target_path) as tokenFile:
        return json.load(tokenFile)[TOKEN_KEY_FILE_FIELDS["riot"]]
    
def get_config(target_path = path.join(CWD, "Discord Bot", "config.json")) -> dict:
    """Gets the configuration file variables.

    Args:
        target_path (str, optional): Path to configuration JSON file. Defaults to "/Discord Bot/config.json".

    Returns:
        dict: A JSON object representing the configuration file.
    """
    validate_file(target_path)
    with open(target_path) as configFile:
        return json.load(configFile)