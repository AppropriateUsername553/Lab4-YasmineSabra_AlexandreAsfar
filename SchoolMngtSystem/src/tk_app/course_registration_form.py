import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.tk_app.student_table import StudentTable

from src.storage.data_manager import DataManager

class CourseRegistrationForm(ttk.Frame):
    def __init__(self, master, dm: DataManager, student_table = None, course_table = None,  **kwargs):
        
        self.dm = dm
        self.student_table = student_table
        self.course_table = course_table 
        super().__init__(master, **kwargs)



        # Student ID
        ttk.Label(self, text="Student ID").grid(row=0, column=0, sticky="w", pady=4)
        self.student_id_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.student_id_var, width=30).grid(row=0, column=1, sticky="ew", pady=4)

        # Course dropdown
        ttk.Label(self, text="Register for Courses").grid(row=1, column=0, sticky="w", pady=4)
        self.course_var = tk.StringVar()
        self.course_dropdown = ttk.Combobox(self, textvariable=self.course_var, state="readonly")
        self.course_dropdown.grid(row=1, column=1, sticky="ew", pady=4)
        self.course_dropdown.bind("<Button-1>", self.update_courses)

    def update_courses(self, event=None):
        self.course_map = {c.course_name: c for c in self.dm.courses_data}
        self.course_dropdown["values"] = list(self.course_map.keys())

        # mapping 
        self.course_map = {}
        for course in self.dm.courses_data:
            self.course_map[course.course_name] = course
        self.course_dropdown["values"] = list(self.course_map.keys())
        self.course_dropdown.set("Select a Course")

        # Register button
        register_btn = ttk.Button(self, text="Register Course", command=self.register_course)
        register_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.columnconfigure(1, weight=1)

    def register_course(self):
        try:         
            matched_student = None
            matched_course = None
            #find the course by name using the mapping
            input_course_name = self.course_var.get()
            matched_course = self.course_map.get(input_course_name)
            #find teh student by ID
            input_student_id = self.student_id_var.get()
            for s in self.dm.students_data:
                if s.student_id == input_student_id:
                        matched_student = s
                        break
            if matched_student is None:
                raise ValueError("ID not found")
            
            matched_student.register_course(matched_course)
            matched_course.add_student(matched_student)
            
            #refreshing the tables

            if self.student_table:
                self.student_table.load_data()
            if self.course_table:
                self.course_table.load_data()

            messagebox.showinfo("Success", f"Student {matched_student.name} registered in {matched_course.course_name}")
            self.student_id_var.set("")
            self.course_dropdown.set("Select a Course")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            