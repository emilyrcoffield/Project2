# 1. import 
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime

engine = create_engine("sqlite:///Project2/Data/SQLite/Housing_Code_Violations.sqlite")



# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

#table reference
hcv = Base.classes.housing_code_violations

#Session link
session = Session(engine)

#################################################
# Flask Setup
#################################################


app = Flask(__name__)

@app.route('/hcv')
def opening():

    """Return Housing Code Violation Data"""
    results = session.query(hcv.latitude, hcv.longitude).all()

    return jsonify(results)

if __name__ == '__main__':
   app.run(debug=True)