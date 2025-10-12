import tkinter as tk
from tkinter import ttk

from src.core.modules import Course
from src.storage.data_manager import DataManager
from tkinter import messagebox

class CourseForm(ttk.Frame):
    def __init__(self, master, dm:DataManager, course_table = None, **kwargs): # master is the main window, dm to store the new inputs. kwargs is for styling
        
        self.dm = dm
        self.course_table = course_table
        super().__init__(master, **kwargs) #initializing the frame
        #labels and entry fields
        # Course Name
        ttk.Label(self, text="Course Name").grid(row=0, column=0, sticky="w", pady=4)
        self.name_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.name_var, width=30).grid(row=0, column=1, sticky="ew", pady=4)
        # Course ID 
        ttk.Label(self, text="Course ID").grid(row=3, column=0, sticky="w", pady=4)
        self.course_id_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.course_id_var, width=30).grid(row=3, column=1, sticky="ew", pady=4)

        # Submit button for course form
        submit_btn = ttk.Button(self, text="Add Course", command=self.add_course)
        submit_btn.grid(row=4, column=0, columnspan=2, pady=10)
        #command expects a collable that takes no parameters, tkinter will call this command when the submit button is pressed 
        self.columnconfigure(1, weight = 1)  

    def add_course(self):
        """Add a new course from the GUI input fields.
    
    Creates a new 'Course' object using input values from the entry fields.
    The course is assigned to the 'courses' list, dropdowns are updated, and the Treeview is refreshed.

    :return: None
    :rtype: None
    """
        try:
            if any(c.course_id == self.course_id_var.get().strip() for c in self.dm.courses_data):
                raise ValueError(f"Course ID {self.course_id_var.get()} already exists.")
            course = Course(
                course_name = self.name_var.get(),
                course_id = self.course_id_var.get(),
                course_instructor = None,
                enrolled_students = []
                )
            self.dm.courses_data.append(course)
            #refreshing tables
            if self.course_table:
                self.course_table.load_data()
            #updating json files
            self.dm.save_data_to_file("startschool_data.json")
            
            #clearing 
            self.name_var.set("")
            self.course_id_var.set("")
            messagebox.showinfo("Success", f"Course {course.course_name} is added successfully.")

        except Exception as e:
            messagebox.showerror("Error", str(e))
 
