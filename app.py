from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

@app.route("/")
def index():
    mars_collection = mongo.db.collection.find_one()
    return render_template("index.html", data=mars_collection)

@app.route("/scrape")
def scraper():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({}, mars_data, upsert=True)
    
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)