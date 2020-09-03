import scrape_mars
from flask import Flask, render_template, request
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config['MONGO_URI'] = 'mondodb://localhost:27017/mars_data_scrape'
mongo = PyMongo(app)


##
@app.route('/')
def index():
    
    #
    mars_data_scrape = mongo.db.mars_data_scrape.fine_one()

    #
    return render_template('index.html',mars_data_scrape = mars_data_scrape)


##
@app.route("/scrape")
def scrape():

    #
    mars_data_scrape = scrape_mars.scrape()

    #
    mongo.db.mars_data_scrape.update({}, mars_data_scrape, upsert = True)
    return 'Scrape Finished.'

if __name__ == '__main__':
    app.run(debug=True)