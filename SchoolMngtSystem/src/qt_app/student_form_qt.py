from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from src.core.modules import Student 
from src.storage.data_manager import DataManager
class StudentForm(QWidget):
    added_student = pyqtSignal(Student)   #notify when a new student is added, the type of data is Stucent Object 
    def __init__(self, dm: DataManager, parent = None):
        self.dm = dm
        super().__init__()
        layout = QVBoxLayout()

        # ID
        self.id_input = QLineEdit()  #QLine is a one line input box 
        layout.addWidget(QLabel("Student ID"))  #addWidget adds on the window 
        layout.addWidget(self.id_input)  #under the first widget, add this
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
        add_student_button = QPushButton("Add Student")
        add_student_button.clicked.connect(self.add_student) #add_student to be defined later
        layout.addWidget(add_student_button)
        
        self.setLayout(layout) #to display in the window

    def add_student(self):
        try:
            # when button is clicked, send data as dictionary
            new_student = Student (
                student_id = self.id_input.text(),
                name = self.name_input.text(),
                email =  self.email_input.text(),
                age = int(self.age_input.text()),
                registered_courses=[]
            )
            #save to data manager
            self.dm.students_data.append(new_student)
            #signal
            self.added_student.emit(new_student) 
            #clearing 
            self.id_input.clear()
            self.name_input.clear()
            self.email_input.clear()
            self.age_input.clear()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))