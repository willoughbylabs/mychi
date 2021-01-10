from flask_wtf import FlaskForm
from wtforms import SelectField
from wtforms.validators import InputRequired


class TransitTrainForm(FlaskForm):
    """ Form for selecting a line, stop, and direction to recieve an arrival prediction. """

    line = SelectField(
        "'L' Line", validators=[InputRequired(message="Please select a train line.")]
    )
    station = SelectField(
        "Station", validators=[InputRequired(message="Please select a station.")]
    )
    direction = SelectField(
        "Direction",
        validators=[InputRequired(message="Please select a direction of travel.")],
    )
