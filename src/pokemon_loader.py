"""
    Notes to work on tomorrow:
        - Look into how to refactor the structure of main
        - How to optimize the new unique data entry 
"""

from models.PokemonType import PokemonType
from models.Pokemon import Pokemon
from Enviroment import Enviroment
from helper_functions import (
    api_request,
    select_all_from_table,
    check_and_insert_rows,
    compare_dataframes,
)

from sqlalchemy import Table, Column, String, PrimaryKeyConstraint


env = Enviroment()


def load_pokemon_type_data():
    pokemon_type_reponse = api_request('https://pokeapi.co/api/v2/type/')
    type_count = pokemon_type_reponse['count']
    type_results = pokemon_type_reponse['results']
    pokemon_type = PokemonType(type_count, type_results)
    return pokemon_type


def load_pokemon_by_type_data(url):
    pokemon_by_type_response = api_request(url)
    damage_relations = pokemon_by_type_response['damage_relations']
    type_name = pokemon_by_type_response['name']
    pokemons = pokemon_by_type_response['pokemon']
    pokemon_by_type = Pokemon(damage_relations, type_name, pokemons)
    return pokemon_by_type


def load_pokemon_sprite(url):
    pokemon_sprite = api_request(url)
    sprites = pokemon_sprite['sprites']['front_default']
    return sprites


def gather_all_pokemon_related_to_type(pokemon_type):
    pokemon_by_types_list = []
    counter_type = 0
    for type in pokemon_type.type_results:
        counter_type += 1
        pokemon_by_type_info = load_pokemon_by_type_data(type.type_url)
        counter_pokemons = 0
        for pokemon in pokemon_by_type_info.pokemons:
            counter_pokemons += 1
            print(
                f"Working on pokemon {counter_pokemons} of {len(pokemon_by_type_info.pokemons)} in type {counter_type} of {len(pokemon_type.type_results)}"
            )
            pokemon_sprite = load_pokemon_sprite(pokemon.pokemon.pokemon_url)
            pokemon_by_type_dict = {
                'pokemon': pokemon.pokemon.pokemon_name,
                'type': type.type_name,
                'sprite': pokemon_sprite,
            }
            pokemon_by_types_list.append(pokemon_by_type_dict)
    return pokemon_by_types_list


def get_weather_condition(type_name):
    weather_conditions = {
        'grass': 'sunny',
        'fire': 'sunny',
        'ground': 'sunny',
        'water': 'rainy',
        'electric': 'rainy',
        'bug': 'rainy',
        'normal': 'partly cloudy',
        'rock': 'partly cloudy',
        'fairy': 'cloudy',
        'fighting': 'cloudy',
        'poison': 'cloudy',
        'flying': 'windy',
        'dragon': 'windy',
        'psychic': 'windy',
        'ice': 'snow',
        'steel': 'snow',
        'dark': 'fog',
        'ghost': 'fog',
    }
    return weather_conditions.get(type_name, 'none')


def gather_all_weather_boosts_by_type(pokemon_type):
    weather_boost_by_type_list = []
    for type in pokemon_type.type_results:
        weather_condition = get_weather_condition(type.type_name)
        weather_boost_by_type_dict = {
            'weather_condition': weather_condition,
            'type': type.type_name,
        }
        weather_boost_by_type_list.append(weather_boost_by_type_dict)
    return weather_boost_by_type_list


def add_damage_relations(damage_relations_list, damage_type, type_name, relation_type):
    for damage_relation in damage_type:
        to_type = damage_relation.name
        damage_relations_by_type_dict = {
            'damage_relation': relation_type,
            'type': type_name,
            'opponent': to_type,
        }
        damage_relations_list.append(damage_relations_by_type_dict)


def gather_all_damage_relations(pokemon_type):
    damage_relations_by_type_list = []
    for type in pokemon_type.type_results:
        pokemon_info = load_pokemon_by_type_data(type.type_url)
        add_damage_relations(
            damage_relations_by_type_list,
            pokemon_info.damage_relations.double_damage_to,
            type.type_name,
            'double_damage_to',
        )
        add_damage_relations(
            damage_relations_by_type_list,
            pokemon_info.damage_relations.half_damage_to,
            type.type_name,
            'half_damage_to',
        )
        add_damage_relations(
            damage_relations_by_type_list,
            pokemon_info.damage_relations.no_damage_to,
            type.type_name,
            'no_damage_to',
        )
        add_damage_relations(
            damage_relations_by_type_list,
            pokemon_info.damage_relations.double_damage_from,
            type.type_name,
            'double_damage_from',
        )
        add_damage_relations(
            damage_relations_by_type_list,
            pokemon_info.damage_relations.half_damage_from,
            type.type_name,
            'half_damage_from',
        )
        add_damage_relations(
            damage_relations_by_type_list,
            pokemon_info.damage_relations.no_damage_from,
            type.type_name,
            'no_damage_from',
        )
    return damage_relations_by_type_list


