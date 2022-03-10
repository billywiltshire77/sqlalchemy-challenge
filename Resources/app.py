from posixpath import split
import numpy as np
import pandas as pd
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
            f'/api/v1.0/tobs <br/>'
            f'/api/v1.0/&lt;start&gt; <br/>'
            f'/api/v1.0/&lt;start&gt/&lt;end&gt <br/>'
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
    station_info = [(row[0], row[1]) for row in stations]
    return jsonify(station_info)

@app.route('/api/v1.0/tobs')
def tobs():
    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.date.fromisoformat(most_recent_date[0])
    one_year = latest_date - dt.timedelta(days=365)
    most_active_stations = session.query(Measurement.station, func.count(Measurement.date)).group_by(Measurement.station).order_by(func.count(Measurement.date).desc()).all()
    most_active_station = most_active_stations[0][0]
    last_year_station = session.query(Measurement.date, Measurement.tobs).filter(Measurement.station == most_active_station).filter(Measurement.date >= one_year).all()
    last_year_data = [(row[0], row[1]) for row in last_year_station]
    return jsonify(last_year_data)

@app.route('/api/v1.0/<start>')
def start_summary(start):
    month, day, year = start.split('-')
    start_date = dt.date(int(year), int(month), int(day))
    sum_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).all()
    min_tob, max_tob, avg_tob = sum_stats[0]
    return jsonify(min_tob, max_tob, avg_tob)

@app.route('/api/v1.0/<start>/<end>')
def range_summary(start, end):
    s_month, s_day, s_year = start.split('-')
    e_month, e_day, e_year = end.split('-')
    start_date = dt.date(int(s_year), int(s_month), int(s_day))
    end_date = dt.date(int(e_year), int(e_month), int(e_day))
    sum_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    min_tob, max_tob, avg_tob = sum_stats[0]
    return jsonify(min_tob, max_tob, avg_tob)

if __name__ == "__main__":
    app.run(debug=True)