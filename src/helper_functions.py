from Enviroment import Enviroment

import requests
import json
from sqlalchemy import (
    insert,
    text
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

    print(f"Added {len(list_of_dicts)} new entries.")


def check_and_insert_rows(list_of_objects, list_of_tables):
    for table in list_of_tables:
        for objects in list_of_objects:
            if objects:
                key = list(objects[0].keys())[0]
                if key in table.columns:
                    try: 
                        insert_rows_to_table(table, objects)
                        print(f"Inserted entry to {key} table!")
                    except Exception as e:
                        print(f"Data exists already in {key} table!")
                        pass


def select_all_from_table(table):
    query = table.select()
    with env.engine.connect() as conn:
        result = conn.execute(query)

        result_list_of_rows = []
        for row in result.fetchall():
            row_dict = {}
            for idx, column in enumerate(table.columns):
                row_dict[column.name] = row[idx]
            result_list_of_rows.append(row_dict)
        
        conn.close()
        return result_list_of_rows
    

def compare_dataframes(db_list, api_list):
    print(f"{len(db_list)} entries in DB and {len(api_list)} objects from API.")
    db_list_keys = {tuple(item.items()) for item in db_list}
    api_list_keys = {tuple(item.items()) for item in api_list}

    unique_keys = api_list_keys - db_list_keys

    unique_dicts = [dict(key_value_pairs) for key_value_pairs in unique_keys]
    print(f"Quantity of new entries: {len(unique_dicts)}")
    return unique_dicts


def db_select_query(sql_stmt):
    with env.engine.connect() as conn:
        query = text(sql_stmt)
        results = conn.execute(query)
        rows = results.fetchall() if results.rowcount > 0 else ()

    return rows
