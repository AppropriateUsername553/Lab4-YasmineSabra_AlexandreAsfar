import json
import re 
import tkinter as tk
from tkinter import ttk 
import csv



root = tk.Tk()
root.title("School Management System")
root.geometry("800x600")

def is_valid_email(email):
    """Validate the formate of an email address.
    
    :param email: Email address to validate.
    :type email: str
    :return: True if the email matches the valid pattern, False otherwise.
    :rtype: bool
    
    """
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def is_valid_age(age):
    """Check if age is valid (must be a non-negative integer).

    :param age: Age value to check.
    :type age: int
    :return: True if age is a non-negative integer, False otherwise.
    :rtype: bool
    
    """
    return isinstance(age,int) and age >= 0

def save_people_to_file(people, filename):
    """Save a list of people objects into a JSON file
    
    :param people: list of Person/Student/Intrusctor objects.
    :type people: list
    :param filename: File path to save JSON.
    :type filename: str
    """
    with open(filename, 'w') as f:
        json.dump([person.to_dict() for person in people], f)

def load_people(filename):
    """Load a list of Person objects from a JSON file.

    :param filename: File path containing people data in JSON format.
    :type filename: str
    :return: List of Person objects.
    :rtype: list[Person]
    
    """
    with open(filename, 'r') as f:
        data = json.load(f)
        return [Person(d["name"], d["age"], d["email"]) for d in data]

class Person:
    """Represents a person with a name, age, and email.
    
    :param name: Full name of the person.
    :type name: str
    :param age: Age of the person (must be a non-negative integer).
    :type age: int
    :param _email: Email address of the person.
    :type _email: str
    :raises ValueError: If the email format is invalid or age is negative.
    """
    def __init__(self, name: str, age: int, _email: str):

        """Initialize a Person instance.
        
        :param name: Name of the person.
        :type name: str
        :param age: Age of the person.
        :type age: int
        :param_email: Valid email address.
        :type _email: str
        :raises ValueError: If the email format is invalid or age is negative.
        """
        if not is_valid_email(_email):
            raise ValueError("Invalid email format")
        if not is_valid_age(age):
            raise ValueError("Age must be a non-negative integer")
        self.name = name
        self.age = age
        self._email = _email  # Private attribute

    def to_dict(self):
        """Convert the person object to a dictionary.
        
        :return: Dictionary with name, age, and email.
        :rtype: dict
        """
        return {
            "name": self.name,
            "age": self.age,
            "email": self._email
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Person(data["name"], data["age"], data["email"])

    def introduce(self):
        """Introduce the person in a formatted string.
        
        :return: Intrduction sentence including name and age
        :rtype: str
        """
        return f"Hello, my name is {self.name} and I am {self.age} years old."
    
class Student(Person):
    """Represents a student, inheriting from Person.

    :param nameL Full name of the student.
    :type name: str
    :param age: Age of the student.
    :type age: int
    :param _email: Email of the student.
    :type _email: str
    :param student_id: Unique ID for the student.
    :type student_id: str
    :param registered_courses: List of registered course names.
    :type registered_courses: list[str], optional
    
    """
    def __init__(self, name: str, age: int, _email: str, student_id: str, registered_courses=None):
        """Initialize a Student instance.
        
        :param name: Student name.
        :type name: str
        :param age: Student age.
        :type age: int
        :param _email: Student email.
        :type _email: str
        :param student_id: Unique student ID.
        :type student_id: str
        :param registered_courses: List of registered courses
        :type registered_courses: list[str], optional
        """
        super().__init__(name, age, _email)
        self.student_id = student_id
        if registered_courses is None:
            registered_courses = []
        self.registered_courses = registered_courses

    def register_course(self, course: str):
        """Register the student for a new course.

        :param course: The course name to register.
        :type course: str
        :return: Confirmation message.
        :rtype: str
        
        """
        self.registered_courses.append(course)
        return f"{self.name} has registered for the course: {course}"
    
    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "email": self._email,
            "student_id": self.student_id,
            "registered_courses": self.registered_courses
        }
    
    @staticmethod
    def from_dict(data):
        """Create a Student object from dictionary.

        :param data: Dictionary with student data.
        :type data: dict
        :return: Student object.
        :rtype: Student
        
        """
        return Student(data["name"], data["age"], data["email"], data["student_id"], data.get("registered_courses", []))

