from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal
from src.core.modules import Course 
from src.storage.data_manager import DataManager 

class CourseForm(QWidget):
    added_course = pyqtSignal(Course)   
    def __init__(self, dm: DataManager, parent = None):
        self.dm = dm
        super().__init__()
        layout = QVBoxLayout()

        # ID
        self.id_input = QLineEdit()  
        layout.addWidget(QLabel("ID"))  
        layout.addWidget(self.id_input)  
        #Name 
        self.name_input = QLineEdit()  
        layout.addWidget(QLabel("Name")) 
        layout.addWidget(self.name_input)  
        #Button
        add_course_button = QPushButton("Add Course")
        add_course_button.clicked.connect(self.add_course) 
        layout.addWidget(add_course_button)
        
        self.setLayout(layout) 

    def add_course(self):
        # when button is clicked, send data as dictionary
        new_course = Course(
            course_id = self.id_input.text(),
            course_name= self.name_input.text(),
            enrolled_students = [],
            course_instructor=None
            
        )
        #save to data manager 
        self.dm.courses_data.append(new_course)
        #signal 
        self.added_course.emit(new_course) 
        #clearing 
        self.id_input.clear()
        self.name_input.clear()
