from Enviroment import Enviroment

import requests
import json
from sqlalchemy import (
    insert
)

env = Enviroment()


def api_request(url):
    response = requests.get(url)
    json_data = json.loads(response.text)
    return json_data

def insert_rows_to_table(table, list_of_dicts):
    with env.engine.connect() as conn:
        result = conn.execute(
            insert(table),
            list_of_dicts
        )
        conn.commit()

def test_dict(list):
    for dict in list:
        for key, value in dict.items():
            print(f"{key}: {value}")
