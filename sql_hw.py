import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
start_date = ""
end_date=""
# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

#Flask set-up
app = Flask(__name__)

#Flask routes
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_end_date"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    # Query
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_prcp_data = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp_data.append(prcp_dict)

    return jsonify(all_prcp_data)


@app.route("/api/v1.0/stations")
def station_info():
    session = Session(engine)

    # Query
    results = session.query(Station.station).all()

    session.close()

    all_stations = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def temperature():
    starting_date = dt.date(2016, 8, 23)
    session = Session(engine)
    station_query = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= starting_date).filter(Measurement.station == 'USC00519281').all()
    session.close()
    return jsonify(station_query)


@app.route("/api/v1.0/start_end_date")
def start_end_date():
    print("Enter Start Date ")
    start_date = input()
    print("Enter End Date ")
    end_date = input()
    session = Session(engine)

    active_station_dates = engine.execute(f'SELECT station, MAX(tobs), MIN(tobs), AVG(tobs) FROM Measurement WHERE date >= {start_date} AND date < {end_date}').fetchall()
    session.close()
    return jsonify({'Active Station': [dict(row) for row in active_station_dates]})

if __name__ == "__main__":
    app.run(debug=True)
