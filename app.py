# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 11:55:28 2020

@author: zdamd
"""
#%%

# 1. import Flask
import numpy as np

from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd
import datetime as dt
from flask import Flask, jsonify
from sqlalchemy.ext.automap import automap_base


#%%

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine, reflect=True)

# Print all of the classes mapped to the Base
Base.classes.keys()


session=Session(engine)

Measurement=Base.classes.measurement
Station=Base.classes.station
#%%
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

                       
#%%
# 3. Define what to do when a user hits the index route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start_date>/<end_date>"
    )

#%%
@app.route("/api/v1.0/precipitation")
def precipitation():
    past12mth_date= dt.date(2017, 8, 23) - dt.timedelta(days=365)
    pcpt_data=session.query(Measurement.date,Measurement.prcp).filter(Measurement.date>=past12mth_date).all()
    
    return jsonify(pcpt_data)


#%%
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    st_result = list(np.ravel(results))
    return jsonify(st_result)


#%%
@app.route("/api/v1.0/tobs")
def tobs():
    past12mth_date= dt.date(2017, 8, 23) - dt.timedelta(days=365)  
    tobs_data=session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date>=past12mth_date).all()
    tobs_result = list(np.ravel(tobs_data))
    return jsonify(tobs_result)


#%%
@app.route("/api/v1.0/<start_date>/<end_date>" )

def dates(start_date, end_date):
     output=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
     filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
     dates_result = list(np.ravel(output))
     return jsonify(dates_result)   
        
        
#%%
if __name__ == "__main__":
    app.run(debug=True)