class Instructor(Person):
    """Represents an instructor, inheriting from Person"""
    def __init__(self, name: str, age: int, _email: str, instructor_id: str, assigned_courses=None):

        """Initialize an Instructor object.
        
        :param name: Instructor name.
        :type name: str 
        :param age: Instructor age.
        :type age: int
        :param _email: Instructor email.
        :type _email: str
        :param instructor_id: Unique instructor ID.
        :type instructor_id: str
        :param assigned_courses: List of assigned courses.
        :type assigned_courses: list[str], optional
        """
        super().__init__(name, age, _email)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses if assigned_courses is not None else []

    def assign_course(self, course: str):
        """Assign a course to the instructor.

        :param course: Course name to assign.
        :type course: str
        return: Confirmation message.
        :rtype: str
        
        """
        self.assigned_courses.append(course)
        return f"{self.name} is now teaching the course: {course}"
    
    def to_dict(self):
        """Convert instructor object to a dictionary.

        :return: Dictionary with instructor attributes.
        :rtype: dict
        
        """
        return {
            "name": self.name,
            "age": self.age,
            "email": self._email,
            "instructor_id": self.instructor_id,
            "assigned_courses": self.assigned_courses
        }
    
    @staticmethod
    def from_dict(data):
        """Create an Instructor object from dictionary.

        :param data: Dictionary with instructor data.
        :type data: dict
        :return: Instructor object.
        :rtype: Instructor
        
        """
        return Instructor(data["name"], data["age"], data["email"], data["instructor_id"], data.get("assigned_courses", []))

class Course:
    """Represents a course with an ID, name, instructor, and enrolled students."""
    def __init__(self, course_id: str, course_name: str, instructor: Instructor, enrolled_students=None):
        """Initialize a Course instance.
        
        :param course_id: Unique identifier for the course.
        :type course_id: str
        :param course_name: Name of the course.
        :type course_name: str
        :param instructor: Instructor teaching the course.
        :type instructor: Instructor
        :param enrolled_students: List of enrolled Student objects.
        :type enrolled_students: list[Student], optional
        """
        self.course_id = course_id
        self.course_name = course_name
        self.instructor = instructor
        self.enrolled_students = enrolled_students if enrolled_students is not None else []

    def add_student(self, student: Student):
        """Enroll a student in the course.
        
        :param student: Student to enroll.
        :type student: Student
        :return: Confirmation message.
        :rtype: str
        """
        self.enrolled_students.append(student)
        return f"{student.name} has been enrolled in {self.course_name}"

    def to_dict(self):
        """Convert course object to a dictionary.
        
        :return: Dictionary with course attributes.
        :rtype: dict
        """
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor_id": self.instructor.instructor_id if self.instructor else None,
            "enrolled_student_ids": [s.student_id for s in self.enrolled_students]
        }

students = []
instructors = []
courses = []

def refresh_treeview():
    """Refresh the Treeview to show current students, instructors and courses.
    
    This function clears all rows in the Treeview and repopulates it with the latest data from global lists: "students", "instructors", and "courses".
    
    :return: None
    :rtype: None
    """
    for item in tree.get_children():
        tree.delete(item)
    for s in students:
        tree.insert("", "end", values=("Student", s.name, s.student_id, ", ".join(s.registered_courses)))
    for i in instructors:
        tree.insert("", "end", values=("Instructor", i.name, i.instructor_id, ", ".join(i.assigned_courses)))
    for c in courses:
        tree.insert("", "end", values=("Course", c.course_name, c.course_id, c.instructor.name if c.instructor else "None"))


