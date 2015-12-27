
from flask_wtf import Form

from wtforms import StringField, SubmitField
from wtforms.validators import url, data_required


class ShortURLForm(Form):

    url = StringField('url', validators=[url(), data_required()])
    submit = SubmitField('Shorten')

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

    def validate(self):
        """  performs validation of input  """
        if not Form.validate(self):
            return False
        return True