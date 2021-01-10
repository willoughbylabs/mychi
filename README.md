# MyChi - A Concise Open Data Dashboard for Chicago

## Visit myChi at [mychi.willoughbylabs.com/](http://mychi.willoughbylabs.com/)

## Welcome!
myChi is a dashboard to display Chicago open data in an at-a-glance, concise format that focuses on the details that matter most. The scope of this first implementation is a train-tracking dashboard. 

## Features
- Real-time transit tracking from the Chicago Transit Authority (CTA).
- Save regularly-visited transit stops to a dashboard to monitor their status. 
- myChi doesn't require registration and saves your dashboard locally.

## How It Helps
During a typical week, transit riders have typical routes and play a typical game of catch-that-train. It is an integral part of a transit rider's journey to know when the next vehicle will arrive or if delayed to pursue an alternative route. Thanks to the CTA's transit tracking, residents have real time data for their decision making. 

With a bustling downtown, there are many Chicagoans face-to-face with their web browsers at the end of a workday. There are apps and sites to look up transit information but this easy-to-read dashboard can quickly display specific lines curtailed to individual commutes. The mantra of this dashboard is to provide real quick info; it is opinionated to be fast and assumes the critical details to remove distractions or clutter. 

## How To Use
Retrieve a prediction after selecting a train line, stop, and direction. Predictions can be added to your dashboard. When you revisit the site from the same browser, your dashboard predictions will remain (unless cookies have been cleared). Predictions can be refreshed manually for a single prediction or all predictions on the dashboard.

## Data Usage
- Data kindly provided by the City of Chicago and the Chicago Transit Authority.
- [CTA Train Tracker API](https://www.transitchicago.com/developers/traintracker/)
    - Usage: to display real-time train tracking. 
- [City of Chicago Open Data, List of 'L' Stops](https://dev.socrata.com/foundry/data.cityofchicago.org/8pix-ypme)
    - Usage: to retrieve a list of all stops on a line. 

## Development Tools
myChi is grateful to have used the following free tools:
- Python 3.9, JavaScript, HTML, CSS, Bootstrap
- PostgreSQL
- Flask, Flask-SQLAlchemy, Flask-WTF
- Heroku
- VS Code
- [freeCodeCamp Radio](https://coderadio.freecodecamp.org/)
    
## Future Expansion
- Background refresh of predictions. 
- Registration and cloud storage, to access your dashboard from the web, anywhere. 
- Toggle for accessibility-related alerts for an accessibility-first dashboard. 
- Integrate CTA alerts for predictions. 
- Integrate CTA Twitter commentary for additional details about delays for predictions.
- Enable desktop notifications to alert when time to leave.
- Add attributes to stops (i.e. covered, underground); for those who have multipe route options, can reorder list of selected stops based on attributes and current weather. 
- Conversion into a progressive web application.
- Integrate bus tracking data.
- Add additional Chicago open datasets to similarly display concise, at-a-glance topics of interest (examples: restaurant inspections, filming locations, building permits, street sweeping).