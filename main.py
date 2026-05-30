import requests
import os
import random

# Environment variables (GitHub Secrets se aayenge)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
CITY = "usa" # Aap apni city yahan likh sakte hain

def get_coffee_shop():
    # Google Places API URL
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=coffee+shops+in+{CITY}&key={GOOGLE_API_KEY}"
    
    response = requests.get(url).json()
    shops = response.get('results', [])
    
    if shops:
        # Kisi bhi ek random shop ko select karein
        shop = random.choice(shops)
        name = shop['name']
        address = shop['formatted_address']
        rating = shop.get('rating', 'N/A')
        place_id = shop['place_id']
        map_link = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
        
        return f"☕ *Daily Coffee Recommendation* ☕\n\nShop: {name}\nRating: ⭐{rating}\nAddress: {address}\n\nLink: {map_link}"
    return "No shops found!"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    requests.post(url, data=payload)

if __name__ == "__main__":
    message = get_coffee_shop()
    send_telegram_message(message)
