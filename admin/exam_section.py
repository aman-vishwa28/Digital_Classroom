import customtkinter as ctk
from db_connection import get_db_connection
from tkinter import simpledialog,messagebox
import mysql.connector
from datetime import datetime


# import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import mysql.connector
# from tkinter import messagebox
from collections import defaultdict

chart_canvas = None
student_name = ""

def exam_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen):
    teacher_screen.pack_forget()
    dashboard_screen.pack_forget()
    payment_screen.pack_forget()
    fees_screen.pack_forget()
    attendance_screen.pack_forget()
    student_screen.pack_forget()
    profile_screen.pack_forget()
    expense_screen.pack_forget()
    exam_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)





def create_exam_screen(root, screen_width, menu_bar_color):
    exam_screen = ctk.CTkFrame(root)
    exam_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    exam_screen.configure(width=screen_width - 50)

    #exam title strip
    exam_title_bar = ctk.CTkFrame(exam_screen, fg_color = menu_bar_color, corner_radius=0, border_width=0)
    exam_title_bar.pack(side = ctk.TOP, fill=ctk.X, pady=0)
    exam_title_bar.configure(height=100)

    #exam Panel Title
    exam_title = ctk.CTkLabel(exam_title_bar,text="Exam Section",fg_color=menu_bar_color,text_color="white", font=("Gudea", 20,"bold"))
    exam_title.pack(expand=True,anchor="center", pady=15)

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

    #side nav for Exam

    exam_side_nav = ctk.CTkFrame(exam_screen)
    exam_side_nav.pack(side=ctk.TOP,fill=ctk.X, padx=0,pady=0)

    def add_marks():
        view_marks_frame.pack_forget()
        view_performance_frame.pack_forget()
        scroll_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, anchor="n")

    def show_marks():
        scroll_frame.pack_forget()
        view_performance_frame.pack_forget()
        view_marks_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, anchor="n")

    def show_performance():
        view_marks_frame.pack_forget()
        scroll_frame.pack_forget()
        view_performance_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, anchor="n")



    for i in range(3):
        exam_side_nav.grid_columnconfigure(i,weight=1)
    
    marks_exam = ctk.CTkButton(exam_side_nav, text="Enter Marks",font=("Gudea", 15,"bold"), corner_radius = 0, command = add_marks)
    marks_exam.grid(row=0,column=0,sticky="ew", padx=0,pady=0)

    view_marks = ctk.CTkButton(exam_side_nav, text="View Marks",font=("Gudea", 15,"bold"), corner_radius = 0, command = show_marks)
    view_marks.grid(row=0,column=1,sticky="ew", padx=0,pady=0)

    view_performance = ctk.CTkButton(exam_side_nav, text="View Performance",font=("Gudea", 15,"bold"), corner_radius = 0, command = show_performance)
    view_performance.grid(row=0,column=2,sticky="ew", padx=0,pady=0)



    scroll_frame = ctk.CTkScrollableFrame(exam_screen)
    scroll_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, anchor="n")

    view_marks_frame = ctk.CTkScrollableFrame(exam_screen)
    view_marks_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, anchor="n")

    view_performance_frame = ctk.CTkFrame(exam_screen)
    view_performance_frame.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, anchor="n")

    #Attendence Frame
    marks_frame = ctk.CTkFrame(scroll_frame, corner_radius=5)
    marks_frame.pack(side=ctk.TOP, fill=ctk.X, expand=True, anchor="n", padx= 15, pady = 15)

    update_marks = ctk.CTkFrame(scroll_frame, corner_radius=5)
    update_marks.pack(side=ctk.TOP, fill=ctk.X, expand=True, anchor="n", padx= 15, pady = 15)

    delete_marks = ctk.CTkFrame(scroll_frame, corner_radius=5)
    delete_marks.pack(side=ctk.TOP, fill=ctk.X, expand=True, anchor="n", padx= 15, pady = 15)

    for i in range(5):
        marks_frame.grid_rowconfigure(i,weight=0)
    for j in range(4):
        marks_frame.grid_columnconfigure(j,weight=1)   


    def check_batch(*args):
        if (exam_batch_entry.get() != "--Select--"):
            exam_class_entry.set("--Select--")

    def check_std(*args):
        if (exam_class_entry.get() != "--Select--"):
            exam_student_entry.configure(state = "readonly")
            exam_student_entry.set("--Select--")
            std = exam_class_entry.get()
            year = exam_batch_entry.get()
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                query = "SELECT student_id, first_name, middle_name, last_name FROM students_detail where class = %s and academic_year = %s"
                cursor.execute(query, (std, year))
                student_names = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
                exam_student_entry.configure(values = student_names)
                conn.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
                student_names = []
                exam_student_entry.configure(values = student_names)

        else:
            exam_student_entry.configure(state = "normal")
            exam_student_entry.set("--Select--")
            exam_student_entry.configure(state = "disabled")

    def validate():
        errors = []
        if exam_batch_entry.get() == "--Select--":
            errors.append("Batch not Selected")

        if not exam_student_entry.get():
            errors.append("Student not Selected")

        if exam_teacher_entry.get() == "--Select--":
            errors.append("Teacher not Selected")

        if not exam_date_entry.get():
            errors.append("Date not Entered")

        if exam_subject_entry.get() == "--Select--":
            errors.append("Subject not Selected")

        if exam_type_entry.get() == "--Select--":
            errors.append("Exam type not Selected")

        if not exam_obtained_marks_entry.get():
            errors.append("Obtained marks not Entered")

        if not exam_total_marks_entry.get():
            errors.append("Total marks not Entered")

        if (exam_obtained_marks_entry.get() > exam_total_marks_entry.get()):
            errors.append("Obtained Marks Cannot be Greater than Total Marks")

        date_str = exam_date_entry.get().strip()
        
        try:
            # Try to parse the date in the format yyyy-mm-dd
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # If successful, calculate the day of the week
            day_of_week = date_obj.strftime("%A")  # Get the full name of the day (e.g., Monday)
            
            # Update the select_day_entry with the day of the week
            exam_day_entry.configure(state="normal")
            exam_day_entry.delete(0, ctk.END)
            exam_day_entry.insert(0, day_of_week)
            exam_day_entry.configure(state = "disabled")
        except ValueError:
            messagebox.showerror("Date Error",f"{exam_date_entry.get()} \nEnter the Valid date")
            exam_date_entry.delete(0, ctk.END)
            exam_date_entry._activate_placeholder()
            exam_day_entry._activate_placeholder()

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return False
        
        return True
            


    def insert_marks():
        if not validate():
            return False
        

        student_id = exam_student_entry.get().split(" - ")[0]
        studen_name = exam_student_entry.get().split(" - ")[1]
        try: 
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO student_marks (student_id, student_name, date, day, batch_year, subject, obtained_mark, total_mark, class, exam_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (student_id, studen_name, exam_date_entry.get(), exam_day_entry.get(), exam_batch_entry.get(), exam_subject_entry.get(), exam_obtained_marks_entry.get(), exam_total_marks_entry.get(), exam_class_entry.get(), exam_type_entry.get())
            cursor.execute(query,values)
            conn.commit()    
            conn.close()

            messagebox.showinfo("Success", "Marks Added successfully!")
            add_another()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data: {err}")


    def on_focus_out(event):
        # Get the date string from the pay_date_entry
        date_str = exam_date_entry.get().strip()
        
        try:
            # Try to parse the date in the format yyyy-mm-dd
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # If successful, calculate the day of the week
            day_of_week = date_obj.strftime("%A")  # Get the full name of the day (e.g., Monday)
            
            # Update the select_day_entry with the day of the week
            exam_day_entry.configure(state="normal")
            exam_day_entry.delete(0, ctk.END)
            exam_day_entry.insert(0, day_of_week)
            exam_day_entry.configure(state = "disabled")
        except ValueError:
            # messagebox.showerror("Date Error",f"{fees_date_entry.get()} \nEnter the Valid date")

            exam_date_entry.delete(0, ctk.END)
            exam_date_entry._activate_placeholder()

            exam_day_entry.configure(state="normal")
            exam_day_entry.delete(0, ctk.END)
            exam_day_entry._activate_placeholder()
            exam_day_entry.configure(state = "disabled")
            return False
        
    def clear_all():
        exam_batch_entry.set("--Select--")
        exam_class_entry.set("--Select--")
        exam_teacher_entry.set("--Select--")

        exam_student_entry.configure(state = "normal")
        exam_student_entry.set("--Select--")
        exam_student_entry.configure(state = "disabled")

        exam_date_entry.delete(0, ctk.END)
        exam_date_entry._activate_placeholder()

        exam_day_entry.configure(state = "normal")
        exam_day_entry.delete(0, ctk.END)
        exam_day_entry._activate_placeholder()
        exam_day_entry.configure(state = "disabled")

        exam_subject_entry.set("--Select--")
        exam_type_entry.set("--Select--")

        exam_obtained_marks_entry.delete(0, ctk.END)
        exam_obtained_marks_entry._activate_placeholder()

        exam_total_marks_entry.delete(0, ctk.END)
        exam_total_marks_entry._activate_placeholder()

    def add_another():

        exam_subject_entry.set("--Select--")
        # exam_type_entry.set("--Select--")

        exam_obtained_marks_entry.delete(0, ctk.END)
        exam_obtained_marks_entry._activate_placeholder()

        exam_total_marks_entry.delete(0, ctk.END)
        exam_total_marks_entry._activate_placeholder()



    exam_batch_lbl = ctk.CTkLabel(marks_frame, text="\tBatch Year",font=("Gudea", 15,"bold"), anchor="w")
    exam_batch_lbl.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

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

    exam_batch_entry = ctk.CTkComboBox(marks_frame, values = batch_values, state="readonly", font=("Gudea", 12, "bold"))
    exam_batch_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
    exam_batch_entry.set("--Select--")
    exam_batch_entry.configure(command = check_batch)

    exam_class_lbl = ctk.CTkLabel(marks_frame,text="\tStandard",font=("Gudea", 15,"bold"), anchor="w")
    exam_class_lbl.grid(row=0, column=2, sticky="ew", padx=5, pady=5)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT course_name FROM courses"
        cursor.execute(query)
        course_names = [f"{row[0]}".strip() for row in cursor.fetchall()]
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
        course_names = []

    exam_class_entry = ctk.CTkComboBox(marks_frame, values = course_names, state="readonly", font=("Gudea", 12, "bold"))
    exam_class_entry.grid(row=0, column=3, sticky="ew", padx=5, pady=5)
    exam_class_entry.set("--Select--")
    exam_class_entry.configure(command = check_std)

    exam_student_lbl = ctk.CTkLabel(marks_frame,text="\tStudent Name",font=("Gudea", 15, "bold"), anchor="w")
    exam_student_lbl.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

    exam_student_entry = ctk.CTkComboBox(marks_frame, values=[], font=("Gudea", 12, "bold"))
    exam_student_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
    exam_student_entry.set("--Select--")
    exam_student_entry.configure(state="disabled")

    exam_teacher_lbl = ctk.CTkLabel(marks_frame, text="\tTeacher Name",font=("Gudea", 15, "bold"), anchor="w")
    exam_teacher_lbl.grid(row=1, column=2, sticky="ew", padx=5,pady=5)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT teacher_id, first_name, middle_name, last_name FROM teachers_detail"
        cursor.execute(query)
        teacher_names = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
        conn.close()
        # return teacher_names
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
        teacher_names = []

    exam_teacher_entry = ctk.CTkComboBox(marks_frame, values=teacher_names, state="readonly", font=("Gudea", 12, "bold"))
    exam_teacher_entry.grid(row=1, column=3, sticky="ew", padx=5,pady=5)
    exam_teacher_entry.set("--Select--")
    
    exam_date_lbl = ctk.CTkLabel(marks_frame, text="\tDate", font=("Gudea", 15, "bold"), anchor="w")
    exam_date_lbl.grid(row=2, column=0, sticky="ew", padx=5,pady=5)

    exam_date_entry = ctk.CTkEntry(marks_frame, placeholder_text="YYYY-MM-DD", font=("Gudea", 12, "bold"))
    exam_date_entry.grid(row=2, column=1, sticky="ew", padx=5,pady=5)
    exam_date_entry.bind("<FocusOut>", on_focus_out)

    exam_day_lbl = ctk.CTkLabel(marks_frame, text="\tDay", font=("Gudea", 15, "bold"), anchor="w")
    exam_day_lbl.grid(row=2, column=2, sticky="ew", padx=5,pady=5)

    exam_day_entry = ctk.CTkEntry(marks_frame, placeholder_text = "Day of date appear here", font=("Gudea", 12))
    exam_day_entry.grid(row=2, column=3, sticky="ew", padx=5, pady=5)
    exam_day_entry.configure(state="disabled")

    exam_subject_lbl = ctk.CTkLabel(marks_frame,text="\tSubject",font=("Gudea", 15,"bold"), anchor="w")
    exam_subject_lbl.grid(row=3, column=0, sticky="ew", padx=5,pady=5)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT subject_name FROM subjects"
        cursor.execute(query)
        subject_names = [f"{row[0]}".strip() for row in cursor.fetchall()]
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
        subject_names = []

    exam_subject_entry = ctk.CTkComboBox(marks_frame, values = subject_names, state="readonly", font=("Gudea", 12,"bold"))
    exam_subject_entry.grid(row=3, column=1, sticky="ew", padx=5,pady=5)
    exam_subject_entry.set("--Select--")

    exam_type_lbl = ctk.CTkLabel(marks_frame,text="\tExam Type",font=("Gudea", 15,"bold"), anchor="w")
    exam_type_lbl.grid(row=3, column=2, sticky="ew", padx=5,pady=5)

    exam_type_entry = ctk.CTkComboBox(marks_frame, values=["Offline", "Online", "First Term", "Second Term", "Third Term", "Fourth Term", "Fifth Term"], state="readonly", font=("Gudea", 12,"bold"))
    exam_type_entry.grid(row=3, column=3, sticky="ew", padx=5,pady=5)
    exam_type_entry.set("--Select--")   

    exam_obtained_marks_lbl = ctk.CTkLabel(marks_frame, text="\tMarks Obtained", font=("Gudea", 15,"bold"), anchor="w")
    exam_obtained_marks_lbl.grid(row=4, column=0, sticky="ew", padx=5,pady=5)

    exam_obtained_marks_entry = ctk.CTkEntry(marks_frame, placeholder_text="Enter Obtained Marks", font=("Gudea", 12, "bold"))
    exam_obtained_marks_entry.grid(row=4, column=1, sticky="ew", padx=5,pady=5)

    exam_total_marks_lbl = ctk.CTkLabel(marks_frame, text="\tTotal Marks", font=("Gudea", 15,"bold"), anchor="w")
    exam_total_marks_lbl.grid(row=4, column=2, sticky="ew", padx=5,pady=5)

    exam_total_marks_entry = ctk.CTkEntry(marks_frame, placeholder_text="Enter Out of Marks", font=("Gudea", 12, "bold"))
    exam_total_marks_entry.grid(row=4, column=3, sticky="ew", padx=5,pady=5)

    exam_ok_btn = ctk.CTkButton(marks_frame,text="OK",font=("Gudea", 12,"bold"), command = insert_marks)
    exam_ok_btn.grid(row=5, column=0, sticky="ew",padx=10,pady=10)

    exam_add_another_btn = ctk.CTkButton(marks_frame,text="Add Another Marks",font=("Gudea", 12,"bold"), command=add_another)
    exam_add_another_btn.grid(row=5, column=1, columnspan = 2, sticky="ew",padx=10,pady=10)

    exam_clear_btn = ctk.CTkButton(marks_frame,text="CLEAR ALL",font=("Gudea", 12,"bold"), command=clear_all)
    exam_clear_btn.grid(row=5, column=3, sticky="ew",padx=10,pady=10)

    # Update Marks

    for i in range(4):
        update_marks.grid_rowconfigure(i,weight=0)
    for j in range(4):
        update_marks.grid_columnconfigure(j,weight=1) 

    def update_mark():
        errors1 = []

        if not exam_id_entry.get().strip:
            errors1.append("Exam ID not Entered")

        if not exam_id_entry.get().isdigit:
            errors1.append("Exam ID must be a digit")

        if not obtained_mark_update_entry.get():
            errors1.append("Obtained marks not Entered")

        if not total_mark_update_entry.get():
            errors1.append("Total marks not Entered")

        if (obtained_mark_update_entry.get() > total_mark_update_entry.get()):
            errors1.append("Obtained Marks Cannot be Greater than Total Marks")

        if errors1:
            messagebox.showerror("Validation Error", "\n".join(errors1))
            return False


        exam_id_check = exam_id_entry.get()
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "UPDATE student_marks SET obtained_mark = %s, total_mark = %s WHERE exam_id = %s"
            cursor.execute(query, (obtained_mark_update_entry.get(), total_mark_update_entry.get(), exam_id_check))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Marks Updated successfully!")
            cancel_grid()
            exam_id_entry.delete(0, ctk.END)
            exam_id_entry._activate_placeholder()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating data: {err}")
            return False
        

    def grid_it():

        if not exam_id_entry.get().strip:
            messagebox.showerror("Validation Error", "Exam id cannot be empty")
            cancel_grid()
            return False
        
        if not exam_id_entry.get().isdigit:
            messagebox.showerror("Validation Error", "Exam id must be a digit only")
            cancel_grid()
            return False
        
        exam_id_check = exam_id_entry.get()
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT student_id FROM student_marks where exam_id = %s"
            cursor.execute(query,(exam_id_check,))
            check_exam_id = [f"{row[0]}".strip() for row in cursor.fetchall()]
            conn.close()
            if not check_exam_id:
                messagebox.showerror("Retriving Error", "Exam id not found")
                return False

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            return False

        obtained_mark_update.grid(row = 2, column = 0, sticky="ew", padx=10, pady=10)
        obtained_mark_update_entry.grid(row = 2, column = 1, sticky="ew", padx=10, pady=10)
        total_mark_update.grid(row = 2, column = 2, sticky="ew", padx=10, pady=10)
        total_mark_update_entry.grid(row = 2, column = 3, sticky="ew", padx=10, pady=10)

        update_btn.grid(row = 3, column = 0, columnspan = 2, sticky="ew", padx=10, pady=10)
        cancel_btn.grid(row = 3, column = 2, columnspan = 2, sticky="ew", padx=10, pady=10)

    def cancel_grid():
        obtained_mark_update_entry.delete(0,ctk.END)
        total_mark_update_entry.delete(0,ctk.END)

        obtained_mark_update_entry._activate_placeholder()
        total_mark_update_entry._activate_placeholder()

        obtained_mark_update.grid_forget()
        obtained_mark_update_entry.grid_forget()
        total_mark_update.grid_forget()
        total_mark_update_entry.grid_forget()

        update_btn.grid_forget()
        cancel_btn.grid_forget()


    label_for_update = ctk.CTkLabel(update_marks,text="Update Marks", font=("Gudea", 15,"bold"))
    label_for_update.grid(row = 0, column = 0, columnspan = 4, sticky="ew", padx=10, pady=10)

    exam_id_lbl = ctk.CTkLabel(update_marks, text="Enter Exam Id",font=("Gudea", 15,"bold"))
    exam_id_lbl.grid(row = 1, column = 0, sticky="ew", padx=10, pady=10)

    exam_id_entry = ctk.CTkEntry(update_marks, placeholder_text="Enter Exam ID", font=("Gudea", 12,"bold"))
    exam_id_entry.grid(row = 1, column = 1, sticky="ew", padx=10, pady=10)

    exam_search_btn = ctk.CTkButton(update_marks,text="Check", command = grid_it, font=("Gudea", 15,"bold"))
    exam_search_btn.grid(row = 1, column = 2, sticky="ew", padx=10, pady=10)

    obtained_mark_update = ctk.CTkLabel(update_marks,text="Obtained Marks",font=("Gudea", 15,"bold"))
    total_mark_update = ctk.CTkLabel(update_marks,text="Total Marks", font=("Gudea", 15,"bold"))

    obtained_mark_update_entry = ctk.CTkEntry(update_marks, placeholder_text = "Enter Obtained Marks", font=("Gudea", 12,"bold"))
    total_mark_update_entry = ctk.CTkEntry(update_marks, placeholder_text = "Enter Total Marks", font=("Gudea", 12,"bold"))

    update_btn = ctk.CTkButton(update_marks, text = "UPDATE", font=("Gudea", 15,"bold"), command = update_mark)
    cancel_btn = ctk.CTkButton(update_marks, text="CANCEL", font=("Gudea", 15,"bold"), command=cancel_grid)
    

    # Delete marks


    for i in range(4):
        delete_marks.grid_rowconfigure(i,weight=0)
    for j in range(4):
        delete_marks.grid_columnconfigure(j,weight=1)

    def delete_mark():
        if not exam_id_entry_delete.get():
            messagebox.showerror("Validation Error", "Exam Id cannot be Empty")
            return

        if not exam_id_entry_delete.get().isdigit():
            messagebox.showerror("Validation Error", "Exam Id must be digit only")
            return

        # Show password dialog
        password = simpledialog.askstring("Password", "Enter admin password:", show='*')
        
        if password is None:  # If user cancels
            return
        
        if password != PASSWORD[0]:  # Replace with actual admin password
            messagebox.showerror("Error", "Incorrect password! Deletion not allowed.")
            return
        

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT student_id FROM student_marks where exam_id = %s"
            cursor.execute(query,(exam_id_entry_delete.get(),))
            check_exam_id = [f"{row[0]}".strip() for row in cursor.fetchall()]
            conn.close()
            if not check_exam_id:
                messagebox.showerror("Retriving Error", "Exam id not found")
                exam_id_entry_delete.delete(0,ctk.END)
                exam_id_entry_delete._activate_placeholder()
                exam_screen.focus_set()
                return False
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            exam_id_entry_delete.delete(0,ctk.END)
            exam_id_entry_delete._activate_placeholder()
            exam_screen.focus_set()
            return False
        

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "DELETE FROM student_marks WHERE exam_id = %s"
            cursor.execute(query, (exam_id_entry_delete.get(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Marks deleted Successfully!")
            exam_id_entry_delete.delete(0,ctk.END)
            exam_id_entry_delete._activate_placeholder()
            exam_screen.focus_set()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting data: {err}")

    label_for_delete = ctk.CTkLabel(delete_marks,text="Delete Marks", font=("Gudea", 15,"bold"))
    label_for_delete.grid(row = 0, column = 0, columnspan = 4, sticky="ew", padx=10, pady=10)

    exam_id_lbl_delete = ctk.CTkLabel(delete_marks, text="Enter Exam Id",font=("Gudea", 15,"bold"))
    exam_id_lbl_delete.grid(row = 1, column = 0, sticky="ew", padx=10, pady=10)

    exam_id_entry_delete = ctk.CTkEntry(delete_marks, placeholder_text="Enter Exam ID", font=("Gudea", 12,"bold"))
    exam_id_entry_delete.grid(row = 1, column = 1, sticky="ew", padx=10, pady=10)

    exam_delete_btn = ctk.CTkButton(delete_marks,text="Delete Marks", command = delete_mark, font=("Gudea", 15,"bold"))
    exam_delete_btn.grid(row = 1, column = 2, sticky="ew", padx=10, pady=10)

    #======================================= start
    

    def view_exam(e_id):

        # Create new window
        view_exam_detail = ctk.CTkToplevel()  # Use CTkToplevel instead of CTk for child windows
        view_exam_detail.geometry("800x600")
        view_exam_detail.title(f"Exam Details - {e_id}")
        
        # This prevents the DPI scaling errors
        view_exam_detail.after(100, lambda: view_exam_detail.focus_force())
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier access
            
            # Fetch student data
            query = """SELECT exam_id, student_id, student_name, date, day,  batch_year, subject, obtained_mark, total_mark, class, exam_type
                    FROM student_marks WHERE exam_id = %s"""
            cursor.execute(query, (e_id,))
            exam = cursor.fetchone()
            
            if not exam:
                ctk.CTkLabel(view_exam_detail, text="Exam not found").pack()
                return
                
            # Create display frame

            scroll_frame = ctk.CTkScrollableFrame(view_exam_detail)
            scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

            info_frame = ctk.CTkFrame(scroll_frame)
            info_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # Display student info in a grid
            labels = [
                ("Exam ID", exam['exam_id']),
                ("Batch Year", exam['batch_year']),
                ("Student ID", exam['student_id']),
                ("Student Name", exam['student_name']),
                ("Class", exam['class']),
                ("Subject", exam['subject']),
                ("Date", exam['date']),
                ("Day", exam['day']),
                ("Obtained Marks", exam['obtained_mark']),
                ("Total Marks", exam['total_mark']),
                ("Exam Type", exam['exam_type']),
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
            view_exam_detail.destroy()
            
        view_exam_detail.protocol("WM_DELETE_WINDOW", on_close)
    
    
    
   
    def setup_exam_display():
        # Initialize the items list
        items = []
        
        # Function to fetch data from database
        def fetch_exam_data():
            nonlocal items            
            search_input = search_by.get()
            search_val = input_field.get()
            combo_box = select_from_combobox.get()

            if (search_input == "All"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT exam_id, student_id, student_name, subject, exam_type, obtained_mark, total_mark FROM student_marks"
                    cursor.execute(query)
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

            elif (search_input == "Exam ID"):
                if not input_field.get() or not input_field.get().isdigit():
                    messagebox.showerror("Validation Error", "Input cannot be empty and digits are allowed")
                    return False
                
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT exam_id, student_id, student_name, subject, exam_type, obtained_mark, total_mark FROM student_marks Where exam_id = %s"
                    cursor.execute(query,(search_val,))
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
                    query = "SELECT exam_id, student_id, student_name, subject, exam_type, obtained_mark, total_mark FROM student_marks Where student_id = %s"
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
                    query = "SELECT exam_id, student_id, student_name, subject, exam_type, obtained_mark, total_mark FROM student_marks WHERE class = %s"
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
                    query = "SELECT exam_id, student_id, student_name, subject, exam_type, obtained_mark, total_mark FROM student_marks Where subject = %s"
                    cursor.execute(query,(combo_box,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]},{row[5]},{row[6]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

            elif (search_input == "Exam Type"):
                
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT exam_id, student_id, student_name, subject, exam_type, obtained_mark, total_mark FROM student_marks Where exam_type = %s"
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
            for widget in display_exam.winfo_children():
                widget.destroy()
            
            # Fetch fresh data
            fetch_exam_data()
            
            # Rebuild the display
            for i in range(len(items)+1):
                display_exam.grid_rowconfigure(i, weight=0)
            for j in range(8):
                display_exam.grid_columnconfigure(j, weight=1)
            
            # Header row
            ctk.CTkLabel(display_exam, text="Exam ID").grid(row=0, column=0)
            ctk.CTkLabel(display_exam, text="Student ID").grid(row=0, column=1)
            ctk.CTkLabel(display_exam, text="Student Name").grid(row=0, column=2)
            ctk.CTkLabel(display_exam, text="Subject").grid(row=0, column=3)
            ctk.CTkLabel(display_exam, text="Exam Type").grid(row=0, column=4)
            ctk.CTkLabel(display_exam, text="Obtained").grid(row=0, column=5)
            ctk.CTkLabel(display_exam, text="Out Of").grid(row=0, column=6)
            ctk.CTkLabel(display_exam, text="Action").grid(row=0, column=7)
            
            # Data rows
            for i, item in enumerate(items, start=1):
                exam_id_, student_id, student_name, subject, exam_type, obtained, out_of = item.split(",")
                ctk.CTkLabel(display_exam, text=exam_id_).grid(row=i, column=0)
                ctk.CTkLabel(display_exam, text=student_id).grid(row=i, column=1)
                ctk.CTkLabel(display_exam, text=student_name).grid(row=i, column=2)
                ctk.CTkLabel(display_exam, text=subject).grid(row=i, column=3)
                ctk.CTkLabel(display_exam, text=exam_type).grid(row=i, column=4)
                ctk.CTkLabel(display_exam, text=obtained).grid(row=i, column=5)
                ctk.CTkLabel(display_exam, text=out_of).grid(row=i, column=6)
                
                ctk.CTkButton(
                    display_exam,
                    text="View",
                    command=lambda eid=exam_id_: view_exam(eid)
                ).grid(row=i, column=7, pady=5)

        

        set_search_frame = ctk.CTkFrame(view_marks_frame)
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

            elif (search_by.get() == "Exam ID"):
                input_lbl.configure(text = f"Enter {search_by.get()}")
                select_from_combobox.grid_forget()
                input_field.delete(0, ctk.END)
                input_lbl.grid(row = 0, column = 2, sticky = "ew", padx = 5, pady = 5)
                input_field.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)

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

            elif (search_by.get() == "Exam Type"):  
                input_lbl.configure(text = f"Select {search_by.get()}")
                input_field.grid_forget()
                select_from_combobox.configure(values = ["Offline", "Online", "First Term", "Second Term", "Third Term", "Fourth Term", "Fifth Term"])
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

        search_by = ctk.CTkComboBox(set_search_frame, values = ["All", "Exam ID", "Student ID", "Class", "Subject", "Exam Type"])
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
        scrollable_frame_exam = ctk.CTkScrollableFrame(view_marks_frame)
        scrollable_frame_exam.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # Create display frame (only once)
        display_exam = ctk.CTkFrame(scrollable_frame_exam)
        display_exam.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10, expand=True)
        
        # Add refresh button
        refresh_btn = ctk.CTkButton(
            view_marks_frame,
            text="Refresh",
            command=refresh_display
        )
        refresh_btn.pack(side=ctk.TOP, pady=10)
        
        # Initial data load
        refresh_display()

    # Call the setup function
    setup_exam_display()
    # transaction_frame.pack_forget()



    # conn = None
    # chart_canvas = None
    # student_name = ""

    def fetch_student_info(student_id_entry, student_name_label, generate_btn):
        global student_name
        student_id = student_id_entry.get()
        if not student_id:
            messagebox.showwarning("Input Error", "Please enter Student ID")
            return
            
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = "SELECT DISTINCT student_name FROM student_marks WHERE student_id = %s LIMIT 1"
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            
            if result:
                student_name = result['student_name']
                student_name_label.configure(text=f"Student: {student_name}")
                generate_btn.configure(state="normal")
            else:
                messagebox.showinfo("Not Found", "No student found with this ID")
                student_name_label.configure(text="Student: Not found")
                generate_btn.configure(state="disabled")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching student: {err}")
        finally:
            if 'cursor' in locals():
                cursor.close()

    def get_exam_types():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT exam_type FROM student_marks ORDER BY exam_type")
            return [row[0] for row in cursor.fetchall()]
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching exam types: {err}")
            return []
        finally:
            if 'cursor' in locals():
                cursor.close()



    def get_consolidated_student_data(student_id, exam_type):
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            query = """
                SELECT 
                    subject,
                    SUM(obtained_mark) as total_obtained,
                    SUM(total_mark) as total_possible
                FROM student_marks 
                WHERE student_id = %s AND exam_type = %s
                GROUP BY subject
                ORDER BY subject
            """
            cursor.execute(query, (student_id, exam_type))
            return cursor.fetchall()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Query failed: {err}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()


    
    def create_pie_chart(viz_frame, subjects, percentages, student_id, exam_type):
        global chart_canvas, student_name  # Must be at the very top
        
        # Clear previous chart if it exists
        if chart_canvas:
            chart_canvas.get_tk_widget().destroy()
            
        # Create figure
        fig, ax = plt.subplots(figsize=(7, 5), dpi=100)
        fig.patch.set_facecolor('#2b2b2b')
        
        # Create pie chart
        wedges, texts, autotexts = ax.pie(
            percentages,
            labels=subjects,
            autopct=lambda p: f'{p:.1f}%' if p >= 5 else '',
            startangle=90,
            colors=plt.cm.Paired.colors,
            textprops={'color': 'white', 'fontsize': 12},
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
            pctdistance=0.85
        )
        
        # Configure chart appearance
        ax.axis('equal')
        ax.set_title(
            f"Performance Analysis\nStudent: {student_name} (ID: {student_id})\nExam Type: {exam_type}",
            color='white',
            pad=25,
            fontsize=14,
            fontweight='bold'
        )
        
        # Add legend
        legend_labels = [f"{sub} ({perc:.1f}%)" for sub, perc in zip(subjects, percentages)]
        ax.legend(
            wedges,
            legend_labels,
            title="Subjects",
            loc="center left",
            bbox_to_anchor=(-0.1, 0.5),
            facecolor='#2b2b2b',
            edgecolor='white',
            title_fontproperties={'weight': 'bold', 'size': 12},
            fontsize=11,
            labelcolor='white'
        )
        
        # Display chart in Tkinter window
        chart_canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)


    def generate_report(student_id_entry, exam_type_combobox, viz_frame):
        student_id = student_id_entry.get()
        exam_type = exam_type_combobox.get()
        
        if not student_id or not exam_type or exam_type == "No exams available":
            messagebox.showwarning("Input Error", "Please enter valid Student ID and select Exam Type")
            return
            
        student_data = get_consolidated_student_data(student_id, exam_type)
        if not student_data:
            messagebox.showinfo("No Data", "No records found for this student and exam type")
            return
        
        subjects = []
        percentages = []
        
        for record in student_data:
            try:
                subject = record['subject']
                obtained = float(record['total_obtained'])
                total = float(record['total_possible'])
                percentage = (obtained / total) * 100 if total != 0 else 0
                subjects.append(subject)
                percentages.append(percentage)
            except (ValueError, KeyError):
                continue
                
        create_pie_chart(viz_frame, subjects, percentages, student_id, exam_type)

    # Main container
    main_frame = ctk.CTkFrame(view_performance_frame)
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
        command=lambda: fetch_student_info(student_id_entry, student_name_label, generate_btn),
        width=200
    )
    fetch_name_btn.pack(pady=5)
    
    # Student name display
    student_name_label = ctk.CTkLabel(control_frame, text="Student: Not selected", font=("Arial", 12))
    student_name_label.pack(pady=5)
    
    # Exam type selection
    ctk.CTkLabel(control_frame, text="Exam Type:").pack(pady=(10, 0))
    exam_types = get_exam_types()
    if not exam_types:
        messagebox.showwarning("No Exam Types", "No exam types found in database")
        exam_types = ["No exams available"]
    exam_type_combobox = ctk.CTkComboBox(control_frame, values=exam_types)
    exam_type_combobox.pack(pady=5)
    
    # Generate report button
    generate_btn = ctk.CTkButton(
        control_frame, 
        text="Generate Performance Report",
        command=lambda: generate_report(student_id_entry, exam_type_combobox, viz_frame),
        state="disabled"
    )
    generate_btn.pack(pady=20)
    
    # Visualization frame
    viz_frame = ctk.CTkFrame(main_frame)
    viz_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
    
    # root.mainloop()
    
    # Clean up on exit
    # if conn and conn.is_connected():
    #     conn.close()


    view_marks_frame.pack_forget()
    view_performance_frame.pack_forget()

    return exam_screen