from models.PokemonTypeInfo import PokemonTypeInfo

class PokemonType:
    def __init__(self,type_count,type_results):
        self.type_count = type_count
        self.type_results = self.set_type_results(type_results)
    
    def set_type_results(self,type_results):
        types = []
        for type in type_results:
            pokemon_type_info = PokemonTypeInfo(
                type_name = type['name'],
                type_url = type['url']
            )
            types.append(pokemon_type_info)
        return types