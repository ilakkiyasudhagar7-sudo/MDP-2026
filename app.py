from flask import Flask, render_template, redirect, request
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    comfort_score = None
    categories = []
    gender = "women"
    place = ""
    
    if request.method == "POST":
        place = request.form["place"]
        gender = request.form["gender"]
        
        # Mock weather data (replace with ML later)
        temp = 26
        humidity = 65
        comfort_score = round((temp - 15) / 2, 1)

        # Comfort score ranges
        if comfort_score >= 9.0:   # HOT
            if gender == "women":
                categories = ["sleeveless_kurtis", "cotton_maxi_dress", "linen_tunics"]
            else:
                categories = ["linen_shirts", "cotton_shorts", "light_kurtas"]

        elif comfort_score >= 7.0:   # WARM
            if gender == "women":
                categories = ["cotton_kurtis_long", "anarkali_suits", "palazzo_with_kurti"]
            else:
                categories = ["cotton_kurtas", "button_shirts", "chino_pants"]

        elif comfort_score >= 5.0:   # MODERATE
            if gender == "women":
                categories = ["salwar_suits", "maxi_tunics", "casual_kurtis"]
            else:
                categories = ["casual_shirts", "jeans", "polo_tshirts"]

        elif comfort_score >= 3.0:   # CHILLY
            if gender == "women":
                categories = ["layered_kurtis", "shawl_sets", "long_cardigans"]
            else:
                categories = ["light_jackets", "full_sleeve_shirts", "hoodies"]

        else:   # COLD
            if gender == "women":
                categories = ["wool_kurtas", "heavy_shawls", "winter_coats"]
            else:
                categories = ["wool_sweaters", "thermal_sets", "heavy_jackets"]
    
    return render_template(
        "index.html",
        comfort=comfort_score,
        categories=categories,
        gender=gender,
        place=place,
        category_count=len(categories)
    )

@app.route("/category/<name>")
def category(name):
    with open("outfits.json") as f:
        data = json.load(f)
    return render_template("category.html", title=name.capitalize(), items=data.get(name, []))

@app.route("/buy")
def buy():
    url = request.args.get("url")
    return redirect(url or "/")

if __name__ == "__main__":
    app.run(debug=True)
