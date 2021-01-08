from app import app
from models import db, Stop
from seed_helpers import generate_train_lines, generate_stations_list

# ##### Setup #####
# ? How best to implement the suggestion to retry logic that falls back on the previous version, rather than wiping the db each time?
db.drop_all()
db.create_all()

#  ##### Train Lines #####

lines_list = generate_train_lines()
db.session.add_all(lines_list)
db.session.commit()

# ##### Stations #####

stations_list = generate_stations_list()
db.session.add_all(stations_list)
db.session.commit()

# ##### Fix Dan Ryan Spelling Error from API #####

stop = Stop.query.filter(Stop.stop_id == 30088).first_or_404(
    description="Unable to fix Dan Ryan spelling error from API data."
)
stop.station_name = "95th/Dan Ryan"
db.session.commit()
