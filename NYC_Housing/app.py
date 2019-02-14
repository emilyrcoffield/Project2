# 1. import 
from flask import Flask, jsonify, render_template
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine, func, inspect
from collections import Counter
import datetime


app = Flask(__name__)

engine = create_engine("sqlite:///Data/SQLite/crime.sqlite")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

#table reference
db = Base.classes.crime

#Session link
session = scoped_session(sessionmaker(bind=engine))

#################################################
# Flask Setup
#################################################




@app.route('/')
def home():
    return render_template("dashboard-analytics2.html")

@app.route('/Chart.html')
def Chart():
    return render_template("/Chart.html")

@app.route('/index.html')
def index():
    return render_template("/index.html")

@app.route('/Money_Choropleth.html')
def choro():
    return render_template("/Money_Choropleth.html")

@app.route('/Money_Choroplethfinal.html')
def chorofinal():
    return render_template("/Money_Choroplethfinal.html")




@app.route('/crime/<offense>')
def crime_2016(offense):

    """Return # of crimes per borough"""
    results = session.query(db.boro_nm, db.ofns_desc).filter(db.boro_nm != "").filter(db.ofns_desc == offense)
     
    borough = [result[0] for result in results]
    

    boroughs = list(Counter(borough).keys())
    
    crime_count = list(Counter(borough).values())

    trace = {
            "x": boroughs,
            "y": crime_count,
            "type": "bar"
        }

    return jsonify(trace)


@app.route('/offense')
def offenses():

    """Return list of offenses"""
    results = session.query(db.ofns_desc).filter(db.boro_nm != "")
        
    offenses = [result[0] for result in results]
        

    offense_list = list(Counter(offenses).keys())
        
            
    return jsonify(offense_list)



if __name__ == '__main__':
   app.run(port = 5001)