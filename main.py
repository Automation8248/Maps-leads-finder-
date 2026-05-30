import requests
import os
import random
import sys

# Environment variables
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# --- CONFIGURATION ---
CITY = "New York" 
# ---------------------

def get_coffee_shop():
    # Validation: Check if API key exists
    if not GOOGLE_API_KEY:
        return "Error: GOOGLE_API_KEY is missing!"

    # Google Places API URL
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=coffee+shops+in+{(CITY)}&key={GOOGLE_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        # Check if Google returned an error
        if data.get('status') != 'OK':
            return f"Google API Error: {data.get('status')} - {data.get('error_message', 'Check your API key/billing')}"

        shops = data.get('results', [])
        
        if shops:
            shop = random.choice(shops)
            name = shop.get('name')
            address = shop.get('formatted_address')
            rating = shop.get('rating', 'N/A')
            place_id = shop.get('place_id')
            map_link = f"https://www.google.com/maps/search/?api=1&query=Google&query_place_id={place_id}"
            
            # Using HTML mode instead of Markdown to avoid parsing errors with special characters
            message = (
                f"☕ <b>Daily Coffee Recommendation in {CITY}</b> ☕\n\n"
                f"<b>Shop:</b> {name}\n"
                f"<b>Rating:</b> ⭐ {rating}\n"
                f"<b>Address:</b> {address}\n\n"
                f'<a href="{map_link}">📍 View on Google Maps</a>'
            )
            return message
            
        return f"No shops found in {CITY}!"
    
    except Exception as e:
        return f"Script Error: {str(e)}"

def send_telegram_message(message):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("Error: Telegram credentials missing!")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML", # Changed to HTML for better reliability
        "disable_web_page_preview": False
    }
    
    res = requests.post(url, data=payload)
    if res.status_code != 200:
        print(f"Telegram Error: {res.text}")

if __name__ == "__main__":
    # Ensure dependencies are installed: pip install requests
    result_message = get_coffee_shop()
    send_telegram_message(result_message)
    print("Process completed.")
