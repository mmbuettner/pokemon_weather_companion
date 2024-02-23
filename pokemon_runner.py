from helper_functions import api_request
from models.PokemonType import PokemonType
from models.Pokemon import Pokemon

from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    String
)

engine = create_engine('postgresql://localhost/poke_go_pal')
metadata_obj = MetaData()


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
                "type" : type.type_name,
                "pokemon" : pokemon.pokemon.pokemon_name
            }
            pokemon_by_types_list.append(pokemon_by_type_dict)
    return pokemon_by_types_list


def gather_all_weather_boosts_by_type(pokemon_type):
    weather_boost_by_type_list = []
    for type in pokemon_type.type_results:
        if type in ('grass', 'fire', 'ground'):
            weather_condition = 'sunny'
        elif type in ('water', 'electric', 'bug'):
            weather_condition = 'rainy'
        elif type in ('normal', 'rock'):
            weather_condition = 'partly cloudy'
        elif type in ('fairy', 'fighting', 'poison'):
            weather_condition = 'cloudy'
        elif type in ('flying', 'dragon', 'psychic'):
            weather_condition = 'windy'
        elif type in ('ice', 'steel'):
            weather_condition = 'snow'
        elif type in ('dark', 'ghost'):
            weather_condition = 'fog'
        else:
            weather_condition = 'none'
        
        weather_boost_by_type_dict = {
            "weather_condition" : weather_condition,
            "type" : type
        }
        weather_boost_by_type_list.append(weather_boost_by_type_dict)
    return weather_boost_by_type_list

def gather_all_damage_relations(pokemon_type):
    damage_relations_by_type_list = []
    for type in pokemon_type.type_results:
        pokemon_info = load_pokemon_by_type_data(type.type_url)
        for damage_relation in pokemon_info.damage_relations.double_damage_to:
            to_type = damage_relation.name
            damage_relations_by_type_dict = {
                "type" : type,
                "damage_relation" : "double_damage",
                "to_type" : to_type
            }
            damage_relations_by_type_list.append(damage_relations_by_type_dict)
        for damage_relation in pokemon_info.damage_relations.half_damage_to:
            to_type = damage_relation.name
            damage_relations_by_type_dict = {
                "type" : type,
                "damage_relation" : "half_damage",
                "to_type" : to_type
            }
            damage_relations_by_type_list.append(damage_relations_by_type_dict)
        for damage_relation in pokemon_info.damage_relations.no_damage_to:
            to_type = damage_relation.name
            damage_relations_by_type_dict = {
                "type" : type,
                "damage_relation" : "no_damage",
                "to_type" : to_type
            }
            damage_relations_by_type_list.append(damage_relations_by_type_dict)
    return damage_relations_by_type_list


def create_pokemon_by_type_table_schema():
    pokemon_by_type_table_name = "pokemon_by_type"
    pokemon_by_type = Table(
        pokemon_by_type_table_name,
        metadata_obj,
        Column("Type", String),
        Column("Pokemon", String)
    )
    return pokemon_by_type


def create_weather_boost_by_type_table_schema():
    weather_boost_by_type_table_name = "weather_boost_by_type"
    weather_boost_by_type = Table(
        weather_boost_by_type_table_name,
        metadata_obj,
        Column("Weather_Condition", String),
        Column("Type", String)
    )
    return weather_boost_by_type


def create_damage_relations_by_type_table_schema():
    damage_relations_by_type_table_name = "damage_relations_by_type"
    damage_relations_by_type = Table(
        damage_relations_by_type_table_name,
        metadata_obj,
        Column("Damage_Relation", String),
        Column("Type", String),
        Column("To_Type", String)
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
    create_pokemon_by_type_table_schema()
    create_weather_boost_by_type_table_schema()
    create_damage_relations_by_type_table_schema()
    metadata_obj.create_all(engine)
    print(metadata_obj.tables)



if __name__ == "__main__":
    main()

