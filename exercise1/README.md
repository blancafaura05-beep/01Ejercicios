# 3 Look at the data you downloaded
## a What kind of data is it?
The data belongs to Divvy bike-sharing trips.  
Each row represents a single bike ride taken by a user, including trip duration, start and end times, station locations, and basic user information (gender, birth year, and user type).

## b Possible analyses
Looking at the fields, one can analyze:
- Average trip duration by user type (member vs. casual)
- Most popular start and end stations
- Usage patterns by time of day, weekday, or season
- Gender or age distribution among users
- Evolution of ridership over time

## c Is the data normalized or denormalized?
The dataset is denormalized.  
All trip information (stations, users, durations) is stored in a single table instead of being separated into related tables as a normalized database would do.

## d Is any processing needed before use?
Yes:
- Convert time columns (start_time, end_time, started_at, ended_at) to proper datetime format
- Clean inconsistent column names between years (for example, 2019 Q2 uses long column names)
- Convert numerical fields like tripduration to numeric types
- Handle missing values in gender and birthyear

## e Are there null values? In which fields and why?
Yes, several columns have missing values:
- Gender and birthyear frequently have nulls in 2018–2019 datasets  
    Likely because not all users provide demographic information when registering or because “casual” users are anonymous.
- 2020 Q1 has only 4 missing values in location fields (end_station_name, end_station_id, end_lat, end_lng)  
    Probably due to incomplete GPS or station data during trip recording.

# 7 Think of the need of delivery the data. How you will do it?
To deliver the processed data, I would store the final CSV files in the processed folder, which can easily be shared or uploaded to a cloud service like Google Drive or GitHub. This way, others can access the results without running the code again. If needed, the files could also be compressed into a ZIP file or sent by email.