import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route('/')
def homepage():
    print('Welcome to the Home Page')
    return ('Available routes:')

@app.route('/api/v1.0/precipitation')
def prcp_api():
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    prcp_dict = {}
    for obsv in precipitation:
        prcp_dict[obsv[0]] = obsv[1]
    return jsonify(prcp_dict)