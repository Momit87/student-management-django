from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    major = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float, nullable=False)

# Route to display the students
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Route to add a new student
@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    major = request.form['major']
    cgpa = request.form['cgpa']

    new_student = Student(name=name, email=email, phone=phone, major=major, cgpa=float(cgpa))
    
    try:
        db.session.add(new_student)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return "Error: The email already exists in the database. Please use a different email.", 400

    return redirect('/')

# Route to delete a student
@app.route('/delete/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    # Uncomment the line below if running for the first time to create the database
    # db.create_all()
    app.run(debug=True)
