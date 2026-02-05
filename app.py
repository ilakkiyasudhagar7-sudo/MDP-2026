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
        comfort_score = round((temp - 15) / 2, 1)  # Simple formula
        
        # Get modest categories (YOUR 5.3 logic)
        if gender == "women" and comfort_score >= 5.5:
            categories = ["cotton_kurtis_long", "anarkali_suits", "palazzo_with_kurti", 
                         "salwar_suits", "maxi_tunics"]
        elif gender == "men" and comfort_score >= 5.5:
            categories = ["cotton_kurtas", "pathani_suits", "chino_pants", "button_shirts"]
    
    return render_template("index.html", comfort=comfort_score, categories=categories,
                         gender=gender, place=place, category_count=len(categories))

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
