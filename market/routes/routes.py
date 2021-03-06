from market import app
from flask import render_template
from market.models.models import Item
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/about/<username>')
def about_page(username):
    if username == "Abhishek":
        return render_template('AdminPage.html',username = username)
    return render_template('home.html')

@app.route('/market')
def market_page():
    items = Item.query.all()
    return render_template('market.html',items=items)