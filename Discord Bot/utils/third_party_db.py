"""# What did you expect?
we play League of Legends.
"""
from bs4 import BeautifulSoup
from json import loads
from random import randint
import re
import requests

def get_funny_names():
    db_url = "http://rsdb.org/api/html/all" 
    response = requests.get(db_url)
    if response.status_code != 200:
        return
    data = loads(response.content.decode("utf-8")).values()
    return [re.search(r'<tr.*?><td><a.*?>(.*?)</a></td><td><a href=', content).group(1) for content in data if content]

def pick_random_name():
    db = get_funny_names()
    return db[randint(0, len(db) - 1)]