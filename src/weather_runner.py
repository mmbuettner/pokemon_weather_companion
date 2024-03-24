from geopy.geocoders import Nominatim
import requests
from sqlalchemy import (
    Table,
    Column,
    String,
    Integer,
    PrimaryKeyConstraint,
    text
)

from Enviroment import Enviroment
from helper_functions import (
    insert_rows_to_table
)

env = Enviroment()


def create_geoposition_table():
    geoposition_table_name = 'geoposition_keys'
    geoposition_table = Table(
        geoposition_table_name,
        env.metadata_obj,
        Column('city', String),
        Column('region', String),
        Column('country', String),
        Column('postalcode', Integer),
        Column('location_key', Integer),
        PrimaryKeyConstraint('city',
                             'region',
                             'country',
                             'postalcode',
                             'location_key')
    )
    return geoposition_table


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location():
    ip_address = get_ip()
    response = requests.get(f'http://ip-api.com/json/{ip_address}').json()
    location_data = {
        'city': response.get('city'),
        'region': response.get('region'),
        'country': response.get('country'),
        'postalcode': response.get('zip')
    }
    print(f"{response}\n\n")
    return location_data


def get_lat_lon():
    location_data = get_location()
    geolocator = Nominatim(user_agent="Poke_Go_Pal")
    my_location = geolocator.geocode(location_data)
    lat_lon = f"{my_location.latitude},{my_location.longitude}"
    return lat_lon


def location_key_api_query():
    lat_lon = get_lat_lon()
    response = requests.get(f"http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey={env.weather_api_key}&q={lat_lon}").json()
    location_key = response.get('Key')
    print(f"{response}\n\n")
    return location_key


def get_location_key():

    geoposition_table = create_geoposition_table()
    env.metadata_obj.create_all(env.engine)

    location_data = get_location()

    query_bool, result = geoposition_query(location_data)
    if query_bool == False:
        location_key = location_key_api_query()
        location_data['location_key'] = location_key
        insert_rows_to_table(geoposition_table,location_data)
    else: 
        location_key = result[0][-1]
    
    return location_key


def geoposition_query(location_data):

    with env.engine.connect() as conn:
        query = text(f"""
            SELECT * FROM public.geoposition_keys 
            WHERE (
                city LIKE '{location_data['city']}'
                AND region LIKE '{location_data['region']}'
                AND country LIKE '{location_data['country']}'
                AND postalcode = '{location_data['postalcode']}'
            )
        """)
        results = conn.execute(query)
        rows = results.fetchall() if results.rowcount > 0 else ()

    if not rows:
        bool = False
    else:
        bool = True
    
    return bool, rows


def get_weather_data():
    location_key = get_location_key()
    response = requests.get(f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}?apikey={env.weather_api_key}").json()
    print(response)


def main():
    get_weather_data()


if __name__ == "__main__":
    main()