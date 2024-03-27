from weather_runner import weather_dict
from helper_functions import (
    db_select_query
)

pogo_weather_companion_json = weather_dict()

def boosted_types():
    sql_stmt = f"""
        SELECT type FROM public.weather_boost_by_type 
        WHERE weather_condition 
        LIKE '{pogo_weather_companion_json['weather']['weather'].lower()}'
    """
    boosts = db_select_query(sql_stmt)
    boost_list = []
    for boost in boosts:
        boost_list.append(boost[0])

    boosted_type_dict = {
        'boosted_types' : boost_list
    }
    pogo_weather_companion_json.update(boosted_type_dict)

    return boost_list

def pokemon_with_boosted_types():
    boost_list = ['ground', 'fire', 'grass']
    type_query = f"type LIKE '{boost_list[0]}'"
    for i in range(1, len(boost_list)):
        or_query = f" OR type LIKE '{boost_list[i]}'"
        type_query = type_query + or_query
    
    sql_stmt = f"""
        SELECT * FROM public.pokemon_by_type WHERE ({type_query})
    """
    boosted_pokemon = db_select_query(sql_stmt)
    boosted_pokemon_list = []
    for pokemon in boosted_pokemon:
        boosted_pokemon_list.append(pokemon[0])

    {
        "ground" : [
            {
                "pokemon" : "diglette",
                "sprite" : "url"
            },
        ]
    }

    print(boosted_pokemon_list)


def main():
    pokemon_with_boosted_types()

if __name__=="__main__":
    main()