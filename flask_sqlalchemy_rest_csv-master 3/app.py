from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow 
import os
import json
import csv
import json
import requests
from datetime import datetime
from dateutil.parser import parse


# Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
db_name = 'jefflovesyou.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, db_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Init db
db = SQLAlchemy(app)
# Init ma
ma = Marshmallow(app)

class NYPD(db.Model):
  RowID = db.Column(db.Integer, primary_key=True)
  Latitude = db.Column(db.Integer)
  Longitude = db.Column(db.Integer)
  LAW_CAT_CD = db.Column(db.String(255))
  OFNS_DESC = db.Column(db.String(255))
  CMPLNT_FR_DT = db.Column(db.Date)
  def __init__(self, Latitude, Longitude, LAW_CAT_CD, OFNS_DESC, CMPLNT_FR_DT):
    self.Latitude = Latitude
    self.Longitude = Longitude
    self.LAW_CAT_CD = LAW_CAT_CD
    self.OFNS_DESC = OFNS_DESC
    self.CMPLNT_FR_DT = CMPLNT_FR_DT

class HousingViolations(db.Model):
  RowID = db.Column(db.Integer, primary_key=True)
  Latitude = db.Column(db.Integer)
  Longitude = db.Column(db.Integer)
  ApprovedDate = db.Column(db.Date)
  NOVDescription = db.Column(db.String(255))
  def __init__(self, LatitudeH, LongtitudeH, ApprovedDate, NOVDescription):
    self.Latitude = LatitudeH
    self.Longitude = LongtitudeH
    self.ApprovedDate = ApprovedDate
    self.NOVDescription = NOVDescription

class HousingComplaints(db.Model):
  RowID = db.Column(db.Integer, primary_key=True)
  Zip = db.Column(db.Integer)
  RecievedDate = db.Column(db.Date)
  def __init__(self, Zip, RecievedDate):
    self.Zip = Zip
    self.RecievedDate = RecievedDate

class NYPDSchema(ma.Schema):
  class Meta:
    fields = ('RowID', 'Latitude', 'Longitude', 'LAW_CAT_CD', 'OFNS_DESC', 'CMPLNT_FR_DT')

class HousingViolationsSchema(ma.Schema):
  class Meta:
    fields = ('RowID', 'LatitudeH', 'LongtitudeH', 'ApprovedDate', 'NOVDescription')

class HousingComplaintsSchema(ma.Schema):
  class Meta:
    fields = ('RowID', 'Zip', 'RecievedDate')

# Init schema
nypd_report_schema = NYPDSchema(strict=True)
nypd_reports_schema = NYPDSchema(many=True, strict=True)

hv_report_schema = HousingViolationsSchema(strict=True)
hv_reports_schema = HousingViolationsSchema(many=True, strict=True)

hc_report_schema = HousingComplaintsSchema(strict=True)
hc_reports_schema = HousingComplaintsSchema(many=True, strict=True)

@app.route('/NYPD', methods=['POST'])
def add_NYPD():
  data = json.loads(request.data)
  Latitude = data['Latitude']
  Longitude = data['Longitude']
  LAW_CAT_CD = data['LAW_CAT_CD']
  OFNS_DESC = data['OFNS_DESC']
  date = parse("{} {}".format(data['CMPLNT_FR_DT'], data['CMPLNT_FR_TM']))
  CMPLNT_FR_DT = date

  nypd_report = NYPD(Latitude, Longitude, LAW_CAT_CD, OFNS_DESC, CMPLNT_FR_DT)
  db.session.add(nypd_report)
  db.session.commit()
  return jsonify({'submitted': OFNS_DESC})

@app.route('/HousingViolations', methods=['POST'])
def add_HousingViolations():
  data = json.loads(request.data)
  LatitudeH = data['LatitudeH']
  LongitudeH = data['LongitudeH']
  ApprovedDate = data['ApprovedDate']
  NOVDescription = data['NOVDescription']

  Housing_Violationsreport = HousingViolations(LatitudeH, LongitudeH, ApprovedDate, NOVDescription)
  db.session.add(Housing_Violationsreport)
  db.session.commit()

  return hv_report_schema.jsonify(HousingViolations)

@app.route('/HousingComplaints', methods=['POST'])
def add_HousingComplaints():
  data = json.loads(request.data)
  RowID = data['RowID']
  Zip = data['Zip']
  RecievedDate = data['RecievedDate']

  Housing_Complaintsreport = HousingComplaints(Zip, RecievedDate)
  db.session.add(Housing_Complaintsreport)
  db.session.commit()

  return hc_report_schema.jsonify(HousingComplaints)

@app.route('/')
def ping():
  return jsonify({'Open the path': 'dummy.'})

@app.route('/createdb')
def create_databases():
    db.create_all()
    return jsonify({'created': db_name})

@app.route('/import/nypd/<filename>')
def import_nypd_csv(filename):
    with open(filename, 'r') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            if row['Latitude'] != '' and row['Longitude'] != '':
              to_import = {}
              to_import['Latitude'] = row['Latitude']
              to_import['Longitude'] = row['Longitude']
              to_import['LAW_CAT_CD'] = row['LAW_CAT_CD']
              to_import['OFNS_DESC'] = row['OFNS_DESC']
              to_import['CMPLNT_FR_DT'] = row['CMPLNT_FR_DT']
              to_import['CMPLNT_FR_TM'] = row['CMPLNT_FR_TM']
              results = requests.post('http://localhost:5000/NYPD', data = json.dumps(to_import))
              print(results.text)
            else:
              print("Skipping: {}".format(row))
    return jsonify({'imported': filename})

@app.route('/import/hv/<filename>')
def import_hv_csv(filename):
    with open(filename, 'r') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            to_import = {}
            to_import['LatitudeH'] = row['LatitudeH']
            to_import['LongitudeH'] = row['LongitudeH']
            to_import['ApprovedDate'] = row['ApprovedDate']
            to_import['NOVDescription'] = row['NOVDescription']
            results = requests.post('http://localhost:5000/HousingViolations', data = json.dumps(to_import))
            print(results.text)
    return jsonify({'imported': filename})

@app.route('/import/hc/<filename>')
def import_hc_csv(filename):
    with open(filename, 'r') as csvfile:
        data_reader = csv.DictReader(csvfile)
        for row in data_reader:
            to_import = {}
            to_import['Zip'] = row['Zip']
            to_import['RecievedDate'] = row['RecievedDate']
            results = requests.post('http://localhost:5000/HousingComplaints', data = json.dumps(to_import))
            print(results.text)
    return jsonify({'imported': filename})



# @app.route('/policy/<county>')
# def get_county_policy(county):
#   county_policy = InsurancePolicy.query.filter_by(county=county).all()
#   result = policies_schema.dump(county_policy)
#   return jsonify(result)


# Run Server
if __name__ == '__main__':
  app.run(debug=True)