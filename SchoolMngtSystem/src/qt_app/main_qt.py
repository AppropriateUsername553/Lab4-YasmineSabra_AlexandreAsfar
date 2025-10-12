import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout
from src.qt_app.student_form_qt import StudentForm
from src.qt_app.course_form_qt import CourseForm
from src.qt_app.instructor_form_qt import InstructorForm
from src.storage.data_manager import DataManager



class MainWindow(QMainWindow):
    def __init__(self, dm:DataManager):
        self.dm = dm
        super().__init__()
        self.setWindowTitle("School Management System")  # window title
        self.setGeometry(100, 100, 800, 600)  

  
        #tabs for students, instructors, courses
        tabs = QTabWidget()
        self.setCentralWidget(tabs) #to put the tab widget in teh main window

        #student tab
        students_tab = QWidget() #empty container to put in labels, forms, tables..
        tabs.addTab(students_tab, "Students")  #student_tab is teh widget, students is teh text title 
        #inside students tab, need to create a layout to add in it the student form widget
        students_layout = QVBoxLayout()
        students_tab.setLayout(students_layout)
        #adding the form into the layout
        student_form = StudentForm(self.dm)
        students_layout.addWidget(student_form)

        #instructor tab 
        instructors_tab = QWidget()
        tabs.addTab(instructors_tab, "Instructors")

        instructor_layout = QVBoxLayout()
        instructors_tab.setLayout(instructor_layout)

        instructor_form = InstructorForm(self.dm)
        instructor_layout.addWidget(instructor_form)

        #courses tab
        courses_tab = QWidget()
        tabs.addTab(courses_tab, "Courses")

        course_layout = QVBoxLayout()
        courses_tab.setLayout(course_layout)

        course_form = CourseForm(self.dm)
        course_layout.addWidget(course_form)




if __name__ == "__main__":
    app = QApplication(sys.argv)  #this is to run 1 application per process 
    dm = DataManager()
    window = MainWindow(dm)  #create the main window
    window.show() # see the window
    sys.exit(app.exec_())  #start the events loop