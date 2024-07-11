from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SelectField
from wtforms.validators import DataRequired, Email
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    mobile = StringField('Phone', validators=[DataRequired()])

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class BloodRequestForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')],
                        validators=[DataRequired()])
    blood_group = SelectField('Blood Group', choices=[('A+', 'A(+ve)'), ('A-', 'A(-ve)'), ('B+', 'B(+ve)'), ('B-', 'B(-ve)'),
                                                      ('AB+', 'AB(+ve)'), ('AB-', 'AB(-ve)'), ('O+', 'O(+ve)'), ('O-', 'O(-ve)')],
                              validators=[DataRequired()])
    age = StringField('Age', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])

    def return_data(self):
        data = self.data
        data["timestamp"] = str(datetime.now().date())
        del data["csrf_token"]
        return data

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])

class UpdateProfileForm(FlaskForm):
    name = StringField('Name')
    age = StringField('Age', validators=[DataRequired()])
    mobile = StringField('Mobile', validators=[DataRequired()])
    profile_image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Update')

    
class UploadProfileImageForm(FlaskForm):
    profile_image = FileField('Profile Image', validators=[DataRequired()])
    submit = SubmitField('Upload')

class SearchBloodForm(FlaskForm):
    blood_group = SelectField('Blood Group', choices=[('A+', 'A(+ve)'), ('A-', 'A(-ve)'), ('B+', 'B(+ve)'), ('B-', 'B(-ve)'),
                                                      ('AB+', 'AB(+ve)'), ('AB-', 'AB(-ve)'), ('O+', 'O(+ve)'), ('O-', 'O(-ve)')],
                              validators=[DataRequired()])
    csrf_token = StringField('CSRF Token')


class BloodDonateForm(FlaskForm):
    blood_group = SelectField('Blood Group', choices=[('A+', 'A(+ve)'), ('A-', 'A(-ve)'), ('B+', 'B(+ve)'), ('B-', 'B(-ve)'),
                                                      ('AB+', 'AB(+ve)'), ('AB-', 'AB(-ve)'), ('O+', 'O(+ve)'), ('O-', 'O(-ve)')],
                              validators=[DataRequired()])
    NoOfUnits = SelectField('Number Of Units', choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')],
                            validators=[DataRequired()])

    def return_data(self, _id):
        data = self.data
        data["id"] = _id
        data["timestamp"] = str(datetime.now().date())
        del data["csrf_token"]
        return data
