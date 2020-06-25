from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping


# set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection : 'access MongoDB over HTTP on the native driver port.'
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# define the route for the HTML
@app.route("/")
def index():
    # uses PyMongo to find the “mars” collection in our database
    mars = mongo.db.mars.find_one()
    # tells Flask to return an HTML template using an index.html file
    return render_template("index.html", mars=mars)

# set up our scraping route. 
# scrape updated data when we tell it to from the homepage of our web app
@app.route("/scrape")
def scrape():
    # new variable that points to our Mongo database
    mars = mongo.db.mars
    # created a new variable to hold the newly scraped data
    mars_data = scraping.scrape_all()
    # Update database with new data
    mars.update({}, mars_data, upsert=True)
    return "Scraping Successful!"



if __name__ == "__main__":
   app.run()
