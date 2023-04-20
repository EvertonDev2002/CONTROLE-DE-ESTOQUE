from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    user = StringField(
        name='user',
        validators=[InputRequired()],
        render_kw={"placeholder": "Usuário"}
    )

    password = PasswordField(
        name='password',
        validators=[InputRequired()],
        render_kw={'placeholder': 'Senha'}
    )

    sumbit = SubmitField("Enviar")
