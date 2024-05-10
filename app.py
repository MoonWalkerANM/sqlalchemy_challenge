# Import the dependencies.
import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from pathlib import Path
from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB

session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
# Start the route for homepage and list all available routes
@app.route('/')
def home():
    """List all available api routes"""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/EnterStartDate<start><br/>"
        f"/api/v1.0/EnterStartDate<start>/EndDate<end>"
    )

# for precipitation 
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return precipitation for 12 months of data"""
    # Query query to retrieve the last 12 months of precipitation data
    recent_date = session.query(func.max(measurement.date)).scalar()
    recent_date_dt = dt.datetime.strptime(recent_date, '%Y-%m-%d') 
    one_year_ago = recent_date_dt - dt.timedelta(days=365)
    one_year_prcp = session.query(measurement.date, measurement.prcp).filter(measurement.date >= one_year_ago).all() 
    
    session.close()

    # Convert list of tuples into normal list
    one_yr_precipitation = list(np.ravel(one_year_prcp))

    return jsonify(one_yr_precipitation)

# for stations 
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return station list from dataset"""
    # Query query to retrieve the last 12 months of precipitation data
    stations = session.query(measurement.station).distinct().all() 
    
    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(stations))

    return jsonify(station_list)

# for Temperature of the most active station for the previous year of data 
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return date and temperature of the most active station for previous year of data"""
    # Query query to retrieve the last 12 months of temperature with date for USC00519281

    temperature = session.query(measurement.date, measurement.tobs)\
        .filter(measurement.station == 'USC00519281')\
            .filter(measurement.date >='2016-08-24').all() 
    
    session.close()

    # Convert list of tuples into normal list
    active_station_temp = list(np.ravel(temperature))

    return jsonify(active_station_temp)

# Start and End date route
@app.route("/api/v1.0/EnterStartDate<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the min, max, and avg temps >= a given date"""
    # Query query to retrieve the min, max, avg temps >= a given date

    start_stats = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs))\
        .filter(measurement.date >= start).all()
    
    session.close()

    # Convert list of tuples into normal list
    start_info = list(np.ravel(start_stats))

    return jsonify(start_info)


@app.route("/api/v1.0/EnterStartDate<start>/EndDate<end>")
def start_end(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return the min, max, and avg temps >= a given date"""
    # Query query to retrieve the min, max, avg temps >= a given date

    start_end_info = session.query(func.min(measurement.tobs),func.max(measurement.tobs),func.avg(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()

    
    session.close()

    # Convert list of tuples into normal list
    start_info_end = list(np.ravel(start_end_info))

    return jsonify( start_info_end)


if __name__ == '__main__':
    app.run(debug=True)
