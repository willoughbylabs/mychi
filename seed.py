from app import app
from models import Line, db

# ##### Setup #####
db.drop_all()
db.create_all()

#  ##### Train Lines #####

red = Line(id="red", name="Red Line")
blue = Line(id="blue", name="Blue Line")
brown = Line(id="brn", name="Brown Line")
green = Line(id="g", name="Green Line")
orange = Line(id="org", name="Orange Line")
purple = Line(id="p", name="Purple Line")
pink = Line(id="pink", name="Pink Line")
yellow = Line(id="y", name="Yellow Line")
# purple_exp = Line(id="pexp", name="Purple Line Express")

db.session.add_all([red, blue, brown, green, orange, purple, pink, yellow])
db.session.commit()
