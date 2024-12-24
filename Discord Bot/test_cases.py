from utils import file
from riotlib.account_info import get_PUUID

def main():
    name = input("Summoner Name: ").strip()
    tag = input("Tag Line: ").strip()
    region = input("Region: ").strip()
    test_acct_info(name, tag, region)

def test_acct_info(game_name, tag_line, region_code ):
    configs = file.get_config()
    if not game_name:
        game_name = input("Summoner Name: ").casefold().strip()
    elif not tag_line:
        tag_line = input("Tag Line: ").strip()
    #  NEED TO FIX, THIS API ONLY ACCEPTS REGIONAL ROUTING VALUES
    if tag_line in configs["routing_values"].keys():
        region_code = tag_line
    else:
        region_code = configs["default-region-code"] if "default-region-code" in configs.keys() else None
    riot_key = file.get_riot_key()
    host = configs["routing_values"][region_code.upper()]
    print(get_PUUID(riot_key, host, game_name, tag_line))


if __name__ == "__main__":
    main()