def add_student():
    """Add a new student from the GUI input fields.
    
    Retrieves input values from the entry fields, validates them, 
    and creates a new 'Student' object 
    if valid. The sutdent is then added to the
    'students' list and displayed in the Treeview.

    :return: None
    :rtype: None
    raises ValueError: If any input field is empty or age is not a non-negative integer.
    """
    name = student_name_entry.get()
    age_str = student_age_entry.get()
    email = student_email_entry.get()
    student_id = student_id_entry.get()
    if not name or not age_str or not email or not student_id:
        print("All fields required.")
        return
    try:
        age = int(age_str)
    except ValueError:
        print("Age must be an integer.")
        return
    try:
        student = Student(name, age, email, student_id)
        students.append(student)
        refresh_treeview()
    except ValueError as e:
        print(e)

def add_instructor():
    """Add a new instructor from the GUI input fields.
    
    Retrieves input values from the entry fields, validates them, 
    and creates a new 'Instructor' object if valid. The instructor is then
    added to the 'instructors' list and displayed in the Treeview.

    :return: None
    :rtype: None
    :raises ValueError: If any input field is empty or age is not a non-negative integer.
    """
    name = instructor_name_entry.get()
    age = int(instructor_age_entry.get())
    email = instructor_email_entry.get()
    instructor_id = instructor_id_entry.get()
    try:
        instructor = Instructor(name, age, email, instructor_id)
        instructors.append(instructor)
        tree.insert("", "end", values=("Instructor", instructor.name, instructor.instructor_id, ", ".join(instructor.assigned_courses)))
        refresh_treeview()
    except ValueError as e:
        print(e)


instructor_frame = tk.LabelFrame(root, text="Add Instructor")
instructor_frame.pack(fill="x", padx=10, pady=5)

tk.Label(instructor_frame, text="Name").grid(row=0, column=0)
instructor_name_entry = tk.Entry(instructor_frame)
instructor_name_entry.grid(row=0, column=1)

tk.Label(instructor_frame, text="Age").grid(row=1, column=0)
instructor_age_entry = tk.Entry(instructor_frame)
instructor_age_entry.grid(row=1, column=1)

tk.Label(instructor_frame, text="Email").grid(row=2, column=0)
instructor_email_entry = tk.Entry(instructor_frame)
instructor_email_entry.grid(row=2, column=1)

tk.Label(instructor_frame, text="Instructor ID").grid(row=3, column=0)
instructor_id_entry = tk.Entry(instructor_frame)
instructor_id_entry.grid(row=3, column=1)

tk.Button(instructor_frame, text="Add Instructor", command=add_instructor).grid(row=4, columnspan=2, pady=10)

course_frame = tk.LabelFrame(root, text="Add Course")
course_frame.pack(fill="x", padx=10, pady=5)

tk.Label(course_frame, text="Course ID").grid(row=0, column=0)
course_id_entry = tk.Entry(course_frame)
course_id_entry.grid(row=0, column=1)

tk.Label(course_frame, text="Course Name").grid(row=1, column=0)
course_name_entry = tk.Entry(course_frame)
course_name_entry.grid(row=1, column=1)

def add_course():
    """Add a new course from the GUI input fields.
    
    Creates a new 'Course' object using input values from the entry fields.
    The course is assigned to the 'courses' list, dropdowns are updated, and the Treeview is refreshed.

    :return: None
    :rtype: None
    """
    course_id = course_id_entry.get()
    course_name = course_name_entry.get()
    if instructors:
        instructor = instructors[0]  # Assign the first instructor by default
        course = Course(course_id, course_name, instructor)
        courses.append(course)
        update_dropdowns()
        refresh_treeview()
    else:
        print("No instructors available to assign.")

tk.Button(course_frame, text="Add Course", command=add_course).grid(row=2, columnspan=2, pady=10)


def update_dropdowns():
    """
    Update dropdown menus with the latest course names.

    This ensures that both the student course selection dropdown and the instructor assignment dropdown reflect all available courses.

    :return: None
    :rtype: None
    """
    course_names = [course.course_name for course in courses]
    course_dropdown['values'] = course_names
    instructor_course_dropdown['values'] = course_names

