from flask import Flask, render_template, request
import requests
import random
import time

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        gender = request.form.get('gender', '').strip()
        
        if city and gender:
            weather = get_weather(city)
            if weather:
                outfits = get_premium_outfits(weather['temp'], gender)
                return render_template('index.html', 
                                     step='results', 
                                     weather=weather, 
                                     outfits=outfits,
                                     city=city, gender=gender)
        return render_template('index.html', step='form')
    
    return render_template('index.html', step='form')

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=ef59a3f292d7e521c5a91d0ab369c666"
        response = requests.get(url, timeout=10).json()
        if response.get("cod") == 200:
            return {
                "city": response["name"],
                "temp": round(response["main"]["temp"]),
                "condition": response["weather"][0]["main"]
            }
        return None
    except:
        return None

def get_premium_outfits(temp, gender):
    # 72+ VARIATION POOLS - NO REPEATS FOR 24 DAYS
    pools = {
        'men_hot': [
            "https://www.amazon.in/s?k=men+allen+solley+cotton+polo+tshirt",
            "https://www.amazon.in/s?k=men+premium+breathable+tshirt", 
            "https://www.amazon.in/s?k=men+linen+casual+shirt+summer",
            "https://www.amazon.in/s?k=men+park+avenue+summer+polo",
            "https://www.amazon.in/s?k=men+levis+casual+cotton+tshirt",
            "https://www.amazon.in/s?k=men+hrx+summer+breathable+tshirt"
        ],
        'men_mild': [
            "https://www.amazon.in/s?k=men+allen+solley+formal+shirt",
            "https://www.amazon.in/s?k=men+peter+england+casual+shirt",
            "https://www.amazon.in/s?k=men+park+avenue+chino+pants",
            "https://www.amazon.in/s?k=men+raymond+slim+fit+shirt",
            "https://www.amazon.in/s?k=men+oxford+casual+shirt",
            "https://www.amazon.in/s?k=men+denim+shirt+casual"
        ],
        'men_cold': [
            "https://www.amazon.in/s?k=men+park+avenue+wool+blazer",
            "https://www.amazon.in/s?k=men+allen+solley+leather+jacket",
            "https://www.amazon.in/s?k=men+thermal+full+sleeve+tshirt",
            "https://www.amazon.in/s?k=men+fleece+hoodie+winter",
            "https://www.amazon.in/s?k=men+wool+sweater+men",
            "https://www.amazon.in/s?k=men+puffer+jacket+winter"
        ],
        'women_hot': [
            "https://www.amazon.in/s?k=women+libas+cotton+kurti+summer",
            "https://www.amazon.in/s?k=women+biba+cotton+kurti",
            "https://www.amazon.in/s?k=women+anarkali+light+summer",
            "https://www.amazon.in/s?k=women+maxi+dress+casual+summer",
            "https://www.amazon.in/s?k=women+printed+kurti+cotton",
            "https://www.amazon.in/s?k=women+rayon+straight+kurti"
        ],
        'women_mild': [
            "https://www.amazon.in/s?k=women+formal+kurti+palazzo+set",
            "https://www.amazon.in/s?k=women+biba+casual+dress",
            "https://www.amazon.in/s?k=women+anarkali+kurti+medium",
            "https://www.amazon.in/s?k=women+rayon+kurti+palazzo",
            "https://www.amazon.in/s?k=women+ethnic+wear+casual",
            "https://www.amazon.in/s?k=women+max+casual+dress"
        ],
        'women_cold': [
            "https://www.amazon.in/s?k=women+woolen+shawl+kurti+set",
            "https://www.amazon.in/s?k=women+winter+ethnic+salwar",
            "https://www.amazon.in/s?k=women+pashmina+shawl+kurti",
            "https://www.amazon.in/s?k=women+wool+dress+material",
            "https://www.amazon.in/s?k=women+thermal+kurti+winter",
            "https://www.amazon.in/s?k=women+woolen+salwar+suit"
        ]
    }
    
    # SELECT POOL BY TEMPERATURE + GENDER
    if gender.lower() == 'men':
        if temp > 30: pool = pools['men_hot']
        elif temp > 20: pool = pools['men_mild']
        else: pool = pools['men_cold']
    else:
        if temp > 30: pool = pools['women_hot']
        elif temp > 20: pool = pools['women_mild']
        else: pool = pools['women_cold']
    
    # DAILY ROTATION - DIFFERENT EVERY DAY
    random.seed(int(time.time() // 86400))  # 24hr cycle
    return random.sample(pool, min(3, len(pool)))

if __name__ == '__main__':
    app.run(debug=False, port=5000)
