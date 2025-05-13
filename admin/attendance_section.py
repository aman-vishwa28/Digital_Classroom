import customtkinter as ctk
from db_connection import get_db_connection
import mysql.connector
from tkinter import messagebox
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict

def attendance_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen):
    dashboard_screen.pack_forget()
    student_screen.pack_forget()
    payment_screen.pack_forget()
    fees_screen.pack_forget()
    teacher_screen.pack_forget()
    exam_screen.pack_forget()
    profile_screen.pack_forget()
    expense_screen.pack_forget()
    attendance_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

attendance_chart_canvas = None
attendance_student_name = ""

def create_attendance_screen(root, screen_width, menu_bar_color):
    attendance_screen = ctk.CTkFrame(root)
    attendance_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    attendance_screen.configure(width=screen_width - 50)

    #attendance title strip
    attendance_title_bar = ctk.CTkFrame(attendance_screen, fg_color = menu_bar_color, corner_radius=0, border_width=0)
    attendance_title_bar.pack(side = ctk.TOP, fill=ctk.X, pady=0)
    attendance_title_bar.configure(height=100)

    #attendance Panel Title
    attendance_title = ctk.CTkLabel(attendance_title_bar,text="Attendance Section",fg_color=menu_bar_color,text_color="white", font=("Gudea", 20,"bold"))
    attendance_title.pack(expand=True,anchor="center", pady=15)


    #side nav for attendance

    attendance_side_nav = ctk.CTkFrame(attendance_screen, corner_radius=0)
    attendance_side_nav.pack(side=ctk.TOP,fill=ctk.X, padx=0,pady=0)
    

    def add_attendance():
        view_attendance_frame.pack_forget()
        view_chart_frame.pack_forget()
        attendance_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True,anchor="n")

    def show_attendance():
        attendance_frame.pack_forget()
        view_chart_frame.pack_forget()
        view_attendance_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True,anchor="n")

    def view_chart():
        attendance_frame.pack_forget()
        view_attendance_frame.pack_forget()
        view_chart_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True,anchor="n")


    for i in range(3):
        attendance_side_nav.grid_columnconfigure(i,weight=1)
    
    marks_attendance = ctk.CTkButton(attendance_side_nav, text="Mark Attendance",font=("Gudea", 15,"bold"), corner_radius = 0, command=add_attendance)
    marks_attendance.grid(row=0,column=0, sticky="ew", padx=0,pady=0)

    view_attendance = ctk.CTkButton(attendance_side_nav, text="View Attendance",font=("Gudea", 15,"bold"), corner_radius = 0, command=show_attendance)
    view_attendance.grid(row=0,column=1,sticky="ew", padx=0,pady=0)

    view_attendance = ctk.CTkButton(attendance_side_nav, text="View Chart",font=("Gudea", 15,"bold"), corner_radius = 0, command=view_chart)
    view_attendance.grid(row=0,column=2,sticky="ew", padx=0,pady=0)

    #Attendance Frame
    attendance_frame = ctk.CTkFrame(attendance_screen)
    attendance_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True,anchor="n")

    view_attendance_frame = ctk.CTkFrame(attendance_screen)
    view_attendance_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True,anchor="n")

    view_chart_frame = ctk.CTkFrame(attendance_screen)
    view_chart_frame.pack(side=ctk.TOP,fill=ctk.BOTH,expand=True,anchor="n")



    for i in range(3):
        attendance_frame.grid_rowconfigure(i,weight=0)
    for j in range(4):
        attendance_frame.grid_columnconfigure(j,weight=1)   


    student_container = ctk.CTkFrame(attendance_frame)
    student_container.grid(row=4, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)

    student_name_frame = ctk.CTkFrame(student_container)

    def attendance_validation():

        errors = []
        date_str = attendance_date_entry.get().strip()
        
        try:
            # Try to parse the date in the format yyyy-mm-dd
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # If successful, calculate the day of the week
            day_of_week = date_obj.strftime("%A")  # Get the full name of the day (e.g., Monday)
            
            # Update the select_day_entry with the day of the week
            attendance_day_entry.configure(state="normal")
            attendance_day_entry.delete(0, ctk.END)
            attendance_day_entry.insert(0, day_of_week)
            attendance_day_entry.configure(state = "disable")
        except ValueError:
            messagebox.showerror("Date Error",f"{attendance_date_entry.get()} \nEnter the Valid date")
            attendance_date_entry.delete(0, ctk.END)

        if attendance_std_entry.get() == "--Select--":
            errors.append("Standard not Selected")

        if attendance_year_entry.get() == "--Select--":
            errors.append("Batch Year not Selected")

        if not attendance_date_entry.get():
            errors.append("Date cannot be Empty")

        if attendance_subject_entry.get() == "--Select--":
            errors.append("Subject not Selected")

        if attendance_teacher_entry.get() == "--Select--":
            errors.append("Teacher not Selected")

        if errors:
            messagebox.showerror("Validation Error","\n".join(errors))
            return False
        
        return True


    # def display_student():
    #     if not attendance_validation():
    #         return
        
    #     messagebox.showinfo("Test","OK")

    def clear_attendance():
        attendance_std_entry.set("--Select--")
        attendance_date_entry.delete(0, ctk.END)

        attendance_day_entry.configure(state = "normal")
        attendance_day_entry.delete(0, ctk.END)
        attendance_day_entry._activate_placeholder()
        attendance_day_entry.configure(state = "disable")

        attendance_year_entry.set("--Select--")
        attendance_subject_entry.set("--Select--")
        attendance_teacher_entry.set("--Select--")
        
        # placeholder
        attendance_date_entry._activate_placeholder()

        attendance_screen.focus_set()

    # def on_focus_out(event):
    #     # Get the date string from the pay_date_entry
    #     date_str = attendance_date_entry.get().strip()
        
    #     try:
    #         # Try to parse the date in the format yyyy-mm-dd
    #         date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
    #         # If successful, calculate the day of the week
    #         day_of_week = date_obj.strftime("%A")  # Get the full name of the day (e.g., Monday)
            
    #         # Update the select_day_entry with the day of the week
    #         attendance_day_entry.configure(state="normal")
    #         attendance_day_entry.delete(0, ctk.END)
    #         attendance_day_entry.insert(0, day_of_week)
    #         attendance_day_entry.configure(state = "disable")
    #     except ValueError:
    #         messagebox.showerror("Date Error",f"{attendance_date_entry.get()} \nEnter the Valid date")
    #         attendance_date_entry.delete(0, ctk.END)



    def display_student():
        if not attendance_validation():
            return
        
        # Clear previous student display if any
        for widget in student_name_frame.winfo_children():
            widget.destroy()
        
        # Get selected values
        selected_class = attendance_std_entry.get()
        selected_batch = attendance_year_entry.get()
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Fetch students for the selected class and batch
            query = """
            SELECT student_id, CONCAT(first_name, ' ', COALESCE(middle_name, ''), ' ', last_name) AS student_name 
            FROM students_detail 
            WHERE class = %s AND academic_year = %s
            ORDER BY student_id
            """
            cursor.execute(query, (selected_class, selected_batch))
            students = cursor.fetchall()
            conn.close()
            
            if not students:
                messagebox.showinfo("No Students", "No students found for the selected class and batch.")
                return
                
            # Create scrollable frame for student list
            scroll_frame = ctk.CTkScrollableFrame(student_name_frame)
            scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Create select all checkbox
            select_all_var = ctk.BooleanVar(value=False)
            
            def toggle_select_all():
                for var in student_vars:
                    var.set(select_all_var.get())
            
            select_all_cb = ctk.CTkCheckBox(
                scroll_frame, 
                text="Select All", 
                variable=select_all_var,
                command=toggle_select_all,
                font=("Gudea", 12, "bold")
            )
            select_all_cb.pack(anchor="w", pady=(0, 10))
            
            # Store student variables
            student_vars = []
            student_data = []
            
            # Display each student with checkbox
            for student_id, student_name in students:
                var = ctk.BooleanVar(value=True)  # Default to present (checked)
                student_vars.append(var)
                student_data.append((student_id, student_name))
                
                student_row = ctk.CTkFrame(scroll_frame)
                student_row.pack(fill="x", pady=2)
                
                cb = ctk.CTkCheckBox(
                    student_row, 
                    text=f"{student_id} - {student_name}", 
                    variable=var,
                    font=("Gudea", 12)
                )
                cb.pack(side="left", padx=5)
            
            # Add buttons frame at bottom
            buttons_frame = ctk.CTkFrame(student_name_frame)
            buttons_frame.pack(fill="x", padx=10, pady=10)
            
            def mark_attendance():
                selected_date = attendance_date_entry.get()
                selected_day = attendance_day_entry.get()
                selected_subject = attendance_subject_entry.get()
                selected_teacher_str = attendance_teacher_entry.get()
                selected_teacher_id = selected_teacher_str.split(" - ")[0]
                selected_teacher_name = selected_teacher_str.split(" - ")[1]
 
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    
                    # Insert attendance for each student
                    for (student_id, student_name), var in zip(student_data, student_vars):
                        status = "Present" if var.get() else "Absent"
                        
                        query = """
                        INSERT INTO attendance_detail
                        (student_id, class, student_name, attendance_date, attendance_day, batch_year, teacher_id, teacher_name, _status, _subject)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        cursor.execute(query, (
                            student_id,
                            selected_class,
                            student_name,
                            selected_date,
                            selected_day,
                            selected_batch,
                            selected_teacher_id,
                            selected_teacher_name,
                            status,
                            selected_subject
                        ))
                    
                    conn.commit()
                    conn.close()
                    messagebox.showinfo("Success", "Attendance marked successfully!")
                    student_name_frame.pack_forget()
                    clear_attendance()
                    
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error saving attendance: {err}")
                    if conn:
                        conn.close()
            
            mark_btn = ctk.CTkButton(
                buttons_frame, 
                text="Mark Attendance", 
                command=mark_attendance,
                font=("Gudea", 12, "bold")
            )
            mark_btn.pack(side="left", padx=5, expand=True)
            
            cancel_btn = ctk.CTkButton(
                buttons_frame, 
                text="Cancel", 
                command=lambda: student_name_frame.pack_forget(),
                font=("Gudea", 12, "bold")
            )
            cancel_btn.pack(side="left", padx=5, expand=True)
            
            # Display the student frame
            student_name_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching students: {err}")
            if conn:
                conn.close()







    attendance_std_lbl = ctk.CTkLabel(attendance_frame,text="\tSelect Standard",font=("Gudea", 15,"bold"), anchor="w")
    attendance_std_lbl.grid(row=0,column=0, padx=10,pady=10,sticky="ew")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT course_name FROM courses"
        cursor.execute(query)
        course_names = [f"{row[0]}".strip() for row in cursor.fetchall()]
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
        
    attendance_std_entry = ctk.CTkComboBox(attendance_frame, values=course_names, state="readonly",font=("Gudea", 12,"bold"))
    attendance_std_entry.set("--Select--")
    attendance_std_entry.grid(row=0,column=1, padx=10,pady=10,sticky="ew")

    attendance_year_lbl = ctk.CTkLabel(attendance_frame, text="\tSelect Batch Year", font=("Gudea", 15,"bold"), anchor="w")
    attendance_year_lbl.grid(row=0,column=2, padx=10,pady=10,sticky="ew")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT batch_year FROM batch"
        cursor.execute(query)
        batch_values = [f"{row[0]}".strip() for row in cursor.fetchall()]
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
        batch_values = []

    attendance_year_entry = ctk.CTkComboBox(attendance_frame, values = batch_values, state="readonly", font=("Gudea",12,"bold"))
    attendance_year_entry.grid(row=0,column=3,sticky="ew",padx=10,pady=10)
    attendance_year_entry.set("--Select--")

    attendance_date_lbl = ctk.CTkLabel(attendance_frame,text="\tDate",font=("Gudea", 15,"bold"), anchor="w")
    attendance_date_lbl.grid(row=1,column=0, padx=10,pady=10,sticky="ew")

    attendance_date_entry = ctk.CTkEntry(attendance_frame, placeholder_text="YYYY-MM-DD", font=("Gudea", 12,"bold"))
    attendance_date_entry.grid(row=1,column=1, padx=10,pady=10,sticky="ew")
    # attendance_date_entry.bind("<FocusOut>", on_focus_out)
    
    attendance_day_lbl = ctk.CTkLabel(attendance_frame,text="\tDay",font=("Gudea", 15,"bold"), anchor="w")
    attendance_day_lbl.grid(row=1,column=2, padx=10,pady=10,sticky="ew")

    attendance_day_entry = ctk.CTkEntry(attendance_frame, placeholder_text="Day of Date appear hear", font=("Gudea",12,"bold"))
    attendance_day_entry.grid(row=1,column=3,sticky="ew",padx=10,pady=10)
    attendance_day_entry.configure(state="disable")

    attendance_subject_lbl = ctk.CTkLabel(attendance_frame,text="\tSelect Subject",font=("Gudea", 15,"bold"), anchor="w")
    attendance_subject_lbl.grid(row=2,column=0, padx=10,pady=10,sticky="ew")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT subject_name FROM subjects"
        cursor.execute(query)
        subject_values = [f"{row[0]}".strip() for row in cursor.fetchall()]
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
        subject_values = []

    attendance_subject_entry = ctk.CTkComboBox(attendance_frame, values = subject_values, state="readonly", font=("Gudea",12,"bold"))
    attendance_subject_entry.grid(row=2,column=1,sticky="ew",padx=10,pady=10)
    attendance_subject_entry.set("--Select--")

    attendance_teacher_lbl = ctk.CTkLabel(attendance_frame,text="\tSelect Teacher",font=("Gudea", 15,"bold"), anchor="w")
    attendance_teacher_lbl.grid(row=2,column=2, padx=10,pady=10,sticky="ew")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT teacher_id, first_name, middle_name, last_name FROM teachers_detail"
        cursor.execute(query,)
        teacher_names = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
        # attendance_name_entry.configure(values = teacher_names, state = "readonly")
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
        teacher_names = []

    attendance_teacher_entry = ctk.CTkComboBox(attendance_frame, values = teacher_names, state="readonly", font=("Gudea",12,"bold"))
    attendance_teacher_entry.grid(row=2,column=3,sticky="ew",padx=10,pady=10)
    attendance_teacher_entry.set("--Select--")


    attendance_ok_btn = ctk.CTkButton(attendance_frame,text="OK",font=("Gudea", 12,"bold"), command=display_student)
    attendance_ok_btn.grid(row=3, column=0, columnspan = 2, sticky="ew",padx=20,pady=5)

    attendance_clear_btn = ctk.CTkButton(attendance_frame,text="CLEAR",font=("Gudea", 12,"bold"), command= clear_attendance)
    attendance_clear_btn.grid(row=3, column=2, columnspan = 2, sticky="ew",padx=20,pady=5)


    #======================================= start
    

    def view_attendance(a_id):

        # Create new window
        view_attendance_detail = ctk.CTkToplevel()  # Use CTkToplevel instead of CTk for child windows
        view_attendance_detail.geometry("800x600")
        view_attendance_detail.title(f"Attendance Details - {a_id}")
        
        # This prevents the DPI scaling errors
        view_attendance_detail.after(100, lambda: view_attendance_detail.focus_force())
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier access
            
            # Fetch student data
            query = """SELECT attendance_id, student_id, student_name, class, batch_year, attendance_date, attendance_day, _status, _subject, teacher_id, teacher_name
                    FROM attendance_detail WHERE attendance_id = %s"""
            cursor.execute(query, (a_id,))
            attendance = cursor.fetchone()
            
            if not attendance:
                ctk.CTkLabel(view_attendance_detail, text="Attendance not found").pack()
                return
                
            # Create display frame

            scroll_frame = ctk.CTkScrollableFrame(view_attendance_detail)
            scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

            info_frame = ctk.CTkFrame(scroll_frame)
            info_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # Display student info in a grid
            labels = [
                ("Attendance ID", attendance['attendance_id']),
                ("Student ID", attendance['student_id']),
                ("Student Name", attendance['student_name']),
                ("Class", attendance['class']),
                ("Batch Year", attendance['batch_year']),
                ("Date", attendance['attendance_date']),
                ("Day", attendance['attendance_day']),
                ("Status", attendance['_status']),
                ("Subject", attendance['_subject']),
                ("Teacher ID", attendance['teacher_id']),
                ("Teacher Name", attendance['teacher_name'])
            ]
            
            for i, (label, value) in enumerate(labels):
                ctk.CTkLabel(info_frame, text=label + ":", font=("Arial", 12, "bold")).grid(row=i, column=0, padx=10, pady=5, sticky="w")
                ctk.CTkLabel(info_frame, text=value).grid(row=i, column=1, padx=10, pady=5, sticky="w")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error retrieving data: {err}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()
                
        # Handle window close properly
        def on_close():
            view_attendance_detail.destroy()
            
        view_attendance_detail.protocol("WM_DELETE_WINDOW", on_close)
    
    
    
   
    def setup_attendance_display():
        # Initialize the items list
        items = []
        
        # Function to fetch data from database
        def fetch_attendance_data():
            nonlocal items            
            search_input = search_by.get()
            search_val = input_field.get()
            combo_box = select_from_combobox.get()

            if (search_input == "All"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT attendance_id, student_id, student_name, class, batch_year, attendance_date, _status FROM attendance_detail"
                    cursor.execute(query)
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

                    
            elif (search_input == "Student ID"):
                if not input_field.get() or not input_field.get().isdigit():
                    messagebox.showerror("Validation Error", "Input cannot be empty and digits are allowed")
                    return False
                
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT attendance_id, student_id, student_name, class, batch_year, attendance_date, _status FROM attendance_detail Where student_id = %s"
                    cursor.execute(query,(search_val,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

    
            elif (search_input == "Class"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT attendance_id, student_id, student_name, class, batch_year, attendance_date, _status FROM attendance_detail WHERE class = %s"
                    cursor.execute(query,(combo_box,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []
            

            elif (search_input == "Batch Year"):
                
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT attendance_id, student_id, student_name, class, batch_year, attendance_date, _status FROM attendance_detail Where batch_year = %s"
                    cursor.execute(query,(combo_box,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

            elif (search_input == "Subject"):
                
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT attendance_id, student_id, student_name, class, batch_year, attendance_date, _status FROM attendance_detail Where _subject = %s"
                    cursor.execute(query,(combo_box,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

        
        # Function to refresh the display
        def refresh_display():
            nonlocal items
            # Destroy existing widgets
            for widget in display_attendance.winfo_children():
                widget.destroy()
            
            # Fetch fresh data
            fetch_attendance_data()
            
            # Rebuild the display
            for i in range(len(items)+1):
                display_attendance.grid_rowconfigure(i, weight=0)
            for j in range(7):
                display_attendance.grid_columnconfigure(j, weight=1)
            
            # Header row
            ctk.CTkLabel(display_attendance, text="Student ID").grid(row=0, column=0)
            ctk.CTkLabel(display_attendance, text="Student Name").grid(row=0, column=1)
            ctk.CTkLabel(display_attendance, text="Class").grid(row=0, column=2)
            ctk.CTkLabel(display_attendance, text="Batch Year").grid(row=0, column=3)
            ctk.CTkLabel(display_attendance, text="Date").grid(row=0, column=4)
            ctk.CTkLabel(display_attendance, text="Status").grid(row=0, column=5)
            ctk.CTkLabel(display_attendance, text="Action").grid(row=0, column=6)
            
            # Data rows
            for i, item in enumerate(items, start=1):
                attendance_id, student_id, student_name, _class, batch_years, attendance_date, status = item.split(",")
                ctk.CTkLabel(display_attendance, text=student_id).grid(row=i, column=0)
                ctk.CTkLabel(display_attendance, text=student_name).grid(row=i, column=1)
                ctk.CTkLabel(display_attendance, text=_class).grid(row=i, column=2)
                ctk.CTkLabel(display_attendance, text=batch_years).grid(row=i, column=3)
                ctk.CTkLabel(display_attendance, text=attendance_date).grid(row=i, column=4)
                ctk.CTkLabel(display_attendance, text=status).grid(row=i, column=5)
                
                # Status label with conditional color
                status_color = "red" if status == "Absent" else "white"
                ctk.CTkLabel(
                    display_attendance, 
                    text=status,
                    text_color=status_color,
                    font=("Arial", 12, "bold")  # Optional: make it bold for better visibility
                ).grid(row=i, column=5)
                
                ctk.CTkButton(
                    display_attendance,
                    text="View",
                    command=lambda aid=attendance_id: view_attendance(aid)
                ).grid(row=i, column=6, pady=5)

        

        set_search_frame = ctk.CTkFrame(view_attendance_frame)
        set_search_frame.pack(side = ctk.TOP, fill = ctk.X, padx = 10, pady = 10, anchor = "n")

        for i in range(5):
            set_search_frame.grid_columnconfigure(i, weight = 1)
        

        def check_search(*args):
            if search_by.get() == "All":
                input_field.delete(0, ctk.END)
                input_lbl.grid_forget()
                input_field.grid_forget()
                select_from_combobox.set("--Select--")
                select_from_combobox.grid_forget()

            elif (search_by.get() == "Student ID"):
                input_lbl.configure(text = f"Enter {search_by.get()}")
                select_from_combobox.grid_forget()
                input_field.delete(0, ctk.END)
                input_lbl.grid(row = 0, column = 2, sticky = "ew", padx = 5, pady = 5)
                input_field.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)

   
            elif (search_by.get() == "Class"):  
                input_lbl.configure(text = f"Select {search_by.get()}")
                input_field.grid_forget()
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT course_name FROM courses"
                    cursor.execute(query)
                    search_class = [f"{row[0]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    search_class = []

                select_from_combobox.configure(values = search_class)
                select_from_combobox.set("-Select--")
                select_from_combobox.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)
                input_lbl.grid(row = 0, column = 2, sticky = "ew", padx = 5, pady = 5)


            elif (search_by.get() == "Batch Year"):
                input_lbl.configure(text = f"Select {search_by.get()}")
                input_field.grid_forget()
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT batch_year FROM batch"
                    cursor.execute(query)
                    search_batch = [f"{row[0]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    search_batch = []

                select_from_combobox.configure(values = search_batch)
                select_from_combobox.set("-Select--")
                select_from_combobox.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)
                input_lbl.grid(row = 0, column = 2, sticky = "ew", padx = 5, pady = 5)

            elif (search_by.get() == "Subject"):
                input_lbl.configure(text = f"Select {search_by.get()}")
                input_field.grid_forget()
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT subject_name FROM subjects"
                    cursor.execute(query)
                    search_subject = [f"{row[0]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    search_subject = []

                select_from_combobox.configure(values = search_subject)
                select_from_combobox.set("-Select--")
                select_from_combobox.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)
                input_lbl.grid(row = 0, column = 2, sticky = "ew", padx = 5, pady = 5)


        ctk.CTkLabel(set_search_frame, text = "Search By").grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)

        search_by = ctk.CTkComboBox(set_search_frame, values = ["All", "Student ID", "Class", "Batch Year", "Subject"])
        search_by.grid(row = 0, column = 1, sticky = "ew", padx = 5, pady = 5)
        search_by.set("All")
        search_by.configure(command = check_search)


        input_lbl = ctk.CTkLabel(set_search_frame, text = f"Enter {search_by.get()}")

        select_from_combobox = ctk.CTkComboBox(set_search_frame, values = [], state="readonly")
        select_from_combobox.set("--Select--")

        input_field = ctk.CTkEntry(set_search_frame)

        input_lbl.grid_forget()
        input_field.grid_forget()
        # ctk.CTkComboBox(transaction_frame)

        
        # Create scrollable frame (only once)
        scrollable_frame_attendance = ctk.CTkScrollableFrame(view_attendance_frame)
        scrollable_frame_attendance.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # Create display frame (only once)
        display_attendance = ctk.CTkFrame(scrollable_frame_attendance)
        display_attendance.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10, expand=True)
        
        # Add refresh button
        refresh_btn = ctk.CTkButton(
            view_attendance_frame,
            text="Refresh",
            command=refresh_display
        )
        refresh_btn.pack(side=ctk.TOP, pady=10)
        
        # Initial data load
        refresh_display()

    # Call the setup function
    setup_attendance_display()
    # transaction_frame.pack_forget()

    #======================================= End


    def get_attendance_data(student_id, subject):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    _status,
                    COUNT(*) as count
                FROM attendance_detail 
                WHERE student_id = %s AND _subject = %s
                GROUP BY _status
            """
            cursor.execute(query, (student_id, subject))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Query failed: {err}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()

    def create_attendance_chart(viz_frame, status_counts, student_id, subject):
        global attendance_chart_canvas, attendance_student_name
        
        # Clear previous chart
        if 'attendance_chart_canvas' in globals() and attendance_chart_canvas is not None:
            try:
                attendance_chart_canvas.get_tk_widget().destroy()
            except:
                pass
        
        # Prepare data
        labels = []
        sizes = []
        colors = []
        
        present_count = 0
        absent_count = 0
        
        for record in status_counts:
            if record['_status'] == 'Present':
                present_count = record['count']
                labels.append('Present')
                sizes.append(present_count)
                colors.append('#4CAF50')  # Green
            elif record['_status'] == 'Absent':
                absent_count = record['count']
                labels.append('Absent')
                sizes.append(absent_count)
                colors.append('#F44336')  # Red
        
        total = present_count + absent_count
        present_percentage = (present_count / total) * 100 if total > 0 else 0
        absent_percentage = (absent_count / total) * 100 if total > 0 else 0
        
        # Create figure
        fig, ax = plt.subplots(figsize=(7, 5), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            sizes,
            labels=labels,
            autopct=lambda p: f'{p:.1f}%',
            startangle=90,
            colors=colors,
            textprops={'color': 'white', 'fontsize': 12},
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )
        
        ax.axis('equal')
        ax.set_title(
            f"Attendance Analysis\nStudent: {attendance_student_name} (ID: {student_id})\nSubject: {subject}",
            color='white',
            pad=25,
            fontsize=14,
            fontweight='bold'
        )
        
        # Add detailed legend
        legend_labels = [
            f"Present: {present_count} ({present_percentage:.1f}%)",
            f"Absent: {absent_count} ({absent_percentage:.1f}%)",
            f"Total Classes: {total}"
        ]
        
        ax.legend(
            wedges,
            legend_labels,
            title="Attendance Summary",
            loc="center left",
            bbox_to_anchor=(-0.1, 0.5),
            facecolor='#2b2b2b',
            edgecolor='white',
            title_fontproperties={'weight': 'bold', 'size': 12},
            fontsize=11,
            labelcolor='white'
        )
        
        # Display chart
        attendance_chart_canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        attendance_chart_canvas.draw()
        attendance_chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

    def generate_attendance_report(student_id_entry, subject_combobox, viz_frame):
        student_id = student_id_entry.get()
        subject = subject_combobox.get()
        
        if not student_id or not subject or subject == "--Select--":
            messagebox.showwarning("Input Error", "Please enter valid Student ID and select Subject")
            return
            
        attendance_data = get_attendance_data(student_id, subject)
        if not attendance_data:
            messagebox.showinfo("No Data", "No attendance records found for this student and subject")
            return
        
        create_attendance_chart(viz_frame, attendance_data, student_id, subject)


    def fetch_student_and_subjects(student_id_entry, student_name_label, subject_combobox, generate_btn):
        global attendance_student_name
        student_id = student_id_entry.get()
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter Student ID")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            
            # Fetch student name
            query = "SELECT DISTINCT student_name FROM attendance_detail WHERE student_id = %s LIMIT 1"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            if result:
                attendance_student_name = result['student_name']
                student_name_label.configure(text=f"Student: {attendance_student_name}")
                
                # Fetch subjects for this student
                query = "SELECT DISTINCT _subject FROM attendance_detail WHERE student_id = %s ORDER BY _subject"
                cursor.execute(query, (student_id,))
                subjects = [row['_subject'] for row in cursor.fetchall()]
                
                if subjects:
                    subject_combobox.configure(values=subjects)
                    subject_combobox.set(subjects[0])  # Auto-select first subject
                    generate_btn.configure(state="normal")
                else:
                    messagebox.showinfo("No Subjects", "No attendance records found for this student")
                    subject_combobox.configure(values=[])
                    subject_combobox.set("--Select--")
                    generate_btn.configure(state="disabled")
            else:
                messagebox.showinfo("Not Found", "No student found with this ID")
                student_name_label.configure(text="Student: Not found")
                subject_combobox.configure(values=[])
                subject_combobox.set("--Select--")
                generate_btn.configure(state="disabled")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching data: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals() and conn.is_connected():
                conn.close()


    main_frame = ctk.CTkFrame(view_chart_frame)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Control panel
    control_frame = ctk.CTkFrame(main_frame, width=250)
    control_frame.pack(side="left", fill="y", padx=5, pady=5)
    
    # Student selection
    ctk.CTkLabel(control_frame, text="Student ID:").pack(pady=(10, 0))
    student_id_entry = ctk.CTkEntry(control_frame)
    student_id_entry.pack(pady=5)
    
    # Student info button
    fetch_name_btn = ctk.CTkButton(
        control_frame,
        text="Get Student Info",
        command=lambda: fetch_student_and_subjects(student_id_entry, student_name_label, subject_combobox, generate_btn),
        width=200
    )
    fetch_name_btn.pack(pady=5)
    
    # Student name display
    student_name_label = ctk.CTkLabel(control_frame, text="Student: Not selected", font=("Arial", 12))
    student_name_label.pack(pady=5)
    
    # Subject selection
    ctk.CTkLabel(control_frame, text="Subject:").pack(pady=(10, 0))
    subject_combobox = ctk.CTkComboBox(control_frame, state="readonly")
    subject_combobox.pack(pady=5)
    subject_combobox.set("--Select--")
    
    # Generate report button
    generate_btn = ctk.CTkButton(
        control_frame, 
        text="Generate Attendance Report",
        command=lambda: generate_attendance_report(student_id_entry, subject_combobox, viz_frame),
        state="disabled"
    )
    generate_btn.pack(pady=20)
    
    # Visualization frame
    viz_frame = ctk.CTkFrame(main_frame)
    viz_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)



    # setup_attendance_analysis()

    import os
    def on_closing():
        try:
            # Clean up matplotlib figures
            plt.close('all')
            
            # Destroy all widgets properly
            root.destroy()
            
            # Exit python process
            os._exit(0)
        except:
            os._exit(0)

    # Set this as your window close protocol
    root.protocol("WM_DELETE_WINDOW", on_closing)







    view_chart_frame.pack_forget()
    view_attendance_frame.pack_forget()

    return attendance_screen