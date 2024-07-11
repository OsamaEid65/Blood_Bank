from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from hashlib import sha512
from datetime import datetime
from forms import *
import os
from werkzeug.utils import secure_filename
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.config['SECRET_KEY'] = "lkajdghdadkglajkgah1"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blood_bank.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

csrf = CSRFProtect(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

# Define models
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    profile_image = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return f'<User {self.name}>'


class BloodDetail(db.Model):
    __tablename__ = 'blood_details'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)
    NoOfUnits = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user = db.relationship('User')


class BloodRequest(db.Model):
    __tablename__ = 'blood_requests'
    id = db.Column(db.Integer, primary_key=True)
    requester_name = db.Column(db.String(150), nullable=False)
    blood_group = db.Column(db.String(5), nullable=False)


db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    form = LoginForm()
    return render_template('login.html', form=form, error="You need to login to continue")


@app.route("/")
@app.route("/home")
def redirect_index():
    return redirect("/index")


@app.route('/login', methods=["POST", "GET"])
def login_handle():
    form = LoginForm()

    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == sha512(form.password.data.encode()).hexdigest():
            login_user(user)
            return redirect('/myprofile')
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html', form=form)


@app.route("/newreg", methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
        new_user = User(
            email=form.email.data,
            name=form.name.data,
            password=sha512(form.password.data.encode()).hexdigest()
        )
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("User Registered, continue to login")
            return redirect("/login")
        except IntegrityError:
            db.session.rollback()
            flash("Email already registered")
            return render_template("newreg.html", form=form)

    return render_template("newreg.html", form=form)


@app.route("/blooddonated", methods=["POST", "GET"])
@login_required
def donate_blood():
    form = BloodDonateForm()

    if form.validate_on_submit():
        selected_units = form.NoOfUnits.data  # Get the NoOfUnits from the form

        new_donation = BloodDetail(
            user_id=current_user.id,
            blood_group=form.blood_group.data,
            NoOfUnits=int(selected_units),  # Convert to integer
            timestamp=datetime.utcnow()  # Ensure the timestamp is populated
        )
        db.session.add(new_donation)
        db.session.commit()
        flash("Blood donation request successful, kindly visit the nearest center to save someone's life")
        return redirect('/blooddonated')
    
    return render_template('blooddonated.html', form=form)


@app.route("/view_donations", methods=["POST", "GET"])
@login_required
def view_donations():
    data = BloodDetail.query.filter_by(user_id=current_user.id).all()
    return render_template('view_donations.html', data=data)


@app.route("/myprofile")
@login_required
def my_profile():
    form = UpdateProfileForm()  # Assume UpdateProfileForm is imported from forms.py
    return render_template('myprofile.html', user=current_user, form=form)



@app.route("/uploadprofileimage", methods=["GET", "POST"])
@login_required
def upload_profile_image():
    form = UploadProfileImageForm()
    if form.validate_on_submit():
        file = form.profile_image.data
        if file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Update the user's profile image URL in the database
            current_user.profile_image = filename
            db.session.commit()
            flash('Profile image updated successfully.', 'success')
            return redirect(url_for('my_profile'))
    return render_template('uploadprofile_image.html', form=form)


@app.route("/changepwd", methods=["POST", "GET"])
@login_required
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if form.new_password.data != form.confirm_password.data:
            return render_template("changepwd.html", form=form, error="Password and confirm password don't match")

        user = User.query.filter_by(id=current_user.id).first()
        if user.password == sha512(form.old_password.data.encode()).hexdigest():
            user.password = sha512(form.new_password.data.encode()).hexdigest()
            db.session.commit()
            flash("Password changed successfully")
            return render_template('changepwd.html', form=form)
        else:
            return render_template("changepwd.html", form=form, error="Invalid old password")

    return render_template('changepwd.html', form=form)


@app.route("/updatepf", methods=["POST", "GET"])
@login_required
def update_profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        try:
            user = User.query.get(current_user.id)
            if user:
                # Update user data only if the form fields have valid data
                user.name = form.name.data
                user.age = form.age.data
                user.mobile = form.mobile.data
                
                if form.profile_image.data:
                    file = form.profile_image.data
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(file_path)
                    user.profile_image = filename
                
                db.session.commit()
                flash("Profile updated successfully.", "success")
                return redirect(url_for('update_profile'))
            else:
                flash("User not found.", "danger")
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating profile: {str(e)}", "danger")
    else:
        flash("Form validation failed. Please check your input.", "danger")

    # Pre-populate the form with current user data
    form.name.data = current_user.name
    form.age.data = current_user.age if hasattr(current_user, 'age') else ''
    form.mobile.data = current_user.mobile if hasattr(current_user, 'mobile') else ''

    return render_template('updatepf.html', form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/searchblood", methods=["POST", "GET"])
def searchblood():
    form = SearchBloodForm()

    if form.validate_on_submit():
        data = BloodDetail.query.filter_by(blood_group=form.blood_group.data).all()
        if data:
            return render_template("searchblood.html", form=form, data=data)
        else:
            return render_template("searchblood.html", form=form, message="No data found")

    return render_template("searchblood.html", form=form)


@app.route("/bloodrequest", methods=["POST", "GET"])
def bloodrequest():
    form = BloodRequestForm()

    if form.validate_on_submit():
        new_request = BloodRequest(
            requester_name=form.name.data,
            blood_group=form.blood_group.data
        )
        db.session.add(new_request)
        db.session.commit()
        flash("Blood request submitted successfully. We will get back to you soon.")
        return redirect("/bloodrequest")  # Redirect to the same page after successful submission

    return render_template("bloodrequest.html", form=form)


@app.route("/<file>")
def render_file(file):
    return render_template(file + ".html")


if __name__ == '__main__':
    app.run(debug=True)
