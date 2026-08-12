from flask import Flask, render_template, request
from main import get_grouped_products, search_products

app = Flask(__name__)

# Registrar filtro personalizado para slugs
@app.template_filter('slugify')
def slugify(s):
    return s.lower().replace(' ', '-')

@app.route('/')
def index():
    query = request.args.get('q')
    if query:
        grouped_products = search_products(query)
    else:
        grouped_products = get_grouped_products()
    
    return render_template('index.html', grouped_products=grouped_products, query=query)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=False)
