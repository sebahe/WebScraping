import requests
from bs4 import BeautifulSoup
import json
import time
import os
import re
from datetime import datetime, timedelta
from urllib.parse import urlparse
from html import unescape

BASE_URL = 'https://www.veterinariaalem.com'

# Hardcoded base category URLs
VALID_CATEGORY_URLS = [
    # Alimentos Caninos
    'https://www.veterinariaalem.com/comida-para-perros/agility/',
    'https://www.veterinariaalem.com/comida-para-perros/balanced/',
    'https://www.veterinariaalem.com/comida-para-perros/balanced-natural-recipe/',
    'https://www.veterinariaalem.com/comida-para-perros/bel-can/',
    'https://www.veterinariaalem.com/comida-para-perros/box/',
    'https://www.veterinariaalem.com/comida-para-perros/caro-amici1/',
    'https://www.veterinariaalem.com/comida-para-perros/complete/',
    'https://www.veterinariaalem.com/comida-para-perros/eukanuba1/',
    'https://www.veterinariaalem.com/comida-para-perros/exact/',
    'https://www.veterinariaalem.com/comida-para-perros/excellent1/',
    'https://www.veterinariaalem.com/comida-para-perros/dog-chow/',
    'https://www.veterinariaalem.com/comida-para-perros/dogui/',
    'https://www.veterinariaalem.com/comida-para-perros/fawna/',
    'https://www.veterinariaalem.com/comida-para-perros/homemade/',
    'https://www.veterinariaalem.com/comida-para-perros/hop/',
    'https://www.veterinariaalem.com/comida-para-perros/keddi/',
    'https://www.veterinariaalem.com/comida-para-perros/ken-l/',
    'https://www.veterinariaalem.com/comida-para-perros/maxxium/',
    'https://www.veterinariaalem.com/comida-para-perros/nature/',
    'https://www.veterinariaalem.com/comida-para-perros/nutrique/',
    'https://www.veterinariaalem.com/comida-para-perros/old-prince-equilibrium/',
    'https://www.veterinariaalem.com/comida-para-perros/old-prince-premium/',
    'https://www.veterinariaalem.com/comida-para-perros/old-prince/',
    'https://www.veterinariaalem.com/comida-para-perros/linea-optimum/',
    'https://www.veterinariaalem.com/comida-para-perros/optimus/',
    'https://www.veterinariaalem.com/comida-para-perros/option/',
    'https://www.veterinariaalem.com/comida-para-perros/pedigree/',
    'https://www.veterinariaalem.com/comida-para-perros/premium/',
    'https://www.veterinariaalem.com/comida-para-perros/pro-plan/',
    'https://www.veterinariaalem.com/comida-para-perros/breed-health-nutrition1/',
    'https://www.veterinariaalem.com/comida-para-perros/linea-performance/',
    'https://www.veterinariaalem.com/comida-para-perros/linea-size/',
    'https://www.veterinariaalem.com/comida-para-perros/sieger1/',
    'https://www.veterinariaalem.com/comida-para-perros/supercoat/',
    'https://www.veterinariaalem.com/comida-para-perros/top-nutrition/',
    'https://www.veterinariaalem.com/comida-para-perros/unik/',
    'https://www.veterinariaalem.com/comida-para-perros/whole-earth-farms/',
    
    # Húmedos
    'https://www.veterinariaalem.com/humedos1/homemade2/',
    'https://www.veterinariaalem.com/humedos1/royal-canin/',
    'https://www.veterinariaalem.com/humedos1/pro-plan3/',
    'https://www.veterinariaalem.com/humedos1/balanced2/',
    'https://www.veterinariaalem.com/humedos1/complete2/',
    'https://www.veterinariaalem.com/humedos1/sieger2/',
    'https://www.veterinariaalem.com/humedos1/whiskas1/',
    'https://www.veterinariaalem.com/humedos1/cat-chow1/',
    'https://www.veterinariaalem.com/humedos1/pedigree1/',
    'https://www.veterinariaalem.com/humedos1/optimum1/',
    
    # Alimentos Felinos
    'https://www.veterinariaalem.com/comida-para-gatos/9-lives/',
    'https://www.veterinariaalem.com/comida-para-gatos/agility1/',
    'https://www.veterinariaalem.com/comida-para-gatos/balanced-natural-recipe1/',
    'https://www.veterinariaalem.com/comida-para-gatos/balanced1/',
    'https://www.veterinariaalem.com/comida-para-gatos/bel-cat/',
    'https://www.veterinariaalem.com/comida-para-gatos/box1/',
    'https://www.veterinariaalem.com/comida-para-gatos/cat-chow/',
    'https://www.veterinariaalem.com/comida-para-gatos/complete1/',
    'https://www.veterinariaalem.com/comida-para-gatos/eukanuba/',
    'https://www.veterinariaalem.com/comida-para-gatos/excellent/',
    'https://www.veterinariaalem.com/comida-para-gatos/fawna1/',
    'https://www.veterinariaalem.com/comida-para-gatos/ken-l1/',
    'https://www.veterinariaalem.com/comida-para-gatos/homemade1/',
    'https://www.veterinariaalem.com/comida-para-gatos/hop1/',
    'https://www.veterinariaalem.com/comida-para-gatos/gati/',
    'https://www.veterinariaalem.com/comida-para-gatos/premium1/',
    'https://www.veterinariaalem.com/comida-para-gatos/nutrique1/',
    'https://www.veterinariaalem.com/comida-para-gatos/old-prince-premium1/',
    'https://www.veterinariaalem.com/comida-para-gatos/old-prince-equilibrium1/',
    'https://www.veterinariaalem.com/comida-para-gatos/old-prince1/',
    'https://www.veterinariaalem.com/comida-para-gatos/optimum/',
    'https://www.veterinariaalem.com/comida-para-gatos/pro-plan1/',
    'https://www.veterinariaalem.com/comida-para-gatos/feline-breed-nutrition/',
    'https://www.veterinariaalem.com/comida-para-gatos/performance/',
    'https://www.veterinariaalem.com/comida-para-gatos/linea-size1/',
    'https://www.veterinariaalem.com/comida-para-gatos/sieger/',
    'https://www.veterinariaalem.com/comida-para-gatos/unik1/',
    'https://www.veterinariaalem.com/comida-para-gatos/whiskas/'
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def parse_url_for_categories(url):
    path = urlparse(url).path.strip('/')
    parts = path.split('/')
    
    # Remove trailing numbers and format
    category = re.sub(r'\d+$', '', parts[0].replace('-', ' ')).strip().title()
    subcategory = re.sub(r'\d+$', '', parts[1].replace('-', ' ')).strip().title() if len(parts) > 1 else 'General'
    
    return category, subcategory

def scrape_products(category_url):
    print(f"Scraping category: {category_url}")
    category, subcategory = parse_url_for_categories(category_url)
    try:
        response = requests.get(category_url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = []
        # Find product containers that have variants
        product_containers = soup.find_all('div', class_='js-product-container')
        
        for container in product_containers:
            variants_json = container.get('data-variants')
            if variants_json:
                try:
                    variants = json.loads(unescape(variants_json))
                    # Get product name from title tag or similar
                    name_tag = container.find(class_='js-item-name')
                    base_name = name_tag.text.strip() if name_tag else "Producto sin nombre"
                    
                    variant_list = []
                    for v in variants:
                        if not v.get('available', True):
                            continue
                        price = v.get('price_number_raw', 0) / 100
                        adjusted_price = price * 1.15
                        variant_list.append({
                            'nombre_base': base_name,
                            'nombre_completo': f"{base_name} {v.get('option0', '')}",
                            'foto': f"https:{v.get('image_url', '')}",
                            'precio_ajustado': round(adjusted_price, 2),
                            'presentacion': v.get('option0', 'Unica')
                        })
                    
                    if variant_list:
                        products.append({
                            'nombre_base': base_name,
                            'variantes': variant_list
                        })
                except Exception as e:
                    print(f"Error parsing variants: {e}")
                    continue
        return category, subcategory, products
    except Exception as e:
        print(f"Error scraping {category_url}: {e}")
        return category, subcategory, []

def parse_product(item):
    name = item.get('name', '')
    offers = item.get('offers')
    price = 0.0
    if isinstance(offers, dict):
        price = float(offers.get('price', 0))
    
    # Extract weight/presentation using regex
    weight_match = re.search(r'(\d+(?:\.\d+)?\s?(?:kg|g|gr|unidades|l|ml))', name, re.IGNORECASE)
    weight = weight_match.group(0) if weight_match else 'Unica'
    
    # Normalize name to group variants
    # Remove weight from name for grouping
    base_name = re.sub(r'\d+(?:\.\d+)?\s?(?:kg|g|gr|unidades|l|ml)', '', name, flags=re.IGNORECASE).strip().strip('-')
    # Remove numbers from the name
    base_name = re.sub(r'\d+', '', base_name).strip()
    
    adjusted_price = price * 1.15
    
    return {
        'nombre_base': base_name,
        'nombre_completo': name,
        'descripcion': item.get('description'),
        'foto': item.get('image'),
        'precio_original': price,
        'precio_ajustado': round(adjusted_price, 2),
        'presentacion': weight
    }

def get_grouped_products():
    cache_file = 'products_cache.json'
    scrape_file = 'last_scrape.json'
    
    if os.path.exists(cache_file) and os.path.exists(scrape_file):
        with open(scrape_file, 'r') as f:
            last_scrape_data = json.load(f)
            last_scrape = datetime.fromisoformat(last_scrape_data['last_scrape'])
            
        if datetime.now() - last_scrape < timedelta(days=17):
            with open(cache_file, 'r') as f:
                return json.load(f)
    
    grouped_products = {}
    for cat_url in VALID_CATEGORY_URLS:
        category, subcategory, products = scrape_products(cat_url)
        if products:
            if category not in grouped_products:
                grouped_products[category] = {}
            if subcategory not in grouped_products[category]:
                grouped_products[category][subcategory] = {} # Cambiado a diccionario
            
            for p in products:
                base_name = p['nombre_base']
                if base_name not in grouped_products[category][subcategory]:
                    grouped_products[category][subcategory][base_name] = []
                grouped_products[category][subcategory][base_name].extend(p['variantes'])
        time.sleep(1)
    
    with open(cache_file, 'w') as f:
        json.dump(grouped_products, f)
    with open(scrape_file, 'w') as f:
        json.dump({'last_scrape': datetime.now().isoformat()}, f)
        
    return grouped_products

def get_paginated_products(page=1, per_page=20):
    all_grouped = get_grouped_products()
    flat_products = []
    
    for cat in all_grouped:
        for sub in all_grouped[cat]:
            flat_products.extend(all_grouped[cat][sub].values())
            
    total_products = len(flat_products)
    start = (page - 1) * per_page
    end = start + per_page
    
    return flat_products[start:end], total_products

def search_products(query):
    query = query.lower()
    grouped = get_grouped_products()
    results = {}
    
    for cat, subcategories in grouped.items():
        for subcat, products_map in subcategories.items():
            for base_name, variants in products_map.items():
                # Check if query in base name or any variant name
                match = query in base_name.lower()
                if not match:
                    for v in variants:
                        if query in v['nombre_completo'].lower():
                            match = True
                            break
                if match:
                    if cat not in results: results[cat] = {}
                    if subcat not in results[cat]: results[cat][subcat] = {}
                    results[cat][subcat][base_name] = variants
    return results

