#Person Class 
class Person:
    def __init__(self, name: str, email: str, age: int):
        self.name = name
        self.email = email
        self.age = age
    #getter and setter for the name attribute
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string.")
        if not value.strip():
            raise ValueError("Name must not be empty.")
        self._name = value
    #getter and setter for the email attribute
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise ValueError("Email must be a string.")
        if not value.strip():
            raise ValueError("Email must not be empty.")
        if not value.endswith("@starschool.com") :
            raise ValueError("Email must end with starschool.com.")
        self._email = value
    #getter and setter for the age attribute
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise ValueError("Age must be an integer.")
        if value < 0:
            raise ValueError("Age must be non-negative.")
        self._age = value
    # The introduce method
    def introduce(self):
        print(f"Hi, my name is {self.name}, {self.age} years old. You can reach me out at {self.email}.")

#Student class
class Student(Person):
    def __init__(self, name, email, age, student_id: str, registered_courses: list):
        super().__init__(name, email, age)
        self.student_id = student_id
        self.registered_courses = registered_courses if registered_courses is not None else []

    # getters and setters for id attribute
    @property
    def student_id(self):
        return self._student_id
    
    @student_id.setter
    def student_id(self, value):
        if not isinstance(value, str):
            raise ValueError("Student IDs must be strings.")
        if not value.strip():
            raise ValueError("Student ID must not be empty.")
        if not value.startswith("S"):
            raise ValueError("Your ID must start with 'S'.")
        self._student_id = value
    #getter and setter for registered courses attribute
    @property
    def registered_courses(self):
        return self._registered_courses
    
    @registered_courses.setter
    def registered_courses(self, value):
        if not isinstance(value, list):
             raise ValueError("Registered courses must be a list")
        for course in value:
            if not isinstance(course, Course):
                raise ValueError("Courses must be a Course Object.")
        self._registered_courses = value  

    # methods for the student class
    def register_course(self, course):
        if not isinstance(course, Course):
            raise ValueError("Courses must be a Course Object.")
        if course in self._registered_courses:
            raise ValueError(f"Student is already registered in {course}.")
        self._registered_courses.append(course)
    def introduce(self):
        print(f"I am {self.name}, a student with ID {self.student_id}.")


    # serialization for the student class
    def to_dict(self) -> dict:
        registered_course_ids = []
        for course in self.registered_courses:
            registered_course_ids.append(course.course_id)
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "age": self.age,
            "registered_courses_ids": registered_course_ids
        }
    
    @classmethod 
    def from_dict(cls, data: dict) -> "Student":
        return cls(
            name=data["name"],
            email=data["email"],
            age=data["age"],
            student_id=data["student_id"],
            registered_courses=[]
        )

# instructor class
class Instructor(Person):
    def __init__(self, name, email, age, instructor_id: str, assigned_courses: list):
        super().__init__(name, email, age)
        self.instructor_id = instructor_id
        self.assigned_courses = assigned_courses if assigned_courses is not None else []
    #getter and setter for id attribute
    @property 
    def instructor_id(self):
        return self._instructor_id
    
    @instructor_id.setter
    def instructor_id(self, value):
        if not isinstance(value, str):
            raise ValueError("Instructor IDs must be strings.")
        if not value.strip():
            raise ValueError("Instructor ID must not be empty.")
        if not value.startswith("I"):
            raise ValueError("Your ID must start with 'I'.")        
        self._instructor_id = value
    #getter and setter for assigned courses attribute
    @property 
    def assigned_courses(self):
        return self._assigned_courses 
    
    @assigned_courses.setter
    def assigned_courses(self, value):
        if not isinstance(value, list):
            raise ValueError("Assigned courses must be a list.")
        for course in value:
            if not isinstance(course, Course):
                raise ValueError("Courses must be Course Objects.")
        self._assigned_courses = value
    #methods for instrutor class
    def assign_course(self, course):
        if not isinstance(course, Course):
            raise ValueError("Assigned Course must be a Course object.")
        if course in self._assigned_courses:
            raise ValueError(f"{course} is already assigned to this instructor.")
        self._assigned_courses.append(course)
    def introduce(self):
        print(f"I am {self.name}, an instructor with ID {self.instructor_id}.")


    # serialization for instructor class
    def to_dict(self) -> dict:
        assigned_course_ids = []
        for course in self.assigned_courses:
            assigned_course_ids.append(course.course_id)
        return {
             "instructor_id": self.instructor_id,
             "name": self.name,
             "email": self.email,
             "age": self.age,
             "assigned_courses_ids": assigned_course_ids
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Instructor":
        return cls(
            name=data["name"],
            email=data["email"],
            age=data["age"],
            instructor_id=data["instructor_id"],
            assigned_courses=[]
        )

#course class
class Course:
    def __init__(self, course_id: str, course_name: str, course_instructor: 'Instructor' = None, enrolled_students: list = None):
        self.course_id = course_id
        self.course_name = course_name
        self.course_instructor = course_instructor
        self.enrolled_students = enrolled_students if enrolled_students is not None else []
    #getter and setter for id attribute
    @property 
    def course_id(self):
        return self._course_id
    
    @course_id.setter
    def course_id(self, value):
        if not isinstance(value, str):
            raise ValueError("Course IDs must be strings.")
        if not value.strip():
            raise ValueError("Course IDs must not be empty.")
        if not value.startswith("C"):
            raise ValueError("Course IDs must start with 'C'.")        
        self._course_id = value
    #getter and setter for course name attribute 
    @property 
    def course_name(self):
        return self._course_name 
    
    @course_name.setter
    def course_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Course name must be a string.")
        if not value.strip():
            raise ValueError("Course name must not be empty.")
        self._course_name = value
    #getter and setter for course instrcutor attribute
    @property 
    def course_instructor(self):
        return self._course_instructor
    
    @course_instructor.setter
    def course_instructor(self, value):
        if value is not None and not isinstance(value, Instructor):
            raise ValueError("Course instructor must be an Instructor object.")
        self._course_instructor = value
    #getter and setter for enrolled students attribute
    @property
    def enrolled_students(self):
        return self._enrolled_students
    
    @enrolled_students.setter
    def enrolled_students(self, value):
        if not isinstance(value, list):
             raise ValueError("Enrolled students must be a list")
        for student in value:
            if not isinstance(student, Student):
                raise ValueError("Enrolled students must be Student objects.")
        self._enrolled_students = value  
    #methods for course class
    def add_student(self, student: 'Student'):
        if not isinstance(student, Student):
            raise ValueError("Only Student objects can be added.")
        if student in self._enrolled_students:
            raise ValueError("This student is already enrolled in the course")
        self._enrolled_students.append(student)
    
    # serialization for course class
    def to_dict(self) -> dict:
        enrolled_student_ids = []
        for student in self.enrolled_students:
            enrolled_student_ids.append(student.student_id)
        instructor_id = None
        if self.course_instructor is not None:
            instructor_id = self.course_instructor.instructor_id
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "instructor_id": instructor_id,
            "enrolled_students_ids": enrolled_student_ids
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Course":
        return cls(
            course_id=data["course_id"],
            course_name=data["course_name"],
            course_instructor=None,
            enrolled_students=[]
        )