def create_pokemon_by_type_table_schema():
    pokemon_by_type_table_name = 'pokemon_by_type'
    pokemon_by_type = Table(
        pokemon_by_type_table_name,
        env.metadata_obj,
        Column('pokemon', String),
        Column('type', String),
        Column('sprite', String, nullable=True),
        PrimaryKeyConstraint('pokemon', 'type'),
    )
    return pokemon_by_type


def create_weather_boost_by_type_table_schema():
    weather_boost_by_type_table_name = 'weather_boost_by_type'
    weather_boost_by_type = Table(
        weather_boost_by_type_table_name,
        env.metadata_obj,
        Column('weather_condition', String),
        Column('type', String),
        PrimaryKeyConstraint('weather_condition', 'type'),
    )
    return weather_boost_by_type


def create_damage_relations_by_type_table_schema():
    damage_relations_by_type_table_name = 'damage_relations_by_type'
    damage_relations_by_type = Table(
        damage_relations_by_type_table_name,
        env.metadata_obj,
        Column('damage_relation', String),
        Column('type', String),
        Column('opponent', String),
        PrimaryKeyConstraint('damage_relation', 'type', 'opponent'),
    )
    return damage_relations_by_type


def main():
    """
    Load pokemon types from Pokemon API and gather all Pokemon type relations
    """
    pokemon_type = load_pokemon_type_data()

    """
    Create lists of dictionary for data table entry
    """
    pokemon_by_types_list = gather_all_pokemon_related_to_type(pokemon_type)
    weather_boost_by_type_list = gather_all_weather_boosts_by_type(pokemon_type)
    damage_relations_by_type_list = gather_all_damage_relations(pokemon_type)

    """
    Create database table schema if tables don't already exist
    """
    pokemon_by_type_table = create_pokemon_by_type_table_schema()
    weather_boost_by_type_table = create_weather_boost_by_type_table_schema()
    damage_relations_by_type_table = create_damage_relations_by_type_table_schema()
    env.metadata_obj.create_all(env.engine)

    """
    Check to see if first run data exists in database, if not insert
    """
    list_of_objects = [
        weather_boost_by_type_list,
        pokemon_by_types_list,
        damage_relations_by_type_list,
    ]
    list_of_tables = [
        pokemon_by_type_table,
        weather_boost_by_type_table,
        damage_relations_by_type_table,
    ]
    check_and_insert_rows(list_of_objects, list_of_tables)

    """
    Pull existing rows from table into a list of dictionaries
    """
    result_list_of_rows_for_pokemon_by_types_list = select_all_from_table(
        pokemon_by_type_table
    )
    result_list_of_rows_for_weather_boost_by_type = select_all_from_table(
        weather_boost_by_type_table
    )
    result_list_of_rows_for_damage_relations_by_type = select_all_from_table(
        damage_relations_by_type_table
    )

    """
    Create a unique list of dictionaries that do not already exist in the database
    """
    unique_list_of_pokemon_by_type_dicts = compare_dataframes(
        result_list_of_rows_for_pokemon_by_types_list, pokemon_by_types_list
    )
    unique_list_of_weather_boost_by_type_dicts = compare_dataframes(
        result_list_of_rows_for_weather_boost_by_type, weather_boost_by_type_list
    )
    unique_list_of_damage_relations_by_type_dicts = compare_dataframes(
        result_list_of_rows_for_damage_relations_by_type, damage_relations_by_type_list
    )

    """
    Check to see if there is data to add, and also if the data does not already exist
    """
    unique_list_of_objects = [
        unique_list_of_pokemon_by_type_dicts,
        unique_list_of_weather_boost_by_type_dicts,
        unique_list_of_damage_relations_by_type_dicts,
    ]
    check_and_insert_rows(unique_list_of_objects, list_of_tables)


if __name__ == "__main__":
    main()