def register_course():
    """
    Register the most recently added student to the selected course.

    - ensures a course and a student exist before registration.
    - prevents duplicate registrations for the same course.
    - updates the Treeview to reflect the new registration.

    :return: None
    :rtype: None
    """
    selected_course_name = course_dropdown.get()
    if not students or not selected_course_name:
        return
    student = students[-1]
    if selected_course_name in student.registered_courses:
        print("Student already registered for this course.")
        return
    course = next((c for c in courses if c.course_name == selected_course_name), None)
    if course:
        student.register_course(selected_course_name)
        course.add_student(student)
        refresh_treeview()

def search_records():
    """
    Search for records in the system and update the Treeview with matching results.

    Matches are checked against:
    - Student names and IDs
    - Instructor names and IDs
    - Course names and IDs

    :return: None
    :rtype: None
    """
    query = search_entry.get().lower()
    for item in tree.get_children():
        tree.delete(item)
    for s in students:
        if query in s.name.lower() or query in s.student_id.lower():
            tree.insert("", "end", values=("Student", s.name, s.student_id, ", ".join(s.registered_courses)))
    for instructor in instructors:
        if query in instructor.name.lower() or query in instructor.instructor_id.lower():
            tree.insert("", "end", values=("Instructor", instructor.name, instructor.instructor_id, ", ".join(instructor.assigned_courses)))

    for c in courses:
        if query in c.course_name.lower() or query in c.course_id.lower():
            tree.insert("", "end", values=("Course", c.course_name, c.course_id, c.instructor.name))


def delete_record():
    """
    Delete the selected record from the Treeview and corresponding data list."""
    selected = tree.selection()
    for item in selected:
        tree.delete(item)

def edit_record():
    """
    Edit the selected record in the Treeview and update the corresponding data list.

    :return: None
    :rtype: None
    """
    selected = tree.selection()
    if not selected:
        return
    item = selected[0]
    values = tree.item(item, "values")
    record_type = values[0]
    if record_type == "Student":
        for s in students:
            if s.student_id == values[2]:
                s.name = student_name_entry.get() or s.name
                s.age = int(student_age_entry.get()) if student_age_entry.get() else s.age
                s._email = student_email_entry.get() or s._email
                s.student_id = student_id_entry.get() or s.student_id
                break
    elif record_type == "Instructor":
        for i in instructors:
            if i.instructor_id == values[2]:
                i.name = instructor_name_entry.get() or i.name
                i.age = int(instructor_age_entry.get()) if instructor_age_entry.get() else i.age
                i._email = instructor_email_entry.get() or i._email
                i.instructor_id = instructor_id_entry.get() or i.instructor_id
                break
    refresh_treeview()

def save_data():
    """
    Save all records (students, instructors, courses) to a JSON file.

    the file is named "school_data.json" and contains structured data for easy retrieval.

    :return: None
    :rtype: None
    """
    data = {
        "students": [s.to_dict() for s in students],
        "instructors": [i.to_dict() for i in instructors],
        "courses": [c.to_dict() for c in courses]}
    
    with open("school_data.json", "w") as f:
        json.dump(data, f)

def load_data():
    """
    Load records from a JSON file and populate the Treeview.

    :return: None
    :rtype: None
    """
    with open("school_data.json", "r") as f:
        data = json.load(f)
        for s in data["students"]:
            student = Student(s["name"], s["age"], s["email"], s["student_id"], s["registered_courses"])
            students.append(student)
            tree.insert("", "end", values=("Student", student.name, student.student_id, ", ".join(student.registered_courses)))
        for i in data["instructors"]:
            instructor = Instructor(i["name"], i["age"], i["email"], i["instructor_id"], i["assigned_courses"])
            instructors.append(instructor)
            tree.insert("", "end", values=("Instructor", instructor.name, instructor.instructor_id, ", ".join(instructor.assigned_courses)))
        for c in data["courses"]:
            course = Course(c["course_id"], c["course_name"], next((inst for inst in instructors if inst.instructor_id == c["instructor_id"]), None), [])
            courses.append(course)
            tree.insert("", "end", values=("Course", course.course_name, course.course_id, course.instructor.name if course.instructor else "None"))


