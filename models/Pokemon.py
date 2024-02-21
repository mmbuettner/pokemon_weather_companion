from models.PokemonDamageRelation import PokemonDamageRelation
from models.PokemonByType import PokemonByType

class Pokemon:
    def __init__(self,damage_relations,pokemons):
        self.damage_relations = self.set_damage_relations(damage_relations)
        self.pokemons = self.set_pokemon(pokemons)

    def set_damage_relations(self,damage_relations):
        damage_relations_info = PokemonDamageRelation(
            double_damage_from = damage_relations['double_damage_from'],
            double_damage_to = damage_relations['double_damage_to'],
            half_damage_from = damage_relations['half_damage_from'],
            half_damage_to = damage_relations['half_damage_to'],
            no_damage_from = damage_relations['no_damage_from'],
            no_damage_to = damage_relations['no_damage_to']
        )
        return damage_relations_info
    
    def set_pokemon(self,pokemons):
        pokemons_by_type = []
        for pokemon in pokemons:
            pokemon_by_type = PokemonByType(
                pokemon = pokemon['pokemon']
            )
            pokemons_by_type.append(pokemon_by_type)
        return pokemons_by_type