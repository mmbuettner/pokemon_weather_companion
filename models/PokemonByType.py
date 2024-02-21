from models.PokemonInfo import PokemonInfo

class PokemonByType:
    def __init__(self,pokemon):
        self.pokemon = self.set_pokemon(pokemon)
    
    def set_pokemon(self,pokemon):
        pokemon_info = PokemonInfo(
            pokemon_name = pokemon['name'],
            pokemon_url = pokemon['url']
        )
        return pokemon_info