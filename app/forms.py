from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class OptionInitializeDataForm(FlaskForm):
    contract_id = StringField('Contract ID')

    # User defined fields:
    contract_size = IntegerField('Contract Size', validators=[DataRequired()])
    coll_asset = StringField('Collateral Asset ID', validators=[DataRequired()])
    settle_asset = StringField('Settlement Asset ID', validators=[DataRequired()])
    start = IntegerField('Start (unix timestamp)', validators=[DataRequired()])
    expiry = IntegerField('Expiry (unix timestamp)', validators=[DataRequired()])
    strike_price = IntegerField('Strike Price', validators=[DataRequired()])

    submit = SubmitField('INITIALIZE NEW OPTION')


class OptionImportDataForm(FlaskForm):
    import_data = StringField('Option JSON Data', widget=TextArea(), validators=[DataRequired()])
    submit = SubmitField('IMPORT')
