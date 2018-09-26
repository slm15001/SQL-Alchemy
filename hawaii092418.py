# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, and_, func, desc

engine = create_engine("sqlite:///hawaii.sqlite", echo=False)

# Reflect Database into ORM classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()

# Map Measurement class
Measurement = Base.classes.measurement

# Map Station class
Station = Base.classes.station

# create a session
session = Session(engine)


#Flask App
from flask import Flask, jsonify

#Create an app
app = Flask(__name__)

@app.route("/")
def welcome():
    return (
            f"Available Routes:</br>"
            f"/api/v1.0/precipitation</br>"
            f"/api/v1.0/stations</br>"
            f"/api/v1.0/tobs</br>"
            f"/api/v1.0/<start></br>"
            f"/api/v1.0/<end></br>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > '2016-08-13').\
        order_by(Measurement.date).all()

    #convert the results to a dictionary
    prec_data = []
    for measurement in results:
        measurement_dict = {}
        measurement_dict["date"] = measurement.date
        measurement_dict["prcp"] = measurement.prcp
        prec_data.append(measurement_dict)

    return jsonify(prec_data)

@app.route("/api/v1.0/stations")
def stations():

    results =  session.query(Station.name).all()

    stations = []
    for station in results:
        station_dict = {}
        station_dict['name'] = station.name
        stations.append(station_dict)
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    results = session.query(Measurement.tobs, Measurement.date).\
        filter(Measurement.date > '2016-08-13' ).all()

    tobs = []
    for ob in results:
        tobs_dict = {}
        tobs_dict['tobs'] = ob.tobs
        tobs_dict['date'] = ob.date
        tobs.append(tobs_dict)
    return jsonify(tobs)



# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)