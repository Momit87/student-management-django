from server import app, db, Student
from faker import Faker

def seed_data():
    fake = Faker()
    students = []

    # Generate 1000 students
    for _ in range(1000):
        student = {
            "name": fake.name(),
            "email": fake.unique.email(),
            "phone": fake.phone_number(),
            "major": fake.random_element(elements=["Computer Science", "Mathematics", "Physics", "Biology", "Engineering"]),
            "cgpa": round(fake.random.uniform(2.0, 4.0), 2)  # CGPA between 2.0 and 4.0
        }
        students.append(student)

    # Insert into the database
    with app.app_context():
        for student in students:
            new_student = Student(
                name=student["name"],
                email=student["email"],
                phone=student["phone"],
                major=student["major"],
                cgpa=student["cgpa"]
            )
            try:
                db.session.add(new_student)
            except Exception as e:
                print(f"Error adding student {student['name']}: {e}")

        db.session.commit()
        print("Database seeded successfully with 1000 students!")

if __name__ == '__main__':
    seed_data()