# STEP 1: GUI Setup

root = tk.Tk()
root.title("School Management System")
root.geometry("800x600")

student_frame = tk.LabelFrame(root, text="Add Student")
student_frame.pack(fill="x", padx=10, pady=5)

tk.Label(student_frame, text="Name").grid(row=0, column=0)
student_name_entry = tk.Entry(student_frame)
student_name_entry.grid(row=0, column=1)

tk.Label(student_frame, text="Age").grid(row=1, column=0)
student_age_entry = tk.Entry(student_frame)
student_age_entry.grid(row=1, column=1)

tk.Label(student_frame, text="Email").grid(row=2, column=0)
student_email_entry = tk.Entry(student_frame)
student_email_entry.grid(row=2, column=1)

tk.Label(student_frame, text="Student ID").grid(row=3, column=0)
student_id_entry = tk.Entry(student_frame)
student_id_entry.grid(row=3, column=1)

tk.Button(student_frame, text="Add Student", command=add_student).grid(row=4, columnspan=2, pady=10)

course_dropdown = ttk.Combobox(root, values=["Math", "Physics", "History"])
course_dropdown.pack()

tk.Button(root, text="Register Student to Course", command=register_course).pack()

instructor_course_dropdown = ttk.Combobox(root, values=["Math", "Physics", "History"])
instructor_course_dropdown.pack()

def assign_course():
    """Assign selected course (from instructor_course_dropdown) to the latest instructor (or prints error).
    
    :return: None
    :rtype: None
    """
    selected_course_name = instructor_course_dropdown.get()
    if not instructors:
        print("No instructors available.")
        return
    if not selected_course_name:
        print("No course selected.")
        return
    instructor = instructors[-1]  # simple behaviour: assign to last added instructor
    if selected_course_name in instructor.assigned_courses:
        print("Instructor already assigned to this course.")
        return
    instructor.assign_course(selected_course_name)
    # if the course exists, update its instructor
    course = next((c for c in courses if c.course_name == selected_course_name), None)
    if course:
        course.instructor = instructor
    refresh_treeview()

tk.Button(root, text="Assign Instructor", command=assign_course).pack()

tree = ttk.Treeview(root, columns=("Type", "Name", "ID", "Courses"), show='headings')
tree.heading("Type", text="Type")
tree.heading("Name", text="Name")
tree.heading("ID", text="ID")
tree.heading("Courses", text="Courses")
tree.pack(fill="both", expand=True)

search_entry = tk.Entry(root)
search_entry.pack()

tk.Button(root, text="Search", command=search_records).pack()

tk.Button(root, text="Edit Selected", command=edit_record).pack()
tk.Button(root, text="Delete Selected", command=delete_record).pack()

def export_to_csv():
    """
    Export all records to a CSV file named 'school_records.csv'.

    The exported file contains rows for students, instructors, and courses with relevant details.

    :return: None
    :rtype: None
    """
    with open("school_records.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Type", "Name", "ID", "Courses"])
        for s in students:
            writer.writerow(["Student", s.name, s.student_id, ", ".join(s.registered_courses)])
        for i in instructors:
            writer.writerow(["Instructor", i.name, i.instructor_id, ", ".join(i.assigned_courses)])
        for c in courses:
            writer.writerow(["Course", c.course_name, c.course_id, c.instructor.name if c.instructor else "None"])
    print("Exported to school_records.csv")

tk.Button(root, text="Save Data", command=save_data).pack()
tk.Button(root, text="Load Data", command=load_data).pack()
tk.Button(root, text="Export to CSV", command=export_to_csv).pack()

root.mainloop()