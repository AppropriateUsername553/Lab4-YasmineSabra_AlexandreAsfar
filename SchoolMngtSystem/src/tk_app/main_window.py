import tkinter as tk
from tkinter import ttk
from src.tk_app.student_form import StudentForm
from src.tk_app.course_registration_form import CourseRegistrationForm
from src.tk_app.instructor_form import InstructorForm
from src.tk_app.course_assignment_form import CourseAssignmentForm
from src.tk_app.course_form import CourseForm
from src.tk_app.student_table import StudentTable
from src.tk_app.instructor_table import InstructorTable
from src.tk_app.course_table import CourseTable
from src.storage.data_manager import DataManager

def main():
    root = tk.Tk() #to create the main window
    root.title("School Management System") #gives the main woindow a title
    root.geometry("800x600") #set the size of the main window 
    #data manager instace
    dm = DataManager()

    try:
        dm.load_data_from_file("starschool_data.json")
    except FileNotFoundError:
        pass 


    #Notebook for tabs
    notebook = ttk.Notebook(root)
    notebook.pack(fill = "both", expand = True)
    #table tabs 

    #student table
    student_tab = StudentTable(notebook, dm)
    notebook.add(student_tab, text="Students Records")
    student_tab.load_data()

    #course table
    course_tab = CourseTable(notebook, dm, student_table=student_tab)
    notebook.add(course_tab, text="Course Records")
    course_tab.load_data()

    #instructor table
    instructor_tab = InstructorTable(notebook, dm)
    notebook.add(instructor_tab, text="Instructors Records")
    instructor_tab.load_data()

    #linking
    course_tab.instructor_table = instructor_tab
    course_tab.student_table = student_tab 
    instructor_tab.course_table = course_tab
    student_tab.course_table = course_tab

    #Forms tabs
    forms_tab = ttk.Frame(notebook)
    notebook.add(forms_tab, text ="Forms")
    #Student Form
    student_form = StudentForm(forms_tab, dm, student_table = student_tab)
    student_form.pack(padx =20, pady=20, fill = "x")
    #Course registration Form
    course_registration_form = CourseRegistrationForm(forms_tab, dm, student_table = student_tab, course_table = course_tab)
    course_registration_form.pack(padx =20, pady=20, fill = "x")
    #Instructor Form
    instructor_form = InstructorForm(forms_tab, dm, instructor_table = instructor_tab)
    instructor_form.pack(padx = 20, pady = 20, fill = "x")
    #Course Assignment Form
    course_assignment_form = CourseAssignmentForm(forms_tab, dm, instructor_table = instructor_tab, course_table = course_tab)
    course_assignment_form.pack(padx =20, pady=20, fill = "x")
    #Course Form
    course_form = CourseForm(forms_tab, dm, course_table = course_tab)
    course_form.pack(padx = 20, pady = 20, fill = "x")
    
    def on_closing():
        dm.save_data_to_file("starschool_data.json")
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)


    #keep the window open, run
    root.mainloop() 
if __name__=="__main__":
    main()

