# Database Schema

## Entity Relationship Diagram for myChi
- [Online link to ERD diagram](https://dbdiagram.io/d/5fe574c99a6c525a03bc42fc)
- [Image of ERD diagram](/assets/images/erd_schema.jpg)


## Lines
- Lines are hardcoded using their route identifiers.
-  [Route Identifiers](/assets/images/route_id.jpg)

## Stations
- After user selects a line, route identifier is used to fetch all stations along that line.
- Data provided by the City of Chicago Open Data portal: [CTA-System Information - List of 'L' Stops](https://dev.socrata.com/foundry/data.cityofchicago.org/8pix-ypme)

## Stops
- Each station has a stop depending on the direction of travel for the train. 
- When user selects a stop, they will have the option to choose which direction.
- Data provided by the City of Chicago Open Data portal: [CTA-System Information - List of 'L' Stops](https://dev.socrata.com/foundry/data.cityofchicago.org/8pix-ypme)

## Arrival Time Predictions
- Using the stop ID, predictions for the next arriving train(s) can be fetched.
- Data provided by the Chicago Transit Authority: [Train Tracker API](https://www.transitchicago.com/developers/traintracker/)

## Users
- A table to collect to ID end-users' and their usernames and passwords.

## Users_Stops
- A table to track a user's saved stop IDs. 