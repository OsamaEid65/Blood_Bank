Blood Bank Project README
Overview
The Blood Bank project is a web application designed to facilitate blood donations and requests. It allows users to register, donate blood, request blood, and manage their profiles. The application uses Flask as the web framework, SQLAlchemy for database interactions, and Flask-Login for user session management.

Features
User Registration and Login: Secure user registration and login functionalities.
Blood Donation: Users can donate blood and record the number of units donated.
Blood Request: Users can request specific blood groups.
Profile Management: Users can update their profile details and upload profile images.
Blood Search: Users can search for available blood units based on blood groups.
Technologies Used
Flask: A micro web framework for Python.
SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
Flask-Login: User session management for Flask.
WTForms: Form rendering and validation library.
SQLite: Database used for storing user and blood donation data.
CSRF Protection: Ensures secure forms with Cross-Site Request Forgery protection.
Installation
Prerequisites
Python 3.x
pip (Python package installer)
Steps
Clone the repository:

bash
Copy code
git clone <repository-url>
cd blood-bank
Create a virtual environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up the database:

bash
Copy code
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
Run the application:

bash
Copy code
flask run
Access the application:
Open your browser and go to http://127.0.0.1:5000.

Application Structure
app.py: Main application file initializing Flask and defining routes and models.
config.py: Configuration file for Flask settings.
forms.py: Defines WTForms forms used in the application.
models.py: SQLAlchemy models for the application.
templates/: HTML templates for rendering web pages.
static/: Static files (CSS, JS, images).
Routes
/login: User login page.
/newreg: User registration page.
/blooddonated: Blood donation form.
/view_donations: View donations made by the current user.
/myprofile: View and update user profile.
/uploadprofileimage: Upload profile image.
/changepwd: Change password.
/updatepf: Update profile details.
/logout: User logout.
/searchblood: Search for blood units.
/bloodrequest: Submit a blood request.
/home or /: Redirect to the home page.
Security Considerations
Sanitizing User Input: Ensure that all user inputs are sanitized to prevent SQL Injection and XSS attacks.
CSRF Protection: Use CSRF tokens for all forms to protect against CSRF attacks.
Password Hashing: Store passwords securely using a hashing algorithm (e.g., SHA-512).
Example Code Snippets
User Registration
python
Copy code
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
Blood Donation
python
Copy code
@app.route("/blooddonated", methods=["POST", "GET"])
@login_required
def donate_blood():
    form = BloodDonateForm()
    if form.validate_on_submit():
        new_donation = BloodDetail(
            user_id=current_user.id,
            blood_group=form.blood_group.data,
            NoOfUnits=form.NoOfUnits.data,
            timestamp=datetime.utcnow()
        )
        db.session.add(new_donation)
        db.session.commit()
        flash("Blood donation request successful, kindly visit the nearest center to save someone's life")
        return redirect('/blooddonated')
    return render_template('blooddonated.html', form=form)
License
This project is licensed under the MIT License.

Contributing
Fork the repository.
Create a new branch (git checkout -b feature-branch).
Make your changes.
Commit your changes (git commit -m 'Add new feature').
Push to the branch (git push origin feature-branch).
Create a new Pull Request.
