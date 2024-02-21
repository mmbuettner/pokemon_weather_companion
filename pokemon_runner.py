from helper_functions import api_request
from models.PokemonType import PokemonType
from models.Pokemon import Pokemon

def load_pokemon_type_data():
    pokemon_type_reponse = api_request('https://pokeapi.co/api/v2/type/')
    type_count = pokemon_type_reponse['count']
    type_results = pokemon_type_reponse['results']
    pokemon_type = PokemonType(type_count,type_results)
    return pokemon_type

def load_pokemon_by_type_data(url):
    pokemon_by_type_response = api_request(url)
    damage_relations = pokemon_by_type_response['damage_relations']
    pokemons = pokemon_by_type_response['pokemon']
    pokemon_by_type = Pokemon(damage_relations,pokemons)
    return pokemon_by_type

def gather_all_pokemon_related_to_type(pokemon_type):
    types = []
    for type in pokemon_type.type_results:
        print(type.type_name)
        pokemon_info = load_pokemon_by_type_data(type.type_url)
        for pokemon in pokemon_info.pokemons:
            print(f"  {pokemon.pokemon.pokemon_name}")


def main():
    pokemon_type = load_pokemon_type_data()
    gather_all_pokemon_related_to_type(pokemon_type)

if __name__ == "__main__":
    main()