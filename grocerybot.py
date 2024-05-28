from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3
import logging
import googlemaps
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Google Maps and OpenAI with keys from environment variables
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
openai.api_key = os.getenv('OPENAI_API_KEY')

# Database connection
conn = sqlite3.connect('grocery_app.db', check_same_thread=False)
conn.row_factory = sqlite3.Row  # This allows us to access columns by name

# Ensure tables exist
conn.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        name TEXT NOT NULL,
        size TEXT NOT NULL,
        price REAL NOT NULL,
        unit TEXT NOT NULL
    )
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phone_number TEXT NOT NULL,
        name TEXT,
        state TEXT DEFAULT 'init',
        budget REAL,
        family_size INTEGER,
        ages TEXT,
        days INTEGER,
        grocery_type TEXT,
        latitude REAL,
        longitude REAL
    )
""")

# Function to generate popular and special items using OpenAI
def generate_items_list(location, category_preference):
    prompt = f"""
    Generate a list of {category_preference} grocery items that are popular in {location}. Include staple foods and other commonly purchased items.
    """
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=100
    )
    items = response.choices[0].text.strip().split('\n')
    return [item.strip() for item in items]

# Function to generate recommendations using OpenAI
def generate_recommendations(user, items):
    budget = user['budget']
    family_size = user['family_size']
    ages = user['ages'].split(',')
    days = user['days']

    # Query products from the database
    product_data = {}
    for item in items:
        product_query = conn.execute(
            "SELECT * FROM products WHERE name LIKE ? ORDER BY price ASC",
            (f"%{item}%",)
        ).fetchone()
        if product_query:
            product_data[item] = {
                "name": product_query["name"],
                "size": product_query["size"],
                "price": product_query["price"],
                "unit": product_query["unit"]
            }

    # Construct the prompt for OpenAI
    prompt = f"""
    You are an assistant helping a user with their grocery shopping. The user has a budget of {budget} Naira, a family size of {family_size} with ages {ages}, and needs groceries for {days} days.

    Consider the following product data and adjust the quantities to fit within the budget:
    """
    for item, data in product_data.items():
        prompt += f"\n- {data['name']} ({data['size']}, {data['price']} Naira per {data['unit']})"

    prompt += """
    Generate a recommended list of items considering the budget and family requirements. Adjust quantities as necessary to fit within the budget. Assume staple items should be prioritized and have larger quantities.
    """

    # Use OpenAI to generate recommendations
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )

    recommendations = response.choices[0].text.strip()
    return recommendations

# Function to suggest locations based on user location
def suggest_locations(lat, lng):
    places_result = gmaps.places_nearby(location=(lat, lng), radius=2000, type='grocery_or_supermarket')
    locations_info = []
    for place in places_result['results'][:3]:
        place_id = place['place_id']
        place_details = gmaps.place(place_id=place_id)
        name = place_details['result']['name']
        address = place_details['result']['formatted_address']
        phone_number = place_details['result'].get('formatted_phone_number', 'N/A')
        location_info = f"Name: {name}\nAddress: {address}\nPhone: {phone_number}"
        locations_info.append(location_info)

    # Use OpenAI to format the locations info
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Format the following grocery store information into a user-friendly message:\n{locations_info}",
        max_tokens=200
    )

    formatted_locations = response.choices[0].text.strip()
    return formatted_locations

# Function to handle incoming messages
@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    phone_number = request.values.get('From', '')
    media_url = request.values.get('MediaUrl0', '')
    logging.info(f"Incoming message from {phone_number}: {incoming_msg} with media {media_url}")

    resp = MessagingResponse()
    msg = resp.message()

    try:
        user = conn.execute("SELECT * FROM users WHERE phone_number=?", (phone_number,)).fetchone()

        if incoming_msg == 'start':
            if not user:
                msg.body("Welcome! What's your name?")
                conn.execute("INSERT INTO users (phone_number) VALUES (?)", (phone_number,))
                conn.commit()
            elif not user['name']:
                msg.body("Welcome back! What's your name?")
            else:
                msg.body(f"Hi {user['name']}, let's plan your grocery shopping! Please tell me your budget in Naira (e.g., 5000).")
                conn.execute("UPDATE users SET state='name_set' WHERE phone_number=?", (phone_number,))
                conn.commit()
        elif not user:
            msg.body("Please type 'start' to begin.")
        elif not user['name']:
            user_name = incoming_msg.strip()
            conn.execute("UPDATE users SET name=?, state='name_set' WHERE phone_number=?", (user_name, phone_number))
            conn.commit()
            msg.body(f"Hi {user_name}, let's plan your grocery shopping! Please tell me your budget in Naira (e.g., 5000).")
        elif user['state'] == 'name_set':
            try:
                budget = float(incoming_msg.replace('n', '').replace(',', ''))
                msg.body("Got it! Please tell me your family size (number of people).")
                conn.execute("UPDATE users SET budget=?, state='budget_set' WHERE phone_number=?", (budget, phone_number))
                conn.commit()
            except ValueError:
                msg.body("Please enter a valid budget amount (e.g., 5000).")
        elif user['state'] == 'budget_set':
            try:
                family_size = int(incoming_msg)
                msg.body("Great! Please provide the age of each family member separated by commas (e.g., 38,30,5,1).")
                conn.execute("UPDATE users SET family_size=?, state='family_size_set' WHERE phone_number=?", (family_size, phone_number))
                conn.commit()
            except ValueError:
                msg.body("Please enter a valid family size.")
        elif user['state'] == 'family_size_set':
            try:
                ages = [int(age.strip()) for age in incoming_msg.split(',')]
                if len(ages) == user['family_size']:
                    msg.body("Thank you! For how many days should this budget cover your groceries?")
                    conn.execute("UPDATE users SET ages=?, state='ages_set' WHERE phone_number=?", (incoming_msg, phone_number))
                    conn.commit()
                else:
                    msg.body(f"Please provide exactly {user['family_size']} ages.")
            except ValueError:
                msg.body("Please enter valid ages separated by commas (e.g., 38,30,5,1).")
        elif user['state'] == 'ages_set':
            try:
                days = int(incoming_msg)
                msg.body("Great! What type of groceries are you interested in? (popular, special, popular+special)")
                conn.execute("UPDATE users SET days=?, state='days_set' WHERE phone_number=?", (days, phone_number))
                conn.commit()
            except ValueError:
                msg.body("Please enter a valid number of days.")
        elif user['state'] == 'days_set':
            grocery_type = incoming_msg.lower()
            if grocery_type in ['popular', 'special', 'popular+special']:
                location = "Lagos"  # Assuming Lagos for this example
                items = generate_items_list(location, grocery_type)
                msg.body("Please share your location using WhatsApp's location feature.")
                conn.execute("UPDATE users SET grocery_type=?, state='grocery_type_set', items=? WHERE phone_number=?", (grocery_type, ','.join(items), phone_number))
                conn.commit()
            else:
                msg.body("Please choose from 'popular', 'special', or 'popular+special'.")
        elif user['state'] == 'grocery_type_set' and media_url:
            try:
                location_data = extract_location_from_media(media_url)
                if location_data:
                    lat, lng = location_data
                    conn.execute("UPDATE users SET latitude=?, longitude=?, state='location_set' WHERE phone_number=?", (lat, lng, phone_number))
                    conn.commit()
                    msg.body("Thank you! Generating your grocery recommendations...")

                    items = user['items'].split(',')
                    recommendations = generate_recommendations(user, items)
                    msg.body(f"Here are your grocery recommendations:\n{recommendations}")

                    locations_info = suggest_locations(lat, lng)
                    msg.body(f"Here are some grocery stores near you:\n{locations_info}")
                else:
                    msg.body("Could not extract location from the provided media. Please try again.")
            except Exception as e:
                logging.error(f"Error processing location data: {e}")
                msg.body("An error occurred while processing your location. Please try again.")
        else:
            msg.body("Please follow the instructions to provide the required information.")
    except Exception as e:
        logging.error(f"Error handling message: {e}")
        msg.body("An error occurred. Please try again.")

    return str(resp)

def extract_location_from_media(media_url):
    # Placeholder for actual location extraction logic
    return None

if __name__ == '__main__':
    app.run(debug=True)
