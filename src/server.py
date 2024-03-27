from pokemon_runner import boosted_types

from flask import Flask

app = Flask(__name__)

# Data API Route
@app.route("/data")
def data():
    pogo_weather_companion_json = boosted_types()
    
    return pogo_weather_companion_json

if __name__=="__main__":
    app.run(debug=True)