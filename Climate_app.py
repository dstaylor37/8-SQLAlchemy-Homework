#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Flask app
import sqlalchemy
import numpy as np
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

app = Flask(__name__)


# In[2]:


#create SQL engine
engine = create_engine("sqlite:///hawaii.sqlite")


# In[3]:


##refelct an existing database into a new one
Base = automap_base()


# In[4]:


#reflect the tables
Base.prepare(engine, reflect=True)


# In[5]:


#save references to a new table
Measurement = Base.classes.Measurement
Station = Base.classes.station


# In[6]:


#create link between Python and the existing DB
session = Session(engine)


# In[ ]:

# 3. Define what to do when a user hits the precipition route
# * Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.

@app.route("/api/v1.0/prcipitation")
def tobs():
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').order_by(Measurement.date)

    #Create a dictionary based on row data 
    precipitation_values = []
    for p in results:
        prcp_dict = {}
        prcp_dict["date"] = p.date
        prcp_dict["prcp"] = p.prcp
        precipitation_values.append(prcp_dict)
#Return the JSON representation of your dictionary.
    return jsonify(precipitation_values)


# 4. Define what to do when a user hits the station route
@app.route("/api/v.1/stations")
def stations():
    results = session.query(Station.name).all()

    station_names = list(np.ravel(results))
 #Return a JSON list of stations from the dataset.
    return jsonify(station_names)


# 5. Define what to do when a user hits the tobs route
#* query for the dates and temperature observations from a year from the last data point.
@app.route("/api/v1.0/tobs")
def tobs():
    results=session.query(Measurement.tobs).all()

    tobs_values = list(np.ravel(results))
#Return a JSON list of tob values from the dataset.
    return jsonify(tobs_values)

 # Return a json list of the minimum temperature, the average temperature, and the max 
# temperature for a given start or start-end range.
@app.route("/api/v1.0/<start>")
def temperatures_start(start):
    """ Given the start only, calculate TMIN, TAVG, and TMAX for all dates greater than 
        and equal to the start date. 
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).all()
    
    # Convert list of tuples into normal list
    temperatures_start = list(np.ravel(results))

    return jsonify(temperatures_start)

# When given the start and the end date, calculate the TMIN, TAVG, and TMAX for dates 
# between the start and end date inclusive.
@app.route("/api/v1.0/<start>/<end>")
def temperatures_start_end(start, end):
    """ When given the start and the end date, calculate the TMIN, TAVG, 
        and TMAX for dates between the start and end date inclusive.
    """
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
                filter(Measurement.date >= start).\
                filter(Measurement.date <= end).all()
    
    # Convert list of tuples into normal list
    temperatures_start_end = list(np.ravel(results))

    return jsonify(temperatures_start_end)


if __name__ == "__main__":
    app.run(debug=True)   