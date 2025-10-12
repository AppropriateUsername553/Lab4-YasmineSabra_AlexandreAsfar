from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal
from src.core.modules import Instructor
from src.storage.data_manager import DataManager

class InstructorForm(QWidget):
    added_instructor = pyqtSignal(Instructor)   #notify when a new in is added, the type of data is Instructor
    def __init__(self, dm:DataManager, parent = None):
        super().__init__(parent)
        self.dm = dm
        layout = QVBoxLayout()

        # ID
        self.id_input = QLineEdit()  
        layout.addWidget(QLabel("ID"))  
        layout.addWidget(self.id_input)  
        #Name 
        self.name_input = QLineEdit()  
        layout.addWidget(QLabel("Name")) 
        layout.addWidget(self.name_input)  
        #Email
        self.email_input = QLineEdit()  
        layout.addWidget(QLabel("Email")) 
        layout.addWidget(self.email_input)  
        #Age
        self.age_input = QLineEdit()  
        layout.addWidget(QLabel("Age")) 
        layout.addWidget(self.age_input)
        #Button
        add_instructor_button = QPushButton("Add Instructor")
        add_instructor_button.clicked.connect(self.add_instructor) 
        layout.addWidget(add_instructor_button)
        
        self.setLayout(layout) 

    def add_instructor(self):
        # when button is clicked, send data as dictionary
        new_instructor = Instructor(
            instructor_id = self.id_input.text(),
            name = self.name_input.text(),
            email= self.email_input.text(),
            age =  int(self.age_input.text()),
            assigned_courses = []
        )
        #save to data manager 
        self.dm.instructors_data.append(new_instructor)
        #signal
        self.added_instructor.emit(new_instructor) 
        #clearing
        self.id_input.clear()
        self.name_input.clear()
        self.email_input.clear()
        self.age_input.clear()