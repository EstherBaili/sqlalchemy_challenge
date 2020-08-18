import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

############# Database setup ################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
##############Flask setup####################################
app = Flask(__name__)

@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>"

    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    precipitation = session.query(Measurement.date, Measurement.prcp).all()
    session.close()
    return jsonify(precipitation)


@app.route("/api/v1.0/station")
def stations():
   results = session.query(Station.station).all()
   all_names = list(np.ravel(results))
   return jsonify(all_names)


@app.route("/api/v1.0/tobs")
def tobs():
   tobs = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').\
       filter(Measurement.station == 'USC00519397').all()
   return jsonify(tobs)


@app.route("/api/v1.0/<start>")
def start(start):
   result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
   name =["min_temp", "max_temp", "avg_temp"]
   result = list(zip(name, list(np.ravel(result))))
   return jsonify(result)


@app.route("/api/v1.0/<start>/<end>")
def startend(start, end):
   result = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).\
       filter(Measurement.date <= end).all()
   name =["min_temp", "max_temp", "avg_temp"]
   result = list(zip(name, list(np.ravel(result))))
   return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
