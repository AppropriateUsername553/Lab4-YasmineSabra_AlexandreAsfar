import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from src.core.modules import *
from src.tk_app.student_table import StudentTable 
from src.tk_app.instructor_table import InstructorTable

from src.storage.data_manager import DataManager

class CourseTable(ttk.Frame):
    def __init__(self, master, dm, student_table = None, instructor_table = None, **kwargs):
        self.dm = dm
        self.student_table = student_table
        self.instructor_table = instructor_table
        super().__init__(master, **kwargs)
        # Search Bar
        ttk.Label(self, text="Search").grid(row=0, column=0, sticky="w", pady=4)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(self, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, sticky="ew", pady=4)

        search_btn = ttk.Button(self, text="Search for Course", command=self.search_records)
        search_btn.grid(row=0, column=2, padx=6)
        self.columnconfigure(1, weight=1)

        # Treeview
        course_columns = ("ID", "Name", "Course Instructor", "Enrolled Students")
        self.tree = ttk.Treeview(self, columns=course_columns, show="headings")
        for attribute in course_columns:
            self.tree.heading(attribute, text=attribute)
            self.tree.column(attribute, width=120, anchor="center")
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Buttons for editing and deleting
        edit_btn = ttk.Button(self, text="Edit", command=self.edit_course)
        edit_btn.grid(row=2, column=0, pady=5)

        delete_btn = ttk.Button(self, text="Delete", command=self.delete_course)
        delete_btn.grid(row=2, column=1, pady=5)

    # helper to select a course
    def select_course(self):
        selected = self.tree.selection()
        if not selected:
            return None
        course_id = self.tree.item(selected[0])["values"][0]  # first column = ID
        for c in self.dm.courses_data:
            if c.course_id == course_id:
                return c
        return None

    # method to edit course
    def edit_course(self):
        course = self.select_course()
        if not course:
            messagebox.showerror("Error", "Please select a course to edit")
            return

        popup = tk.Toplevel(self)
        popup.title("Edit Course")
        popup.geometry("400x200")

        # Pre-fill with current values
        name_var = tk.StringVar(value=course.course_name)
        id_var = tk.StringVar(value=course.course_id)

        ttk.Label(popup, text="Course Name:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(popup, textvariable=name_var, width=30).grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(popup, text="Course ID:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        ttk.Entry(popup, textvariable=id_var, width=30).grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        def save_changes():
            course.course_name = name_var.get()
            course.course_id = id_var.get()
            self.load_data()
            self.student_table.load_data()
            self.instructor_table.load_data()
            popup.destroy()

        ttk.Button(popup, text="Save", command=save_changes).grid(row=2, column=0, columnspan=2)

    # method to delete course
    def delete_course(self):
        course = self.select_course()
        if not course:
            messagebox.showerror("Error", "Please select a course to delete")
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {course.course_name}?")
        if confirm:
            #remove the course from the courses list in data manager 
            self.dm.courses_data.remove(course)
            #remove the course from the list of assigned courses of the corresponding instructor
            if course.course_instructor:
                course.course_instructor.assigned_courses.remove(course)
                course.course_instructor = None
            #remove the course from the list of registered courses of all registered students in this course
            if course.enrolled_students:
                for student in course.enrolled_students:
                    student.registered_courses.remove(course)
            #refresh the table
            self.load_data()
            if self.student_table:
                self.student_table.load_data()
            if self.instructor_table:
                self.instructor_table.load_data()

            messagebox.showinfo("Deleted", f"Course {course.course_name} has been deleted.")

    # search
    def search_records(self):
        query = self.search_var.get().strip().lower()
        for row in self.tree.get_children():
            self.tree.delete(row)

        if not query:
            self.load_data()
            return

        for course in self.dm.courses_data:
            if query in course.course_id.lower():
                self.insert_course(course)
                continue
            if query in course.course_name.lower():
                self.insert_course(course)
                continue
            if course.course_instructor and query in course.course_instructor.name.lower():
                self.insert_course(course)
                continue
            for s in course.enrolled_students:
                if query in s.name.lower():
                    self.insert_course(course)
                    break

    # insert one course row
    def insert_course(self, course):
        students = [s.name for s in course.enrolled_students]
        students_str = ", ".join(students)
        instructor_name = course.course_instructor.name if course.course_instructor else "Unassigned"
        self.tree.insert("", "end", values=(
            course.course_id,
            course.course_name,
            instructor_name,
            students_str
        ))

    # reload table
    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for course in self.dm.courses_data:
            self.insert_course(course)
