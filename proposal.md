# MyChi - A Concise Open Data Dashboard for Chicago

## Purpose
A dashboard to display Chicago open data in an at-a-glance, concise format that focuses on the details that matter most. The scope of this first capstone is implementing a train-tracking display. 

## Features
- Provide real-time transit tracking and alerts from the Chicago Transit Authority (CTA).
- Allow saving of regularly-visited transit stops to monitor their status. 
- If a route is delayed, displays information from customer alerts suplemented by commentary from the CTA's Twitter account.
- Manual or automatic refresh of data. 

## How It Helps
During a typical week, transit riders have typical routes and play a typical game of catch-that-train. It is an integral part of a transit rider's journey to know when the next vehicle will arrive or if delayed to pursue an alternative route. Thanks to the CTA's transit tracking, residents have real time data for their decision making. 

With a bustling downtown, there are many Chicagoans face-to-face with their web browsers at the end of a workday. There are apps and sites to look up transit information but this easy-to-read dashboard can qucklly display specific lines curtailed to individual commutes. The mantra of this dashboard is to provide real quick info; it is opinionated to be fast and assumes the critical details to remove distractions or clutter. 

When a transit line is delayed, alerts are displayed following a CTA standardized categorization of the delay type. For additional information, the CTA provides supplemental details via Twitter. For riders this requires viewing information in two places to stay fully apprised. This dashboard will integrate information from Twitter when a delay occurs to update riders with additional context. 

## Dashboard Display
- Search for train line and stop.
- Selected train line and stop. 
- Next arriving vehicle(s) - in minutes to arrival as well as date time.
- Customer alerts.
- Additional delay details utilziing CTA Twitter feed.
- Hourly weather - current condition and temperature, precipitation chance, wind speed.

## Data Usage
- [CTA Train Tracker API](https://www.transitchicago.com/developers/traintracker/)
    - Usage: to display real-time train tracking. 
- [Customer Alerts API](https://www.transitchicago.com/developers/alerts/)
    - Usage: to display alerts affecting the line or stop.
- [Twitter API](https://developer.twitter.com/en/docs/twitter-api)
    - Customer alerts often remain static. To provide contextual delay information the CTA often tweets about developments and updates. Usage: to display a feed if an alert is detected for a line.
- Weather API - None currently selected
    - Weather plays a role in deciding what to wear, what to bring, or whether to use the underground stop versus the wind-swept one. Usage: to provide hourly weather data.

## Development Utilities
- Python, Flask, Jinja, HTML
    - Fetch data from APIs and render to viewer. 
    - Make requests and routing.
- Bootstrap, CSS
    - Styling.
- PostgreSQL, SQLAlchemy
    - Store information about transit lines.
    - Store selected lines from visitor if logged in (potential feature, local storage default).
- Flask-WTForms
    - Search for train line and stop.
    - Register and login (potential feature).
- Javascript/AJAX
    - Toggler for automatic or manual refresh.

## Database Schema
![diagram showing relationship between line, stops, and directions tables](assets/images/schema.jpg)
- Lines - Model for storing each train line.
    - id: `INT, PRIMARY KEY`.
    - name: `TEXT NOT NULL` name of line, identified by line color (e.g. blue, red).
- Stops - Model for storing train stops.
    - id: `INT, PRIMARY KEY`.
    - line_id: `INT, FOREIGN KEY NOT NULL` id of the line associated with the stop.
    - direction_id: `INT, FOREIGN KEY NOT NULL` id of the direction for the stop.
    - name: `TEXT NOT NULL` name of the stop.
- Directions - Model for storing travel direction for line and stop.
    - id: `INT, PRIMARY KEY`.
    - heading: `TEXT NOT NULL` defined end station for determining which direction the train is travelling.

## Potential Pain Points
- Twitter integration, querying text to determine if content is related to a specific train line.
- Quantity of APIs, managing requests and how best to store and retrieve data.
- Session storage to retain rider's previously selected lines and stops.
- Design and CSS, dashboards are ideally visually pleasing and UX/UI friendly.
- Auto-retrieval of data and refreshing display without page reload.

## Potential for Expansion
- Add registration and log in to access dashboard and saved widgets from any browser.
- Integrate bus tracking data.
- Add additional Chicago open datasets to similarly display concise, at-a-glance topics of interest (examples: restaurant inspections, filming locations, building permits, street sweeping).
- Convert into a progressive web application.
- Enable desktop notifications (e.g. alert rider when time to leave).

