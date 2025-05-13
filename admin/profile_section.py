import customtkinter as ctk
from db_connection import get_db_connection
from tkinter import messagebox
import re
from PIL import Image
from tkinter import simpledialog
from natsort import natsorted
import mysql.connector
import os
from datetime import datetime


def profile_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen):
    teacher_screen.pack_forget()
    dashboard_screen.pack_forget()
    payment_screen.pack_forget()
    fees_screen.pack_forget()
    attendance_screen.pack_forget()
    exam_screen.pack_forget()
    student_screen.pack_forget()
    expense_screen.pack_forget()
    profile_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)


def create_profile_screen(root, screen_width, menu_bar_color):
    profile_screen = ctk.CTkFrame(root)
    profile_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    profile_screen.configure(width=screen_width - 50)

    #profile title strip
    profile_title_bar = ctk.CTkFrame(profile_screen, fg_color = menu_bar_color, corner_radius=0, border_width=0)
    profile_title_bar.pack(side = ctk.TOP, fill=ctk.X)
    profile_title_bar.configure(height=100)

    #profile Panel Title
    profile_title = ctk.CTkLabel(profile_title_bar,text="Profile Section",fg_color=menu_bar_color,text_color="white", font=("Gudea", 20,"bold"))
    profile_title.pack(expand=True,anchor="center", pady=15)


    # Nav Profile
    profile_nav = ctk.CTkFrame(profile_screen)
    profile_nav.pack(side=ctk.TOP,fill=ctk.X)

    def view():
        course_frame.pack_forget()
        subject_frame.pack_forget()
        batch_frame.pack_forget()
        profile_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)

    def course_detail():
        profile_frame.pack_forget()
        subject_frame.pack_forget()
        batch_frame.pack_forget()
        course_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)

    def subject_detail():
        course_frame.pack_forget()
        profile_frame.pack_forget()
        batch_frame.pack_forget()
        subject_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)

    def batch_detail():
        course_frame.pack_forget()
        subject_frame.pack_forget()
        profile_frame.pack_forget()
        batch_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT username, password 
            FROM user_login 
            WHERE role = 'admin' AND status = 'active'
        """
        cursor.execute(query)
        results = cursor.fetchall()
        USERNAME = [row[0].strip() for row in results]
        PASSWORD = [row[1].strip() for row in results]

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

    for i in range(4):
        profile_nav.grid_columnconfigure(i,weight=1)
    
    view_admin = ctk.CTkButton(profile_nav,text="View Admin Profile", corner_radius=0, font=("Gudea", 15,"bold"), command=view)
    view_admin.grid(row=0,column=0,sticky="ew")

    course = ctk.CTkButton(profile_nav,text="Courses",corner_radius=0, font=("Gudea", 15,"bold"), command=course_detail)
    course.grid(row=0,column=1,sticky="ew")

    subject = ctk.CTkButton(profile_nav,text="Subjects", corner_radius=0, font=("Gudea", 15,"bold"), command=subject_detail)
    subject.grid(row=0,column=2,sticky="ew")
    
    batch = ctk.CTkButton(profile_nav,text="Batch Year", corner_radius=0, font=("Gudea", 15,"bold"), command=batch_detail)
    batch.grid(row=0,column=3,sticky="ew")

    profile_frame = ctk.CTkFrame(profile_screen, corner_radius=0)
    profile_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)

    course_frame = ctk.CTkFrame(profile_screen, corner_radius=0)
    course_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)

    subject_frame = ctk.CTkFrame(profile_screen, corner_radius=0)
    subject_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)

    batch_frame = ctk.CTkFrame(profile_screen, corner_radius=0)
    batch_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True)

    course_frame.pack_forget()
    subject_frame.pack_forget()
    batch_frame.pack_forget()

    #admin Profile Display

    scroll = ctk.CTkScrollableFrame(profile_frame)
    scroll.pack(side = ctk.TOP, fill = ctk.BOTH, expand = True, padx = 5, pady = 5)

    view_admin_detail_frame = ctk.CTkFrame(scroll)
    view_admin_detail_frame.pack(side = ctk.TOP, fill = ctk.BOTH, expand = True, padx = 5, pady = 5)


    for i in range(2):
        view_admin_detail_frame.grid_columnconfigure(i,weight=1)
    for j in range(15):
        view_admin_detail_frame.grid_rowconfigure(j,weight=0)

    ctk.CTkLabel(view_admin_detail_frame,text="SHREE SADGURU COACHING CLASSES",font=("Arial",30,"bold"), anchor="center").grid(row=0,column=0,columnspan=2,sticky="ew", pady = 10)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(base_dir, "..", "icons")

    profile_image = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "profile.jpg")), size = (150,150))
    profile = ctk.CTkButton(view_admin_detail_frame, text="", image=profile_image, border_width=0, fg_color="transparent", hover_color = ctk.ThemeManager.theme["CTkFrame"]["fg_color"])
    profile.image = profile_image
    profile.grid(row = 1, column = 0, columnspan=2,sticky="ew")

    ctk.CTkLabel(view_admin_detail_frame, text="Personal details",font=("Arial",25,"bold"), fg_color="lightblue", text_color="black").grid(row=2,column=0, columnspan = 2, sticky="ew", pady = 10)

    ctk.CTkLabel(view_admin_detail_frame, text="Name :",font=("Arial",15,"bold"),anchor="e").grid(row=3,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text="\tMrs. Umadevi Jitendra Vishwakarma",font=("Arial",15,"bold"),anchor="w").grid(row=3,column=1,sticky="w")

    ctk.CTkLabel(view_admin_detail_frame, text="Position :",font=("Arial",15,"bold"),anchor="e").grid(row=4,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text="\tDirector",font=("Arial",15,"bold"),anchor="w").grid(row=4,column=1,sticky="w")

    ctk.CTkLabel(view_admin_detail_frame, text="Contact :",font=("Arial",15,"bold"),anchor="e").grid(row=5,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text="\t+91-7972290854",font=("Arial",15,"bold"),anchor="w").grid(row=5,column=1,sticky="w")

    ctk.CTkLabel(view_admin_detail_frame, text="E-mail :",font=("Arial",15,"bold"),anchor="e").grid(row=6,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text="\tjeetuma12@gmail.com",font=("Arial",15,"bold"),anchor="w").grid(row=6,column=1,sticky="w")

    ctk.CTkLabel(view_admin_detail_frame, text="Date Of Birth :",font=("Arial",15,"bold"),anchor="e").grid(row=7,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text="\t12 October 1992",font=("Arial",15,"bold"),anchor="w").grid(row=7,column=1,sticky="w")

    ctk.CTkLabel(view_admin_detail_frame, text="Gender :",font=("Arial",15,"bold"),anchor="e").grid(row=8,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text="\tFemale",font=("Arial",15,"bold"),anchor="w").grid(row=8,column=1,sticky="w")

    ctk.CTkLabel(view_admin_detail_frame, text="Qualification :",font=("Arial",15,"bold"),anchor="e").grid(row=9,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text="\tB.sc, B.Ed",font=("Arial",15,"bold"),anchor="w").grid(row=9,column=1,sticky="w")

    current_year = datetime.now().year
    ctk.CTkLabel(view_admin_detail_frame, text="Experience :",font=("Arial",15,"bold"),anchor="e").grid(row=10,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text=f"\t{current_year - 2015 }+ Years in Education",font=("Arial",15,"bold"),anchor="w").grid(row=10,column=1,sticky="w")

    ctk.CTkLabel(view_admin_detail_frame, text="Institute details",font=("Arial",25,"bold"),fg_color="lightblue", text_color="black").grid(row=11, column=0, columnspan = 2, sticky="ew", pady = 10)

    ctk.CTkLabel(view_admin_detail_frame, text="Established :",font=("Arial",15,"bold"),anchor="e").grid(row=12,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text="\t2015",font=("Arial",15,"bold"),anchor="w").grid(row=12,column=1,sticky="w")

    ctk.CTkLabel(view_admin_detail_frame, text="Certified :",font=("Arial",15,"bold"),anchor="e").grid(row=13,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text="\tISO 9001:2015",font=("Arial",15,"bold"),anchor="w").grid(row=13,column=1,sticky="w")

    ctk.CTkLabel(view_admin_detail_frame, text="Address :",font=("Arial",15,"bold"),anchor="e").grid(row=14,column=0,sticky="e")
    ctk.CTkLabel(view_admin_detail_frame, text="\tGat no 11, Plot no 54, Virat Nagar, Ambad link Road, Nashik - 422010",font=("Arial",15,"bold"),anchor="w").grid(row=14,column=1,sticky="w")

    footer = ctk.CTkLabel(
        profile_screen,
        text="© 2025 Shree Sadguru Coaching Classes. All Rights Reserved.\n Design and Developed by Aman Vishwakarma (Aman sir)",
        font=("Arial", 12),
        text_color="gray"
    )
    footer.pack(side = ctk.BOTTOM, fill = ctk.X)

    def validate_course():
        if not course_entry.get().strip():
            messagebox.showerror("Error", "Course cannot be empty")
            return False

        course_names = check_duplicate_course()
        if course_entry.get().strip() in course_names:
            messagebox.showerror("Error", "Course already exists")
            return False
        return True

    def check_duplicate_course():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT course_name FROM courses"
            cursor.execute(query)
            course_names = [f"{row[0]}".strip() for row in cursor.fetchall()]
            conn.close()
            return course_names
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            return []

    def add_course_to_db():
        if not validate_course():
            return
        try: 
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO courses (course_name) VALUES (%s)"
            values = (course_entry.get(),)
            cursor.execute(query, values)
            conn.commit()    
            conn.close()
            messagebox.showinfo("Success", f"Course \"{course_entry.get()}\" added successfully!")
            course_entry.delete(0, ctk.END)
            course_entry._activate_placeholder()
            course_frame.focus_set()
            refresh_course_list()  # Refresh the list after adding
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data: {err}")

    def delete_course(course_to_delete):
        password_for_delete_course = simpledialog.askstring("Password", "Enter admin password:", show='*')
        
        if password_for_delete_course is None:  # If user cancels
            return
        
        if password_for_delete_course != PASSWORD[0]:  # Replace with actual admin password
            messagebox.showerror("Error", "Incorrect password! Deletion not allowed.")
            return
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "DELETE FROM courses WHERE course_name = %s"
            cursor.execute(query, (course_to_delete,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Course {course_to_delete} deleted successfully!")
            refresh_course_list()  # Refresh the list after deletion
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting data: {err}")

    def refresh_course_list():
        # Clear existing widgets
        for widget in view_course_frame.winfo_children():
            widget.destroy()
        
        # Get fresh data
        course_list = natsorted(check_duplicate_course())
        
        # Configure grid
        for i in range(len(course_list)+1):
            view_course_frame.grid_rowconfigure(i, weight=0)
        for j in range(2):
            view_course_frame.grid_columnconfigure(j, weight=1)

        # Header row
        ctk.CTkLabel(view_course_frame, text="Available Courses", font=("Arial",15,"bold")).grid(row=0, column=0)
        ctk.CTkLabel(view_course_frame, text="Action", font=("Arial",15,"bold")).grid(row=0, column=1)

        # Data rows
        for i, course in enumerate(course_list, start=1):
            ctk.CTkLabel(view_course_frame, text=f"{course}").grid(row=i, column=0, pady=5)
            ctk.CTkButton(
                view_course_frame, 
                text="Delete", 
                command=lambda c=course: delete_course(c)
            ).grid(row=i, column=1, pady=5)

    # Frame for Entry and Button of Courses
    course_frame_add = ctk.CTkFrame(course_frame)
    course_frame_add.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)

    for i in range(3):
        course_frame_add.grid_columnconfigure(i, weight=1)

    course_entry = ctk.CTkEntry(course_frame_add, placeholder_text="Enter Course Name", font=("Gudea",12,"bold"))
    course_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    course_add_btn = ctk.CTkButton(course_frame_add, text="Add Course", font=("Gudea",12,"bold"), command=add_course_to_db)
    course_add_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

    course_view_btn = ctk.CTkButton(course_frame_add, text="Refresh List", font=("Gudea",12,"bold"), command=refresh_course_list)
    course_view_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

    # Scrollable frame for course list
    view_course_scroll = ctk.CTkScrollableFrame(course_frame)
    view_course_scroll.pack(side=ctk.TOP, fill=ctk.BOTH, padx=10, pady=10, expand=True)

    view_course_frame = ctk.CTkFrame(view_course_scroll)
    view_course_frame.pack(side=ctk.TOP, fill=ctk.BOTH, padx=10, pady=10)

    # Initial load of course list
    refresh_course_list()

    
    # ================= SUBJECT MANAGEMENT =================
    def validate_subject():
        if not subject_entry.get().strip():
            messagebox.showerror("Error", "Subject cannot be empty")
            return False

        subject_names = check_duplicate_subject()
        if subject_entry.get().strip() in subject_names:
            messagebox.showerror("Error", "Subject already exists")
            return False
        return True

    def check_duplicate_subject():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT subject_name FROM subjects"
            cursor.execute(query)
            subject_names = [f"{row[0]}".strip() for row in cursor.fetchall()]
            conn.close()
            return subject_names
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            return []

    def add_subject_to_db():
        if not validate_subject():
            return
        try: 
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO subjects (subject_name) VALUES (%s)"
            values = (subject_entry.get(),)
            cursor.execute(query, values)
            conn.commit()    
            conn.close()
            messagebox.showinfo("Success", f"Subject \"{subject_entry.get()}\" added successfully!")
            subject_entry.delete(0, ctk.END)
            subject_entry._activate_placeholder()
            subject_frame.focus_set()
            refresh_subject_list()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data: {err}")

    def delete_subject(subject_to_delete):
        password = simpledialog.askstring("Password", "Enter admin password:", show='*')
        if password != PASSWORD[0]:  # Replace with your admin password
            messagebox.showerror("Error", "Incorrect password! Deletion not allowed.")
            return
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "DELETE FROM subjects WHERE subject_name = %s"
            cursor.execute(query, (subject_to_delete,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Subject {subject_to_delete} deleted successfully!")
            refresh_subject_list()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting data: {err}")

    def refresh_subject_list():
        # Clear existing widgets
        for widget in view_subject_frame.winfo_children():
            widget.destroy()
        
        # Get fresh data
        subject_list = natsorted(check_duplicate_subject())
        
        # Configure grid
        for i in range(len(subject_list)+1):
            view_subject_frame.grid_rowconfigure(i, weight=0)
        for j in range(2):
            view_subject_frame.grid_columnconfigure(j, weight=1)

        # Header row
        ctk.CTkLabel(view_subject_frame, text="Available Subjects", font=("Arial",15,"bold")).grid(row=0, column=0)
        ctk.CTkLabel(view_subject_frame, text="Action", font=("Arial",15,"bold")).grid(row=0, column=1)

        # Data rows
        for i, subject in enumerate(subject_list, start=1):
            ctk.CTkLabel(view_subject_frame, text=f"{subject}").grid(row=i, column=0, pady=5)
            ctk.CTkButton(
                view_subject_frame, 
                text="Delete", 
                command=lambda s=subject: delete_subject(s)
            ).grid(row=i, column=1, pady=5)

    # Subject UI Components
    subject_frame_add = ctk.CTkFrame(subject_frame)
    subject_frame_add.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)

    for i in range(3):
        subject_frame_add.grid_columnconfigure(i, weight=1)

    subject_entry = ctk.CTkEntry(subject_frame_add, placeholder_text="Enter Subject Name", font=("Gudea",12,"bold"))
    subject_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    subject_add_btn = ctk.CTkButton(subject_frame_add, text="Add Subject", font=("Gudea",12,"bold"), command=add_subject_to_db)
    subject_add_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

    subject_view_btn = ctk.CTkButton(subject_frame_add, text="Refresh List", font=("Gudea",12,"bold"), command=refresh_subject_list)
    subject_view_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

    # Scrollable frame for subject list
    view_subject_scroll = ctk.CTkScrollableFrame(subject_frame)
    view_subject_scroll.pack(side=ctk.TOP, fill=ctk.BOTH, padx=10, pady=10, expand=True)

    view_subject_frame = ctk.CTkFrame(view_subject_scroll)
    view_subject_frame.pack(side=ctk.TOP, fill=ctk.BOTH, padx=10, pady=10)

    # ================= BATCH MANAGEMENT =================
    def validate_batch(year_str):
        pattern = r"^\d{4}-\d{2}$"
        if not re.match(pattern, year_str):
            return False, "Invalid format. Expected format: yyyy-yy (e.g., 2023-24)."
        
        start_year, end_year = year_str.split("-")
        expected_end_year = str(int(start_year[2:]) + 1)[-2:]
        
        if end_year != expected_end_year:
            return False, f"Invalid year range. Expected {start_year}-{expected_end_year}."
        
        return True, "Valid year format."

    def check_duplicate_batch():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT batch_year FROM batch"
            cursor.execute(query)
            batch_names = [f"{row[0]}".strip() for row in cursor.fetchall()]
            conn.close()
            return batch_names
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            return []

    def add_batch_to_db():
        year_str = batch_entry.get().strip()
        is_valid, message = validate_batch(year_str)
        if not is_valid:
            messagebox.showerror("Error", message)
            return
        
        batch_names = check_duplicate_batch()
        if year_str in batch_names:
            messagebox.showerror("Error", "Batch already exists")
            return
        
        try: 
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO batch (batch_year) VALUES (%s)"
            values = (year_str,)
            cursor.execute(query, values)
            conn.commit()    
            conn.close()
            messagebox.showinfo("Success", f"Batch \"{year_str}\" added successfully!")
            batch_entry.delete(0, ctk.END)
            batch_entry._activate_placeholder()
            batch_frame.focus_set()
            refresh_batch_list()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data: {err}")

    def delete_batch(batch_to_delete):
        password = simpledialog.askstring("Password", "Enter admin password:", show='*')
        if password != PASSWORD[0]:  # Replace with your admin password
            messagebox.showerror("Error", "Incorrect password! Deletion not allowed.")
            return
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "DELETE FROM batch WHERE batch_year = %s"
            cursor.execute(query, (batch_to_delete,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Batch {batch_to_delete} deleted successfully!")
            refresh_batch_list()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting data: {err}")

    def refresh_batch_list():
        # Clear existing widgets
        for widget in view_batch_frame.winfo_children():
            widget.destroy()
        
        # Get fresh data
        batch_list = natsorted(check_duplicate_batch())
        
        # Configure grid
        for i in range(len(batch_list)+1):
            view_batch_frame.grid_rowconfigure(i, weight=0)
        for j in range(2):
            view_batch_frame.grid_columnconfigure(j, weight=1)

        # Header row
        ctk.CTkLabel(view_batch_frame, text="Available Batches", font=("Arial",15,"bold")).grid(row=0, column=0)
        ctk.CTkLabel(view_batch_frame, text="Action", font=("Arial",15,"bold")).grid(row=0, column=1)

        # Data rows
        for i, batch in enumerate(batch_list, start=1):
            ctk.CTkLabel(view_batch_frame, text=f"{batch}").grid(row=i, column=0, pady=5)
            ctk.CTkButton(
                view_batch_frame, 
                text="Delete", 
                command=lambda b=batch: delete_batch(b)
            ).grid(row=i, column=1, pady=5)

    # Batch UI Components
    batch_frame_add = ctk.CTkFrame(batch_frame)
    batch_frame_add.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10)

    for i in range(3):
        batch_frame_add.grid_columnconfigure(i, weight=1)

    batch_entry = ctk.CTkEntry(batch_frame_add, placeholder_text="Enter Batch Year (yyyy-yy)", font=("Gudea",12,"bold"))
    batch_entry.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    batch_add_btn = ctk.CTkButton(batch_frame_add, text="Add Batch", font=("Gudea",12,"bold"), command=add_batch_to_db)
    batch_add_btn.grid(row=0, column=1, sticky="ew", padx=10, pady=10)

    batch_view_btn = ctk.CTkButton(batch_frame_add, text="Refresh List", font=("Gudea",12,"bold"), command=refresh_batch_list)
    batch_view_btn.grid(row=0, column=2, sticky="ew", padx=10, pady=10)

    # Scrollable frame for batch list
    view_batch_scroll = ctk.CTkScrollableFrame(batch_frame)
    view_batch_scroll.pack(side=ctk.TOP, fill=ctk.BOTH, padx=10, pady=10, expand=True)

    view_batch_frame = ctk.CTkFrame(view_batch_scroll)
    view_batch_frame.pack(side=ctk.TOP, fill=ctk.BOTH, padx=10, pady=10)

    # Initial load of both lists
    refresh_subject_list()
    refresh_batch_list()



    return profile_screen