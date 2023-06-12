# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import func
import numpy as np

#################################################
# Database Setup
#################################################

engine = create_engine('sqlite:////Users/lalagilbert/Workspace/sqlalchemy_challenge/Resources/hawaii.sqlite')

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

@app.route("/")
def welcome():
    return (
       f"Welcome to the Hawaii Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/date<br/>"
        f"/api/v1.0/<start>/<end><br/>" 
    )

#Query last year of precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
   prcp_data = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").all()
    
    # Convert the query results to a dictionary
   prcp_dict = {date: prcp for date, prcp in prcp_data}
    
   return jsonify(prcp_dict)
   

#Query of stations over the last year
app.route("/api/v1.0/stations")
def stations():
    stations = session.query(station.station).all()

    #Station list
    stations_list = list(np.ravel(stations))

    return jsonify(stations_list)
    

#Past year query for the most active station
@app.route("/api/v1.0/tobs")
def tobs():
    tobs_data = session.query(measurement.date, measurement.tobs).filter(measurement.date >= "2016-08-23").filter(measurement.station == "USC00519281").all()

     # Convert the query results to a dictionary
    tobs_dict = {date: tobs for date, tobs in tobs_data}
    
    return jsonify(tobs_dict)
    

#Min and max query for temp
@app.route("/api/v1.0/<date>")
def startDate(date):
    start_date_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).filter(measurement.date >= date).all()
    session.close() 

     #list creation of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_date =[]
    for min, avg, max in start_date_results:
        start_date_dict = {}
        start_date_dict["min"] = min
        start_date_dict["average"] = avg
        start_date_dict["max"] = max
        start_date.append(start_date_dict)  
    return jsonify(start_date)
    

# Min and max query for temp for dates between the start date and end date inclusive
@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    start_end_results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
        filter(measurement.date >= start).filter(measurement.date <= end).all()
    session.close()
   #list creation for min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_end = []
    for min, avg, max in start_end_results:
        start_end_dict = {}
        start_end_dict["min_temp"] = min
        start_end_dict["avg_temp"] = avg
        start_end_dict["max_temp"] = max
        start_end.append(start_end_dict) 
    
    return jsonify(start_end)
    
    




if __name__ == '__main__':
    app.run(debug=True)