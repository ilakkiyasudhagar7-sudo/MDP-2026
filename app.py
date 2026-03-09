from flask import Flask, render_template, redirect, request
import json
import requests

app = Flask(__name__)

API_KEY = "d180e543cab15475e2b82ac2982cce3b"


@app.route("/", methods=["GET", "POST"])
def index():
    comfort_score = None
    categories = []
    gender = "women"
    place = ""
    temp = None
    humidity = None

    if request.method == "POST":
        place = request.form["place"]
        gender = request.form["gender"]

        try:
            # Fetch weather data from OpenWeatherMap
            url = f"http://api.openweathermap.org/data/2.5/weather?q={place}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            data = response.json()

            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]

            # Comfort score calculation
            comfort_score = round((temp - 15) / 2, 1)

        except:
            comfort_score = None

        # Comfort score ranges → outfit categories
        if comfort_score is not None:

            if comfort_score >= 9.0:   # HOT
                if gender == "women":
                    categories = ["cotton_kurtis_long", "palazzo_with_kurti"]
                else:
                    categories = ["cotton_kurtas", "chino_pants"]

            elif comfort_score >= 7.0:   # WARM
                if gender == "women":
                    categories = ["cotton_kurtis_long", "anarkali_suits"]
                else:
                    categories = ["cotton_kurtas", "button_shirts"]

            elif comfort_score >= 5.0:   # MODERATE
                if gender == "women":
                    categories = ["salwar_suits", "maxi_tunics"]
                else:
                    categories = ["cotton_kurtas", "chino_pants"]

            elif comfort_score >= 3.0:   # CHILLY
                if gender == "women":
                    categories = ["anarkali_suits", "salwar_suits"]
                else:
                    categories = ["button_shirts", "chino_pants"]

            else:   # COLD
                if gender == "women":
                    categories = ["salwar_suits", "anarkali_suits"]
                else:
                    categories = ["button_shirts", "cotton_kurtas"]

    return render_template(
        "index.html",
        comfort=comfort_score,
        categories=categories,
        gender=gender,
        place=place,
        temp=temp,
        humidity=humidity,
        category_count=len(categories)
    )


@app.route("/category/<name>")
def category(name):
    with open("outfits.json") as f:
        data = json.load(f)

    return render_template(
        "category.html",
        title=name.replace("_", " ").title(),
        items=data.get(name, [])
    )


@app.route("/buy")
def buy():
    url = request.args.get("url")
    return redirect(url or "/")


if __name__ == "__main__":
    app.run(debug=True)
