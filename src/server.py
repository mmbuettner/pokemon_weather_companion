from weather_runner import weather_api

from flask import Flask

app = Flask(__name__)

# Data API Route
@app.route("/data")
def data():
    weather_data = weather_api()
    return weather_data

if __name__=="__main__":
    app.run(debug=True)