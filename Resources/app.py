import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

engine = create_engine("sqlite:///hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route('/')
def homepage():
    return (f'Welcome to the Home Page <br/>'
            f'Available routes: <br/>'
            f'/api/v1.0/precipitation <br/>'
            f'/api/v1.0/stations <br/>'
            )

@app.route('/api/v1.0/precipitation')
def prcp_api():
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    prcp_dict = {}
    for obsv in precipitation:
        prcp_dict[obsv[0]] = obsv[1]
    return jsonify(prcp_dict)

@app.route('/api/v1.0/stations')
def station_api():
    stations = session.query(Station.station, Station.name). all()
    station_dict = {}
    for station in stations:
        station_dict[station[0]] = station[1]
    return jsonify(station_dict)

@app.route('/api/v1.0/tobs')
def tobs():
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.date.fromisoformat(most_recent_date[0])
    one_year = latest_date - dt.timedelta(days=365)
    most_active_stations = session.query(Measurement.station, func.count(Measurement.date)).group_by(Measurement.station).order_by(func.count(Measurement.date).desc()).all()
    most_active_station = most_active_stations[0][0]
    last_year_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date >= one_year).all()
    tobs_dict = {}
    for obsv in last_year_station:
        tobs_dict[obsv[0]] = obsv[1]
    return jsonify(tobs_dict)

if __name__ == "__main__":
    app.run(debug=True)