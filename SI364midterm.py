###############################
####### SETUP (OVERALL) #######
###############################

## Import statements
# Import statements
import os
from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError # Note that you may need to import more here! Check out examples that do what you want to figure out what.
from wtforms.validators import Required # Here, too
from flask_sqlalchemy import SQLAlchemy
import requests
import json

## App setup code
app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = 'hardtoguessstring'


## All app.config values
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://halliekaufman@localhost/hkaufmidterm'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Statements for db setup (and manager setup if using Manager)
db = SQLAlchemy(app)

######################################
######## HELPER FXNS (If any) ########
######################################




##################
##### MODELS #####
##################


class Location(db.Model):
    __tablename__ = 'Location'
    id = db.Column(db.Integer, primary_key= True)
    city = db.Column(db.String)
    state = db.Column(db.String)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('Names.id'))
    def __repr__(self):
        return '{} is in {}, {} '.format(self.restaurant_id, self.city, self.state)

class Restaurants(db.Model):
    __tablename__ = 'Names'
    id = db.Column(db.Integer, primary_key = True)
    restaurant_name = db.Column(db.String)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    pricerange = db.Column(db.Integer)
    reserverurl= db.Column(db.String)
    def __repr__(self):
        return '{} in {}, {}| ID: {}'.format(self.restaurant_name, self.cityname, self.state, self.id)

###################
###### FORMS ######
###################

class RestaurantName(FlaskForm):
    restaurant_name = StringField('Enter a restaurant name', validators = [Required()])
    submit = SubmitField('Submit')

class LocationForm(FlaskForm):
    city = StringField('What city would you like to find a restaurant in?', validators = [Required()])
    state = StringField('Enter state abbreviation (Must be state abbreviation intials ex: MI)', validators= [Required()])
    pricerange = StringField('What is the price range you are looking for? (Range 1-4)', validators = [Required()])
    submit = SubmitField('Submit')

    def validate_state(self, field):
        if len(self.state.data)>2:
            raise ValidationError('Error! State must be in form of the States abbreviation, not full name.')

    def validate_pricerange(self, field):
        if int((self.pricerange.data))>4:
            raise ValidationError('Error! Number in price range must be 1-4.')

#######################
###### VIEW FXNS ######
#######################

@app.errorhandler(404)
def pagenotfound(e):
    return render_template('404.html'), 404

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/restaurantnames')
def restaurantnames():
    form = RestaurantName()
    return render_template('RestaurantNameForm.html', form= form)

@app.route('/nameresults', methods = ['POST'])
def restaurantnames_results():
    form = RestaurantName()
    if request.method == 'POST' and form.validate_on_submit():
        restaurant_name= form.restaurant_name.data
        url = 'http://opentable.herokuapp.com/api/restaurants?'
        params_diction = {}
        params_diction = {'name': restaurant_name}
        response = requests.get(url, params = params_diction)
        text = response.text
        obj = json.loads(text)['restaurants']
        results = []
        for rest in obj:
            if Restaurants.query.filter_by(restaurant_name=rest['name']).first():
                restaurant = Restaurants.query.filter_by(restaurant_name=rest['name']).first()
                if Location.query.filter_by(city=rest['city']).first():
                    location = Location.query.filter_by(city = rest['city']).first()
                else:
                    location = Location(city = rest['city'], state = rest['state'], restaurant_id = restaurant.id)
            else:
                restaurant = Restaurants(restaurant_name=rest['name'], id= rest['id'], address= rest['address'], city= rest['city'], state= rest['state'], reserverurl = rest['reserve_url'], pricerange = rest['price'])
                db.session.add(restaurant)
                db.session.commit()
                location = Location(city = rest['city'], state = rest['state'], restaurant_id = restaurant.id)
                db.session.add(location)
                db.session.commit()
            results.append((restaurant.restaurant_name, restaurant.address, restaurant.city, restaurant.state, restaurant.reserverurl, restaurant.pricerange))
        return render_template('restaurantnames_results.html', results = results)

    errors = [v for v in form.errors.values()]
    if len(errors) > 0:
        flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))

    return redirect(url_for('restaurantnames'))

@app.route('/locate')
def locate_search():
    form= LocationForm()
    return render_template('LocationForm.html', form=form)

@app.route('/locateresults', methods = ['POST'])
def location_results():
    form = LocationForm()
    if request.method == 'POST' and form.validate_on_submit():
        city = form.city.data
        state= form.state.data
        pricerange= form.pricerange.data
        url = 'http://opentable.herokuapp.com/api/restaurants?'
        params_diction = {}
        params_diction= {'city': city, 'state': state, 'price': pricerange}
        response = requests.get(url, params = params_diction)
        text = response.text
        obj = json.loads(text)['restaurants']
        results = []
        for rest in obj:
            if Restaurants.query.filter_by(restaurant_name=rest['name']).first():
                restaurant = Restaurants.query.filter_by(restaurant_name=rest['name']).first()
                if Location.query.filter_by(city=rest['city']).first():
                    location = Location.query.filter_by(city = rest['city']).first()
                else:
                    location = Location(city = rest['city'], state = rest['state'], restaurant_id = restaurant.id)
            else:
                restaurant = Restaurants(restaurant_name=rest['name'], id= rest['id'], address= rest['address'], city= rest['city'], state= rest['state'], reserverurl = rest['reserve_url'], pricerange = rest['price'])
                db.session.add(restaurant)
                db.session.commit()
                location = Location(city = rest['city'], state = rest['state'], restaurant_id = restaurant.id)
                db.session.add(location)
                db.session.commit()
            results.append((restaurant.restaurant_name, restaurant.address, restaurant.city, restaurant.state, restaurant.reserverurl, restaurant.pricerange))
        return render_template('location_results.html', form= form, results= results)
    # errors = [v for v in form.errors.values()]
    # if len(errors) > 0:
    #     flash("!!!! ERRORS IN FORM SUBMISSION - " + str(errors))
    return redirect(url_for('locate_search'))

@app.route('/allrestaurants')
def see_restaurants():
    all_restaurants = Restaurants.query.all()
    restaurants = []
    for rest in all_restaurants:
        restaurants.append((rest.restaurant_name, rest.address, rest.city, rest.state, rest.pricerange))
    return render_template('all_restaurants.html', restaurants=restaurants)

@app.route('/all_locations')
def see_locations():
    all_locations = Location.query.all()
    locations = []
    for place in all_locations:
        locations.append((place.city, place.state))
    return render_template('all_locations.html', locations=locations)


## Code to run the application...
if __name__ == '__main__':
    db.create_all() #creates defined models when running the application
    app.run(use_reloader=True, debug=True)

# Put the code to do so here!
# NOTE: Make sure you include the code you need to initialize the database structure when you run the application!
