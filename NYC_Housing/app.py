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




@app.route('/crime')
def opening():

    """Return Housing Code Violation Data"""
    results = session.query(db.boro_nm, db.cmplnt_fr_dt).all()
     
    borough = [result[0] for result in results]
    

    borough_names = list(Counter(borough).keys())
    crime_count = list(Counter(borough).values())

    trace = {
            "x": borough_names,
            "y": crime_count,
            "type": "bar"
        }

    return jsonify(trace)





if __name__ == '__main__':
   app.run(port = 5001)