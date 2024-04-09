from pokemon_runner import pokemon_with_boosted_types

from flask import Flask

app = Flask(__name__)


# Data API Route
@app.route("/data")
def data():

    pogo_weather_companion_json = pokemon_with_boosted_types()

    return pogo_weather_companion_json


if __name__ == "__main__":
    app.json.sort_keys = False
    app.run(host="0.0.0.0", port=8080 ,debug=True)
