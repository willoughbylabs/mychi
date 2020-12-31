from app import app
from models import db
from seed_helpers import generate_train_lines, get_stations

# ##### Setup #####
db.drop_all()
db.create_all()

#  ##### Train Lines #####

lines_list = generate_train_lines()
db.session.add_all(lines_list)
db.session.commit()

# ##### Stations #####

stations_list = get_stations()
db.session.add_all(stations_list)
db.session.commit()
