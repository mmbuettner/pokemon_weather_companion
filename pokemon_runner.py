"""
    Notes to work on tomorrow:
        - Figure out a way to clean up gather_all_damage_relations()
        function by creating an agnostic helper function
        - Figure out a way to only add _NEW_ entries and not duplicate
        entries without necessarily having a unique key
        - General clean up with Enviroment object and check imports
"""

from helper_functions import api_request, insert_rows_to_table
from models.PokemonType import PokemonType
from models.Pokemon import Pokemon
from Enviroment import Enviroment

from sqlalchemy import (
    Table,
    Column,
    String,
    Integer
)


env = Enviroment()


def load_pokemon_type_data():
    pokemon_type_reponse = api_request('https://pokeapi.co/api/v2/type/')
    type_count = pokemon_type_reponse['count']
    type_results = pokemon_type_reponse['results']
    pokemon_type = PokemonType(type_count,type_results)
    return pokemon_type


def load_pokemon_by_type_data(url):
    pokemon_by_type_response = api_request(url)
    damage_relations = pokemon_by_type_response['damage_relations']
    type_name = pokemon_by_type_response['name']
    pokemons = pokemon_by_type_response['pokemon']
    pokemon_by_type = Pokemon(damage_relations,type_name,pokemons)
    return pokemon_by_type


def gather_all_pokemon_related_to_type(pokemon_type):
    pokemon_by_types_list = []
    for type in pokemon_type.type_results:
        pokemon_info = load_pokemon_by_type_data(type.type_url)
        for pokemon in pokemon_info.pokemons:
            pokemon_by_type_dict = {
                "Type" : type.type_name,
                "Pokemon" : pokemon.pokemon.pokemon_name
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
        'ghost': 'fog'
    }
    return weather_conditions.get(type_name, 'none')


def gather_all_weather_boosts_by_type(pokemon_type):
    weather_boost_by_type_list = []
    for type in pokemon_type.type_results:
        weather_condition = get_weather_condition(type.type_name)
        weather_boost_by_type_dict = {
            "Weather_Condition" : weather_condition,
            "Type" : type.type_name
        }
        weather_boost_by_type_list.append(weather_boost_by_type_dict)
    return weather_boost_by_type_list


def add_damage_relations(damage_relations_list, damage_type, type_name, relation_type):
    for damage_relation in damage_type:
        to_type = damage_relation.name
        damage_relations_by_type_dict = {
            "Damage_Relation" : relation_type,
            "Type" : type_name,
            "Opponent" : to_type
        }
        damage_relations_list.append(damage_relations_by_type_dict)


def gather_all_damage_relations(pokemon_type):
    damage_relations_by_type_list = []
    for type in pokemon_type.type_results:
        pokemon_info = load_pokemon_by_type_data(type.type_url)
        add_damage_relations(damage_relations_by_type_list, pokemon_info.damage_relations.double_damage_to, type.type_name, "double_damage_to")
        add_damage_relations(damage_relations_by_type_list, pokemon_info.damage_relations.half_damage_to, type.type_name, "half_damage_to")
        add_damage_relations(damage_relations_by_type_list, pokemon_info.damage_relations.no_damage_to, type.type_name, "no_damage_to")
        add_damage_relations(damage_relations_by_type_list, pokemon_info.damage_relations.double_damage_from, type.type_name, "double_damage_from")
        add_damage_relations(damage_relations_by_type_list, pokemon_info.damage_relations.half_damage_from, type.type_name, "half_damage_from")
        add_damage_relations(damage_relations_by_type_list, pokemon_info.damage_relations.no_damage_from, type.type_name, "no_damage_from")
    return damage_relations_by_type_list


def create_pokemon_by_type_table_schema():
    pokemon_by_type_table_name = "pokemon_by_type"
    pokemon_by_type = Table(
        pokemon_by_type_table_name,
        env.metadata_obj,
        Column("Id", Integer, primary_key=True, nullable=False),
        Column("Type", String),
        Column("Pokemon", String)
    )
    return pokemon_by_type


def create_weather_boost_by_type_table_schema():
    weather_boost_by_type_table_name = "weather_boost_by_type"
    weather_boost_by_type = Table(
        weather_boost_by_type_table_name,
        env.metadata_obj,
        Column("Id", Integer, primary_key=True, nullable=False),
        Column("Weather_Condition", String),
        Column("Type", String)
    )
    return weather_boost_by_type


def create_damage_relations_by_type_table_schema():
    damage_relations_by_type_table_name = "damage_relations_by_type"
    damage_relations_by_type = Table(
        damage_relations_by_type_table_name,
        env.metadata_obj,
        Column("Id", Integer, primary_key=True, nullable=False),
        Column("Damage_Relation", String),
        Column("Type", String),
        Column("Opponent", String)
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

    # """
    # Create database table schema if tables don't already exist
    # """
    # pokemon_by_type_table = create_pokemon_by_type_table_schema()
    # weather_boost_by_type_table = create_weather_boost_by_type_table_schema()
    # damage_relations_by_type_table = create_damage_relations_by_type_table_schema()
    # env.metadata_obj.create_all(env.engine)

    # """
    # Inserting new rows for every list of dictionaries create
    # """
    # insert_rows_to_table(pokemon_by_type_table, pokemon_by_types_list)
    # insert_rows_to_table(weather_boost_by_type_table, weather_boost_by_type_list)
    # insert_rows_to_table(damage_relations_by_type_table, damage_relations_by_type_list)






if __name__ == "__main__":
    main()

