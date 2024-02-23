from models.Damage import Damage

class PokemonDamageRelation:
    def __init__(self,double_damage_from,double_damage_to,half_damage_from,half_damage_to,no_damage_from,no_damage_to):
        self.double_damage_from = self.set_damage(double_damage_from)
        self.double_damage_to = self.set_damage(double_damage_to)
        self.half_damage_from = self.set_damage(half_damage_from)
        self.half_damage_to = self.set_damage(half_damage_to)
        self.no_damage_from = self.set_damage(no_damage_from)
        self.no_damage_to = self.set_damage(no_damage_to)

    def set_damage(self,damage):
        damage_types = []
        for type in damage:
            damage_type = Damage(
                name = type['name'],
                url = type['url']
            )
            damage_types.append(damage_type)
        return damage_types