from collections import OrderedDict

from weather_runner import weather_dict
from helper_functions import db_select_query

pogo_weather_companion_json = {}
pogo_weather_companion_json = weather_dict()


def boosted_types():
    sql_stmt = f"""
        SELECT type FROM public.weather_boost_by_type 
        WHERE weather_condition LIKE '{pogo_weather_companion_json['weather']['weather'].lower()}'
    """
    boosts = db_select_query(sql_stmt)
    boost_list = []
    for boost in boosts:
        boost_list.append(boost[0])

    boosted_type_dict = {'boosted_types': boost_list}
    pogo_weather_companion_json.update(boosted_type_dict)

    return boost_list


def double_damage_to_types(boost_list):
    double_damage_to_dict = {}
    for boost in boost_list:
        boost_dict = {boost: ''}
        double_damage_to_dict.update(boost_dict)

    type_query = f"type LIKE '{boost_list[0]}'"
    for i in range(1, len(boost_list)):
        or_query = f" OR type LIKE '{boost_list[i]}'"
        type_query = type_query + or_query

    opponent_query = f"opponent NOT LIKE '{boost_list[0]}'"
    for i in range(1, len(boost_list)):
        or_query = f" AND opponent NOT LIKE '{boost_list[i]}'"
        opponent_query = opponent_query + or_query

    sql_stmt = f"""
        SELECT type,opponent FROM public.damage_relations_by_type 
        WHERE damage_relation LIKE 'double_damage_to'
        AND
        (
            {type_query}
        )
        AND
        (
            {opponent_query}
        )
    """
    double_damage_to = db_select_query(sql_stmt)

    for key in double_damage_to_dict.keys():
        opponent_list = []
        for opponent in double_damage_to:
            print(opponent[0])
            if opponent[0] == key:
                opponent_dict = {'opponent': opponent[1]}
                opponent_list.append(opponent_dict)
        double_damage_to_dict[key] = opponent_list

    full_double_damage_dict = {'double_damage_to': [double_damage_to_dict]}
    pogo_weather_companion_json.update(full_double_damage_dict)

    return full_double_damage_dict


def pokemon_with_boosted_types():

    boost_list = ['fighting', 'poison', 'fairy']

    double_damage_to_types(boost_list)

    pokemon_with_boost_dict = {}
    for boost in boost_list:
        boost_dict = {boost: ''}
        pokemon_with_boost_dict.update(boost_dict)

    type_query = f"type LIKE '{boost_list[0]}'"
    for i in range(1, len(boost_list)):
        or_query = f" OR type LIKE '{boost_list[i]}'"
        type_query = type_query + or_query

    sql_stmt = f"""
        SELECT * FROM public.pokemon_by_type WHERE ({type_query})
    """
    boosted_pokemon = db_select_query(sql_stmt)
    for key in pokemon_with_boost_dict.keys():
        pokemon_list = []
        for pokemon in boosted_pokemon:
            if pokemon[1] == key:
                pokemon_dict = {'pokemon': pokemon[0], 'sprite': pokemon[2]}
                pokemon_list.append(pokemon_dict)
        pokemon_with_boost_dict[key] = pokemon_list

    full_boost_dict = {'pokemon_with_boost': [pokemon_with_boost_dict]}

    pogo_weather_companion_json.update(full_boost_dict)
    print(pogo_weather_companion_json)

    return pogo_weather_companion_json


def main():
    pokemon_with_boosted_types()


if __name__ == "__main__":
    main()
