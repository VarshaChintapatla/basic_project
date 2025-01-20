from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://flask_user:yourpassword@localhost/flask_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define a model for the submissions table
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    dob = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Submission {self.name}>'

# Route to display the form
@app.route('/')
def form():
    return render_template('form.html')

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    # Get form data
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    gender = request.form['gender']
    dob = request.form['dob']

    # Save to the database
    new_submission = Submission(
        name=name, email=email, phone=phone,
        address=address, gender=gender, dob=dob
    )
    db.session.add(new_submission)
    db.session.commit()

    return "Form submitted successfully!"

# Route to view submissions
@app.route('/view')
def view_submissions():
    # Fetch all submissions from the database
    submissions = Submission.query.all()
    return render_template('view_submissions.html', submissions=submissions)

if __name__ == '__main__':
    db.create_all()  # Create tables if they don't exist
    app.run(debug=True)
