import json
from src.core.modules import Student
from src.core.modules import Instructor
from src.core.modules import Course
class DataManager:
    def __init__(self):
        # lists where inputed data will be saved
        self.students_data = []
        self.instructors_data = []
        self.courses_data = []
    def save_data_to_file(self, file_name: str):
        # data dict to save data in file
        data= {}
        students_dicts = []
        instructors_dicts = []
        courses_dicts =[]
        #convert students objects to dicts
        for student_obj in self.students_data:
            students_dicts.append(student_obj.to_dict())
        data ["students"] = students_dicts
        #convert instructors objects to dicts
        for instructor_obj in self.instructors_data:
            instructors_dicts.append(instructor_obj.to_dict())
        data ["instructors"] = instructors_dicts
        #convert courses objects to dicts
        for course_obj in self.courses_data:
            courses_dicts.append(course_obj.to_dict())
        data ["courses"] = courses_dicts
        #saving everything to json file
        with open(file_name, "w") as f:
            json.dump(data, f, indent=4)

    def load_data_from_file(self, file_name: str):
        self.students_data = []
        self.instructors_data = []
        self.courses_data = []
        try:
            with open(file_name, "r") as f:
                data =json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return

        #creating objects with empty relationships and saving them in mappings from id to object

        student_map ={} # empty dictionary, lookup table to map student ids to student objects
        for student_dict in data.get("students", []): #looping over student dictionaries that we loaded from the json file
            student = Student.from_dict(student_dict) # create a student object from the student dict, but the registered courses is an empty list
            self.students_data.append(student) #add this student object to the students data list
            student_map[student.student_id] = student # adding entry to the map, key is student id, and value is he actual student object, but the objects have empty list
        instructor_map = {}
        for instructor_dict in data.get("instructors", []):
            instructor = Instructor.from_dict(instructor_dict)
            self.instructors_data.append(instructor)
            instructor_map[instructor.instructor_id] = instructor

        course_map = {}
        for course_dict in data.get("courses", []):
            course = Course.from_dict(course_dict)
            self.courses_data.append(course)
            course_map[course.course_id] = course

        #building relationships between the objects using the saved IDs 
        #students ==> courses
        for student_dict in data.get("students", []):#looping over students dicts loaded from file
            student = student_map[student_dict["student_id"]] # access the student id of the student dict, and then access the value of the key equal to this id in the map which is gonna be the object with empty lists 
            for course_id in student_dict.get("registered_courses_ids", []): #loop over the courses ids in the registered courses ids of teh student in the dict not object because in obj its an empty list
                course = course_map.get(course_id) # get the courses object from the map using the ids, we can say course_map[course_id] but better use get() to avoid errors
                if course:
                    #add the course to the list of registered courses in the student object
                    if course not in student.registered_courses:
                        student.registered_courses.append(course)
                    #add the student to the list of enrolled students in the course object
                    if student not in course.enrolled_students:
                        course.enrolled_students.append(student)
                    

        for instructor_dict in data.get("instructors", []): 
            instructor = instructor_map[instructor_dict["instructor_id"]]
            for course_id in instructor_dict.get("assigned_courses_ids", []):
                course = course_map.get(course_id)
                if course:
                    instructor.assigned_courses.append(course)
                    course.course_instructor = instructor