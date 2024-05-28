import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('store.db')
cursor = conn.cursor()

# Create categories table
cursor.execute('''
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
)
''')

# Create items table
cursor.execute('''
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    size TEXT,
    price REAL,
    category_id INTEGER,
    FOREIGN KEY (category_id) REFERENCES categories (id)
)
''')

# Insert categories
categories = [
    "Food Bundles", "Foodstuffs", "Soup & stew ingredients", "Meat, Poultry & Seafood",
    "Fruits & Nuts", "Oils & Spices", "Baby Foods", "Packaged Food", "Baking Ingredients",
    "Drinks & Beverages", "Breakfast", "Household Supplies", "Food Voucher", "Top Selling Products"
]

for category in categories:
    cursor.execute('INSERT OR IGNORE INTO categories (name) VALUES (?)', (category,))

# Insert items
items = [
    ("Pepper Mix Bundle", "", 18626.00, "Food Bundles"),
    ("Pepper - Shombo Grade A (1 Paint bucket,1.5kg)", "1.5kg", 7299.00, "Soup & stew ingredients"),
    ("Pepper Shombo - Grade A (25kg)", "25kg", 120099.00, "Soup & stew ingredients"),
    ("Pepper - Shombo Grade A (1 Dustin Basket, 2kg)", "2kg", 9699.00, "Soup & stew ingredients"),
    ("Pepper - Shombo Grade B (1 Paint bucket,1.5kg)", "1.5kg", 6579.00, "Soup & stew ingredients"),
    ("Pepper - Ata Rodo Grade A (30kg)", "30kg", 133299.00, "Soup & stew ingredients"),
    ("Pepper - Ata Rodo Grade A (1 Paint Bucket, 1.5kg)", "1.5kg", 6759.00, "Soup & stew ingredients"),
    ("Pepper - Ata Rodo Grade A (1 Basket, 2kg)", "2kg", 8979.00, "Soup & stew ingredients"),
    ("Pepper - Ata Rodo Grade B (1 Dustbin Basket, 2kg)", "2kg", 8259.00, "Soup & stew ingredients"),
    ("Tomatoes - Grade A (1 Paint Bucket, 3.5kg)", "3.5kg", 8499.00, "Soup & stew ingredients"),
    ("Tomatoes - Grade B (50kg)", "50kg", 92099.00, "Soup & stew ingredients"),
    ("Tomatoes - Grade A Jos (1 Paint bucket, 3.5kg)", "3.5kg", 8849.00, "Soup & stew ingredients"),
    ("Tomatoes - Grade A Jos (50kg)", "50kg", 110099.00, "Soup & stew ingredients"),
    ("Tomatoes - Grade A (50kg)", "50kg", 120099.00, "Soup & stew ingredients"),
    ("Tomatoes - Grade A Jos (1 Basket, 5Kg)", "5kg", 12599.00, "Soup & stew ingredients"),
    ("Tomatoes - Grade B Jos (1 Dustbin Basket, 5kg)", "5kg", 10099.00, "Soup & stew ingredients"),
    ("Tomatoes - Grade B (1 Paint Bucket, 3.5kg)", "3.5kg", 7099.00, "Soup & stew ingredients"),
    ("Tomatoes - Grade B (1kg)", "1kg", 1939.00, "Soup & stew ingredients"),
    ("Tomatoes - Grade A (1kg)", "1kg", 2499.00, "Soup & stew ingredients"),
    ("Pepper - Tatase Grade A (20kg)", "20kg", 72099.00, "Soup & stew ingredients"),
    ("Tasty Cubes Chicken Flavour Seasoning Powder (1kg)", "1kg", 4719.00, "Oils & Spices"),
    ("Tasty Cubes Chicken Flavour Seasoning Powder (400g)", "400g", 2519.00, "Oils & Spices"),
    ("Lettuce (2 Pieces)", "2 Pieces", 749.00, "Fruits & Nuts"),
    ("Pepper - Ata Rodo Grade B (1kg)", "1kg", 4179.00, "Soup & stew ingredients"),
    ("Pepper - Ata Rodo Grade A (1kg)", "1kg", 4539.00, "Soup & stew ingredients"),
    ("Lemon (5 Pieces)", "5 Pieces", 659.00, "Fruits & Nuts"),
    ("Big Bull Rice (1kg)", "1kg", 1599.00, "Foodstuffs"),
    ("Gino Pepper and Onion Mix Paste - Sachet (1 Roll)", "1 Roll", 1039.00, "Packaged Food"),
    ("President Sliced Cheddar Cheese For Sandwich (200g)", "200g", 5049.00, "Packaged Food"),
    ("Gino Tomato Party Jollof Paste - Sachet (1 Roll)", "1 Roll", 1059.00, "Packaged Food"),
    ("Gino Tomato Party Jollof Paste (1 Carton)", "1 Carton", 9059.00, "Packaged Food"),
    ("Fish - Tilapia (1 Carton, 10kg)", "10kg", 42659.00, "Meat, Poultry & Seafood"),
    ("Green Giant Sweetcorn (340g)", "340g", 1459.00, "Packaged Food"),
    ("Green Giant Sweetcorn (340gx12, 1 Carton)", "1 Carton", 15049.00, "Packaged Food"),
    ("Corn Flour (250g)", "250g", 1019.00, "Baking Ingredients"),
    ("Susan Baking Soda (100g)", "100g", 699.00, "Baking Ingredients"),
    ("Tuwo Rice (1 Mudu)", "1 Mudu", 2619.00, "Foodstuffs"),
    ("Millet (1 Mudu)", "1 Mudu", 1369.00, "Foodstuffs"),
    ("Guinea Corn - White (1 Mudu)", "1 Mudu", 1249.00, "Foodstuffs"),
    ("Guinea Corn - Red (1 Mudu)", "1 Mudu", 1249.00, "Foodstuffs"),
    ("Pepper - Shombo Grade A (1 Paint bucket,1.5kg)", "1.5kg", 7299.00, "Soup & stew ingredients"),
    ("Pepper - Ata Rodo Grade A (1 Paint Bucket, 1.5kg)", "1.5kg", 6759.00, "Soup & stew ingredients"),
    ("Pepper - Tatase Grade A (1 Paint bucket, 1.5kg)", "1.5kg", 5499.00, "Soup & stew ingredients"),
    ("Carrot - Washed (1kg)", "1kg", 2599.00, "Fruits & Nuts"),
    ("Bell Pepper - Mixed (1Kg)", "1kg", 6699.00, "Fruits & Nuts"),
    ("Potato - Irish (1kg)", "1kg", 2599.00, "Fruits & Nuts"),
    ("Beans - Oloyin (1kg)", "1kg", 2539.00, "Foodstuffs"),
    ("Pineapple - Medium (5 Pieces)", "5 Pieces", 5279.00, "Fruits & Nuts"),
    ("Cow Meat or Beef - Boneless (1kg)", "1kg", 5919.00, "Meat, Poultry & Seafood"),
    ("Onions - Red (Big, 1kg)", "1kg", 909.00, "Soup & stew ingredients"),
    ("Fish - Mackerel (1kg)", "1kg", 3269.00, "Meat, Poultry & Seafood"),
    ("Fish - Titus (1kg)", "1kg", 2599.00, "Meat, Poultry & Seafood"),
    ("Fish - Catfish Live (1kg)", "1kg", 3589.00, "Meat, Poultry & Seafood"),
    ("Fish - Catfish Dried (Big, 1kg)", "1kg", 9149.00, "Meat, Poultry & Seafood"),
    ("Soya Bean Powder (500g)", "500g", 1329.00, "Foodstuffs"),
    ("Beans - Olotun Brown (1kg)", "1kg", 1959.00, "Foodstuffs"),
    ("Beans - White (1kg)", "1kg", 1759.00, "Foodstuffs"),
    ("Beans - Black Eye (1kg)", "1kg", 2179.00, "Foodstuffs"),
    ("Ginger Root (1kg)", "1kg", 2159.00, "Soup & stew ingredients"),
    ("Garlic (1kg)", "1kg", 1309.00, "Soup & stew ingredients"),
    ("Fresh Tomato Puree (400g)", "400g", 509.00, "Packaged Food"),
    ("Fresh Tomato Puree (1 Carton)", "1 Carton", 6099.00, "Packaged Food"),
    ("Fish - Titus Frozen (1 Carton, 20kg)", "20kg", 44409.00, "Meat, Poultry & Seafood"),
    ("Fish - Panla Fresh (1kg)", "1kg", 3819.00, "Meat, Poultry & Seafood"),
    ("Fish - Panla Fresh (1 Carton)", "1 Carton", 52019.00, "Meat, Poultry & Seafood"),
    ("Fish - Tilapia Fresh (1kg)", "1kg", 4269.00, "Meat, Poultry & Seafood"),
    ("Fish - Tilapia Frozen (1kg)", "1kg", 4269.00, "Meat, Poultry & Seafood"),
    ("Onions - White (1kg)", "1kg", 1049.00, "Soup & stew ingredients"),
    ("Onions - Red (1kg)", "1kg", 929.00, "Soup & stew ingredients"),
    ("Fish - Kote Fresh (1kg)", "1kg", 3749.00, "Meat, Poultry & Seafood"),
    ("Fish - Hake Fresh (1kg)", "1kg", 4019.00, "Meat, Poultry & Seafood"),
    ("Fish - Panla Frozen (1 Carton, 18kg)", "18kg", 52019.00, "Meat, Poultry & Seafood"),
    ("Fish - Hake Frozen (1 Carton, 20kg)", "20kg", 49079.00, "Meat, Poultry & Seafood"),
    ("Beans - Oloyin (5kg)", "5kg", 12399.00, "Foodstuffs"),
    ("Chicken - Broiler (Full, 1.5kg)", "1.5kg", 5549.00, "Meat, Poultry & Seafood"),
    ("Fish - Panla Fresh (1 Carton, 15kg)", "15kg", 52019.00, "Meat, Poultry & Seafood"),
    ("Chicken - Soft (Full, 1kg)", "1kg", 4489.00, "Meat, Poultry & Seafood"),
    ("Beans - Black Eye (5kg)", "5kg", 12399.00, "Foodstuffs"),
    ("Chicken - Broiler (Full, 1.5kg)", "1.5kg", 5399.00, "Meat, Poultry & Seafood"),
    ("Chicken - Broiler (Full, 1.8kg)", "1.8kg", 6549.00, "Meat, Poultry & Seafood"),
    ("Chicken - Broiler (Full, 2kg)", "2kg", 7159.00, "Meat, Poultry & Seafood"),
    ("Chicken - Broiler (Full, 3kg)", "3kg", 10299.00, "Meat, Poultry & Seafood"),
    ("Turkey (Full, 8kg)", "8kg", 40299.00, "Meat, Poultry & Seafood"),
    ("Fish - Kote Fresh (1 Carton, 20kg)", "20kg", 44409.00, "Meat, Poultry & Seafood"),
    ("Beans - Olotun Brown (5kg)", "5kg", 10699.00, "Foodstuffs"),
    ("Chicken - Soft (Full, 1.5kg)", "1.5kg", 6549.00, "Meat, Poultry & Seafood"),
    ("Fish - Kote Fresh (1 Carton, 20kg)", "20kg", 44409.00, "Meat, Poultry & Seafood"),
    ("Fish - Titus Frozen (1 Carton, 20kg)", "20kg", 43979.00, "Meat, Poultry & Seafood"),
    ("Fish - Panla Fresh (1 Carton, 18kg)", "18kg", 52019.00, "Meat, Poultry & Seafood"),
    ("Fish - Hake Frozen (1 Carton, 20kg)", "20kg", 48709.00, "Meat, Poultry & Seafood"),
    ("Beans - Oloyin (1kg)", "1kg", 2609.00, "Foodstuffs")
]

# Get category ID by name
def get_category_id(name):
    cursor.execute('SELECT id FROM categories WHERE name = ?', (name,))
    return cursor.fetchone()[0]

# Insert items into the database
for name, size, price, category_name in items:
    category_id = get_category_id(category_name)
    cursor.execute('''
        INSERT INTO items (name, size, price, category_id)
        VALUES (?, ?, ?, ?)
    ''', (name, size, price, category_id))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data has been inserted into the database.")
