import customtkinter as ctk
from tkinter import simpledialog, messagebox
import mysql.connector
from datetime import datetime
from natsort import natsorted
import re
from db_connection import get_db_connection
from CTkMessagebox import CTkMessagebox

def student_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen):
    teacher_screen.pack_forget()
    dashboard_screen.pack_forget()
    payment_screen.pack_forget()
    fees_screen.pack_forget()
    attendance_screen.pack_forget()
    exam_screen.pack_forget()
    profile_screen.pack_forget()
    expense_screen.pack_forget()
    student_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

def create_student_screen(root, screen_width, menu_bar_color):
    student_screen = ctk.CTkFrame(root, fg_color="white")
    student_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    student_screen.configure(width=screen_width - 50)

    # Student title strip
    student_title_bar = ctk.CTkFrame(student_screen, fg_color=menu_bar_color, corner_radius=0, border_width=0)
    student_title_bar.pack(side=ctk.TOP, fill=ctk.X, pady=0)
    student_title_bar.configure(height=100)

    # Student Panel Title
    student_title = ctk.CTkLabel(student_title_bar, text="Student Section", fg_color=menu_bar_color, text_color="white", font=("Gudea", 20, "bold"))
    student_title.pack(expand=True, anchor="center", pady=15)

    def change_to_add_screen_student():
        #adding_student.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
        add_student_scroll.pack(side = ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)
        editing_student.pack_forget()
        deleting_student.pack_forget()
        showing_student.pack_forget()

    def change_to_update_screen_student():
        editing_student.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
        #adding_student.pack_forget()
        add_student_scroll.pack_forget()
        deleting_student.pack_forget()
        showing_student.pack_forget()
    
    def change_to_delete_screen_student():
        deleting_student.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
        #adding_student.pack_forget()
        add_student_scroll.pack_forget()
        editing_student.pack_forget()
        showing_student.pack_forget()

    def change_to_show_screen_student():
        showing_student.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
        add_student_scroll.pack_forget()
        #adding_student.pack_forget()
        editing_student.pack_forget()
        deleting_student.pack_forget()

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

    #Button side screen
    modify_buttons_student = ctk.CTkFrame(student_screen, corner_radius=0)
    modify_buttons_student.pack(side=ctk.TOP,fill=ctk.X, padx=0,pady=0)
    modify_buttons_student.configure(width=200)


    for i in range(4):
        modify_buttons_student.grid_columnconfigure(i,weight=1)
    #add update delete show 

    add_student = ctk.CTkButton(modify_buttons_student,text="Add",font=("Gudea",15,"bold"), corner_radius=0, command=lambda:change_to_add_screen_student())
    add_student.grid(row=0,column=0,sticky="ew",padx=0,pady=0)

    edit_student = ctk.CTkButton(modify_buttons_student,text="Edit/Update",font=("Gudea",15,"bold"), corner_radius=0,command=lambda:change_to_update_screen_student())
    edit_student.grid(row=0,column=1,sticky="ew",padx=0,pady=0)

    delete_student = ctk.CTkButton(modify_buttons_student,text="Delete",font=("Gudea",15,"bold"), corner_radius=0, command=lambda:change_to_delete_screen_student())
    delete_student.grid(row=0,column=2,sticky="ew",padx=0,pady=0)

    show_student = ctk.CTkButton(modify_buttons_student,text="Show",font=("Gudea",15,"bold"), corner_radius=0, command=lambda:change_to_show_screen_student())
    show_student.grid(row=0,column=3,sticky="ew",padx=0,pady=0)

    #operation (Add) Screen
    main_content_student_update = ctk.CTkFrame(student_screen, corner_radius=0)
    main_content_student_update.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)

    
    add_student_scroll = ctk.CTkScrollableFrame(main_content_student_update)
    add_student_scroll.pack(side = ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)

    adding_student = ctk.CTkFrame(add_student_scroll)
    adding_student.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)

    editing_student = ctk.CTkFrame(main_content_student_update)
    editing_student.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)

    deleting_student = ctk.CTkFrame(main_content_student_update)
    deleting_student.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
    
    showing_student = ctk.CTkFrame(main_content_student_update)
    showing_student.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)

    editing_student.pack_forget()
    deleting_student.pack_forget()
    showing_student.pack_forget()
    
    #Adding student Section

    for i in range(4):
        adding_student.grid_columnconfigure(i,weight=1)
    for j in range(13):
        adding_student.grid_rowconfigure(j,weight=0)


    batch_year_lbl = ctk.CTkLabel(adding_student, text="\tSelect Batch Year", font=("Gudea", 15, "bold"), anchor="w")
    batch_year_lbl.grid(row=0, column=0, sticky="ew", padx=10,pady=10)
    
     # Retrieving Batch
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT batch_year FROM batch ORDER BY batch_year Desc"
        cursor.execute(query)
        batch_values = [f"{row[0]}".strip() for row in cursor.fetchall()]
        conn.close()
        # return student_names_to_display
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
        batch_values = []

    select_batch = ctk.CTkComboBox(adding_student, values = batch_values, state="readonly",font=("Gudea", 12, "bold"))
    select_batch.grid(row=0, column=1,sticky="ew", padx=10,pady=10)
    select_batch.set("--Select--")

    fname_lbl_s = ctk.CTkLabel(adding_student, text="\tFirst Name",font=("Gudea", 15,"bold"), anchor="w")
    fname_lbl_s.grid(row=1, column=0, sticky="ew", padx=10,pady=10)

    fname_entry_s = ctk.CTkEntry(adding_student, placeholder_text="Enter First Name", font=("Gudea", 12,"bold"))
    fname_entry_s.grid(row=1, column=1,sticky="ew",  padx=10,pady=10)

    mname_lbl_s = ctk.CTkLabel(adding_student, text="\tMiddle Name", font=("Gudea", 15, "bold"), anchor="w")
    mname_lbl_s.grid(row=1, column=2,sticky="ew", padx=10,pady=10)

    mname_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Middle Name",font=("Gudea", 12, "bold"))
    mname_entry_s.grid(row=1, column=3,sticky="ew", padx=10,pady=10)
    
    lname_s = ctk.CTkLabel(adding_student, text="\tLast Name", font=("Gudea", 15, "bold"), anchor="w")
    lname_s.grid(row=2, column=0,sticky="ew", padx=10,pady=10)

    lname_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Last Name",font=("Gudea", 12, "bold"))
    lname_entry_s.grid(row=2, column=1,sticky="ew", padx=10,pady=10)

    uid_lbl_s = ctk.CTkLabel(adding_student, text="\tUID (Adhaar No.)", font=("Gudea", 15, "bold"), anchor="w")
    uid_lbl_s.grid(row=2, column=2, sticky="ew", padx=10,pady=10)

    uid_entry_s = ctk.CTkEntry(adding_student, placeholder_text="Enter Adhaar No.", font=("Gudea", 12, "bold"))
    uid_entry_s.grid(row=2, column=3,sticky="ew",  padx=10,pady=10)

    dob_lbl_s = ctk.CTkLabel(adding_student, text="\tDate of Birth", font=("Gudea", 15, "bold"), anchor="w")
    dob_lbl_s.grid(row=3, column=0,sticky="ew", padx=10,pady=10)

    dob_entry_s = ctk.CTkEntry(adding_student,placeholder_text="YYYY-MM-DD",font=("Gudea", 12, "bold"))
    dob_entry_s.grid(row=3, column=1,sticky="ew", padx=10,pady=10)

    gender_lbl_s = ctk.CTkLabel(adding_student, text="\tGender", font=("Gudea", 15, "bold"), anchor="w")
    gender_lbl_s.grid(row=3, column=2,sticky="ew", padx=10,pady=10)

    select_gender = ctk.CTkComboBox(adding_student, values=["Male","Female","Other"], state="readonly",font=("Gudea", 12, "bold"))
    select_gender.grid(row=3, column=3,sticky="ew", padx=10,pady=10)
    select_gender.set("--Select--")

    std_lbl_s = ctk.CTkLabel(adding_student, text="\tApplying for Course", font=("Gudea", 15, "bold"), anchor="w")
    std_lbl_s.grid(row=4, column=0,sticky="ew", padx=10,pady=10)

    def get_course():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT course_name FROM courses ORDER BY course_name"
            cursor.execute(query)
            course_names = [f"{row[0]}".strip() for row in cursor.fetchall()]
            conn.close()
            return course_names

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            return []

    course_name = get_course() 
    course_name_sorted = natsorted(course_name)
    select_std = ctk.CTkComboBox(adding_student, values = course_name_sorted, state="readonly",font=("Gudea", 12, "bold"))
    select_std.grid(row=4, column=1,sticky="ew", padx=10,pady=10)
    select_std.set("--Select--")

    medium_lbl_s = ctk.CTkLabel(adding_student, text="\tMedium", font=("Gudea", 15, "bold"), anchor="w")
    medium_lbl_s.grid(row=4, column=2,sticky="ew", padx=10,pady=10)

    select_medium = ctk.CTkComboBox(adding_student, values=["English","Hindi","Marathi","Urdu"], state="readonly",font=("Gudea", 12, "bold"))
    select_medium.grid(row=4, column=3,sticky="ew", padx=10,pady=10)
    select_medium.set("--Select--")

    school_lbl_s = ctk.CTkLabel(adding_student, text="\tSchool", font=("Gudea", 15, "bold"), anchor="w")
    school_lbl_s.grid(row=5, column=0,sticky="ew", padx=10,pady=10)

    school_entry_s = ctk.CTkEntry(adding_student, placeholder_text="Enter School Name", font=("Gudea", 12, "bold"))
    school_entry_s.grid(row=5, column=1, columnspan=3, sticky="ew", padx=10,pady=10)

    Address_lbl_s = ctk.CTkLabel(adding_student, text="\tAddress", font=("Gudea", 15, "bold"), anchor="w")
    Address_lbl_s.grid(row=6, column=0,sticky="ew", padx=10,pady=10)

    Address_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Full Address",font=("Gudea", 12, "bold"))
    Address_entry_s.grid(row=6, column=1, columnspan=3, sticky="ew", padx=10,pady=10)

    admission_lbl_s = ctk.CTkLabel(adding_student, text="\tDate of Admission", font=("Gudea", 15, "bold"), anchor="w")
    admission_lbl_s.grid(row=7, column=0,sticky="ew", padx=10,pady=10)

    admission_entry_s = ctk.CTkEntry(adding_student,placeholder_text="YYYY-MM-DD",font=("Gudea", 12, "bold"))
    admission_entry_s.grid(row=7, column=1,sticky="ew", padx=10,pady=10)

    mother_lbl_s = ctk.CTkLabel(adding_student, text="\tMother Name", font=("Gudea", 15, "bold"), anchor="w")
    mother_lbl_s.grid(row=7, column=2,sticky="ew", padx=10,pady=10)

    mother_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Mother Name",font=("Gudea", 12, "bold"))
    mother_entry_s.grid(row=7, column=3, sticky="ew", padx=10,pady=10)

    father_occu_lbl_s = ctk.CTkLabel(adding_student, text="\tFather Occupation", font=("Gudea", 15, "bold"), anchor="w")
    father_occu_lbl_s.grid(row=8, column=0,sticky="ew", padx=10,pady=10)

    father_occu_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Father Occupation",font=("Gudea", 12, "bold"))
    father_occu_entry_s.grid(row=8, column=1,sticky="ew", padx=10,pady=10)

    mother_occu_lbl_s = ctk.CTkLabel(adding_student, text="\tMother Occupation", font=("Gudea", 15, "bold"), anchor="w")
    mother_occu_lbl_s.grid(row=8, column=2,sticky="ew", padx=10,pady=10)

    mother_occu_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Mother Occupation",font=("Gudea", 12, "bold"))
    mother_occu_entry_s.grid(row=8, column=3, sticky="ew", padx=10,pady=10)

    primary_no_lbl_s = ctk.CTkLabel(adding_student, text="\tPrimary no.", font=("Gudea", 15, "bold"), anchor="w")
    primary_no_lbl_s.grid(row=9, column=0,sticky="ew", padx=10,pady=10)

    primary_no_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Mobile No.",font=("Gudea", 12, "bold"))
    primary_no_entry_s.grid(row=9, column=1,sticky="ew", padx=10,pady=10)

    secondary_no_lbl_s = ctk.CTkLabel(adding_student, text="\tSecondary No.", font=("Gudea", 15, "bold"), anchor="w")
    secondary_no_lbl_s.grid(row=9, column=2,sticky="ew", padx=10,pady=10)

    secondary_no_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Mobile No.",font=("Gudea", 12, "bold"))
    secondary_no_entry_s.grid(row=9, column=3, sticky="ew", padx=10,pady=10)

    email_lbl_s = ctk.CTkLabel(adding_student, text="\tEmail ID", font=("Gudea", 15, "bold"), anchor="w")
    email_lbl_s.grid(row=10, column=0, sticky="ew", padx=10,pady=10)

    email_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Email",font=("Gudea", 12, "bold"))
    email_entry_s.grid(row=10, column=1, sticky="ew", padx=10,pady=10)

    ref_lbl_s = ctk.CTkLabel(adding_student, text="\tReference", font=("Gudea", 15, "bold"), anchor="w")
    ref_lbl_s.grid(row=10, column=2,sticky="ew", padx=10,pady=10)

    select_ref = ctk.CTkComboBox(adding_student, values=["Walk-In","Friend","Advertise"], state="readonly",font=("Gudea", 12, "bold"))
    select_ref.grid(row=10, column=3,sticky="ew", padx=10,pady=10)
    select_ref.set("--Select--")

    description_lbl_s = ctk.CTkLabel(adding_student, text="\tDescription", font=("Gudea", 15, "bold"), anchor="w")
    description_lbl_s.grid(row=11, column=0,sticky="ew", padx=10,pady=10)

    description_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Description (Optional)",font=("Gudea", 12, "bold"))
    description_entry_s.grid(row=11, column=1,sticky="ew", padx=10,pady=10)

    fees_lbl_s = ctk.CTkLabel(adding_student, text="\tTotal Fees", font=("Gudea", 15, "bold"), anchor="w")
    fees_lbl_s.grid(row=11, column=2,sticky="ew", padx=10,pady=10)

    fees_entry_s = ctk.CTkEntry(adding_student,placeholder_text="Enter Total Fees",font=("Gudea", 12, "bold"))
    fees_entry_s.grid(row=11, column=3,sticky="ew", padx=10,pady=10)


    def validate_students_detail():
        errors = []
        if select_batch.get() == "--Select--":
            errors.append("Batch Year not selected")

        if not fname_entry_s.get().isalpha():
            errors.append("First name should contain only alphabets.")

        if not mname_entry_s.get().isalpha():
            errors.append("Middle name should contain only alphabets.")

        if not lname_entry_s.get().isalpha():
            errors.append("Last name should contain only alphabets.")

        if not re.match(r"^\d{12}$", uid_entry_s.get()):
            errors.append("UID must be exactly 12 digits.")

        # Date validation start 
        dob_str = dob_entry_s.get().strip()
        if len(dob_str) == 0:
            errors.append("Date of Birth cannot be empty")

        if not all(c.isdigit() or c == '-' for c in dob_str):
            errors.append("Date of Birth must contain only numbers and hyphens.")
        
        if len(dob_str) != 10 or dob_str[4] != '-' or dob_str[7] != '-':
            errors.append("Invalid Date of Birth Format")

        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid Date of Birth")
        # Date validation end


        if select_gender.get() == "--Select--":
            errors.append("Gender not selected")

        if select_std.get() == "--Select--":
            errors.append("Standard not selected")

        if select_medium.get() == "--Select--":
            errors.append("Medium not selected")

        if not (school_entry_s).get().strip():
            errors.append("School cannot be empty")
        
        if not Address_entry_s.get().strip():
            errors.append("Address cannot be empty")

        addmission_str = admission_entry_s.get().strip()
        if len(addmission_str) == 0:
            errors.append("Date of Admission cannot be empty")

        if not all(c.isdigit() or c == '-' for c in addmission_str):
            errors.append("Date of Admission must contain only numbers and hyphens.")
        
        if len(addmission_str) != 10 or addmission_str[4] != '-' or addmission_str[7] != '-':
            errors.append("Invalid Date of Admission Format")

        try:
            add = datetime.strptime(addmission_str, "%Y-%m-%d")
        except ValueError:
            errors.append("Invalid Admission Date")

        if not mother_entry_s.get().isalpha():
            errors.append("Mother name should contain only alphabets.")

        if not re.match(r'^[A-Za-z\s]+$',father_occu_entry_s.get()):
            errors.append("Father Occupation should contain only alphabets.")

        if not re.match(r'^[A-Za-z ]+$',mother_occu_entry_s.get()):
            errors.append("Mother Occupation should contain only alphabets.")

        if not re.match(r"^\d{10}$", primary_no_entry_s.get()):
            errors.append("Mobile number must be exactly 10 digits.")
        
        if not re.match(r"^\d{10}$", secondary_no_entry_s.get()):
            errors.append("Mobile number must be exactly 10 digits.")

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email_entry_s.get()):
            errors.append("Invalid email format.")

        if select_ref.get() == "--Select--":
             errors.append("Reference not Selected")

        if not fees_entry_s.get().strip():
            errors.append("Total Fees cannot be empty")

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return False  # Stop execution if there are validation errors

        return True  # Proceed if all validations pass

    # def test():
    #     print(fname_entry_s.get(), mname_entry_s.get(), lname_entry_s.get(), uid_entry_s.get(), dob_entry_s.get(), select_gender_student.get(), select_std_student.get(), select_medium_student.get(), school_entry_s.get(), Address_entry_s.get(), mother_entry_s.get(), father_occu_entry_s.get(), mother_entry_s.get(), primary_no_entry_s.get(), secondary_no_entry_s.get(), email_entry_s.get(), select_ref_student.get(), description_entry_s.get(), fees_entry_s.get())
    

    def insert_students():
        #print(fname_entry_s.get(),"\n",mname_entry_s.get(), "\n",lname_entry_s.get(), "\n",uid_entry_s.get(), "\n",dob_entry_s.get(),"\n", select_gender.get(),"\n", select_std.get(),"\n", select_medium.get(),"\n", school_entry_s.get(), "\n",Address_entry_s.get(), "\n",mother_entry_s.get(), "\n",father_occu_entry_s.get(), "\n",mother_entry_s.get(),"\n", primary_no_entry_s.get(),"\n", secondary_no_entry_s.get(),"\n", email_entry_s.get(), "\n",select_ref.get(),"\n", description_entry_s.get(),"\n", fees_entry_s.get(),"\n", select_batch.get())
        if not validate_students_detail():
            return
        #MySql query
        try: 
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO students_detail (first_name, middle_name, last_name, uid, dob, gender, class, s_medium, school, address, date_of_addmission, mother_name, father_occupation, mother_occupation, primary_no, secondary_no,email, reference_via, s_description, total_fees, academic_year, total_paid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (fname_entry_s.get(), mname_entry_s.get(), lname_entry_s.get(), uid_entry_s.get(), dob_entry_s.get(), select_gender.get(), select_std.get(), select_medium.get(), school_entry_s.get(), Address_entry_s.get(), admission_entry_s.get(), mother_entry_s.get(), father_occu_entry_s.get(), mother_occu_entry_s.get(), primary_no_entry_s.get(), secondary_no_entry_s.get(), email_entry_s.get(), select_ref.get(), description_entry_s.get(), fees_entry_s.get(),select_batch.get(),0)
            cursor.execute(query,values)
            conn.commit()    
            conn.close()

            messagebox.showinfo("Success", "Student info updated successfully!")
            clear_entries_s()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data: {err}")


    def clear_entries_s():
        select_batch.set("--Select--")
        fname_entry_s.delete(0, ctk.END)
        mname_entry_s.delete(0, ctk.END)
        lname_entry_s.delete(0, ctk.END)
        uid_entry_s.delete(0, ctk.END)
        dob_entry_s.delete(0, ctk.END)
        select_gender.set("--Select--")
        select_std.set("--Select--")
        select_medium.set("--Select--")
        school_entry_s.delete(0, ctk.END)
        Address_entry_s.delete(0, ctk.END)
        admission_entry_s.delete(0, ctk.END)
        mother_entry_s.delete(0, ctk.END)
        father_occu_entry_s.delete(0, ctk.END)
        mother_occu_entry_s.delete(0, ctk.END)
        primary_no_entry_s.delete(0, ctk.END)
        secondary_no_entry_s.delete(0, ctk.END)
        email_entry_s.delete(0, ctk.END)
        select_ref.set("--Select--")
        description_entry_s.delete(0, ctk.END)
        fees_entry_s.delete(0, ctk.END)

        fname_entry_s._activate_placeholder()
        mname_entry_s._activate_placeholder()
        lname_entry_s._activate_placeholder()
        uid_entry_s._activate_placeholder()
        dob_entry_s._activate_placeholder()
        school_entry_s._activate_placeholder()
        Address_entry_s._activate_placeholder()
        admission_entry_s._activate_placeholder()
        mother_entry_s._activate_placeholder()
        father_occu_entry_s._activate_placeholder()
        mother_occu_entry_s._activate_placeholder()
        primary_no_entry_s._activate_placeholder()
        secondary_no_entry_s._activate_placeholder()
        email_entry_s._activate_placeholder()
        description_entry_s._activate_placeholder()
        fees_entry_s._activate_placeholder()

        adding_student.focus_set()

    add_btn_s = ctk.CTkButton(adding_student, text="Add Student",font=("Gudea", 15, "bold"),command=insert_students)
    add_btn_s.grid(row=12, column=0,columnspan=2,sticky="ew", padx=10,pady=10)

    clear_btn_s = ctk.CTkButton(adding_student, text="Clear",font=("Gudea", 15, "bold"),command=clear_entries_s)
    clear_btn_s.grid(row=12, column=2,columnspan=2,sticky="ew", padx=10,pady=10)


    # Editing / Upating Student


    def get_student_name():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT student_id, first_name, middle_name, last_name FROM students_detail"
            cursor.execute(query)
            student_names = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]

            conn.close()
            return student_names
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            return []

    def update_input_field(*args):
        selected_student = student_dropdown_u.get()
        selected_option = select_option_u.get()
        
        if selected_student != "--Select--" and selected_option != "--Select--":
            input_for_update.delete(0, ctk.END)
            input_for_update.grid(row=2, column=1, columnspan=2, sticky="ew", padx=10, pady=10)
        else:
            input_for_update.grid_forget()

    def clear_info_u():
        select_option_u.set("--Select--")
        student_dropdown_u.set("--Select--")
        input_for_update.delete(0, ctk.END)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT student_id, first_name, middle_name, last_name FROM students_detail"
            cursor.execute(query)
            student_names = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
            conn.close()
            
            student_dropdown_u.configure(values = student_names)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            return False
        
        input_for_update.grid_forget()



    def update_student_info():
        selected_student = student_dropdown_u.get()
        selected_option = select_option_u.get()
        new_value = input_for_update.get().strip()

        if selected_student == "--Select--":
            messagebox.showerror("Error", "Please select a student.")
            return
        
        if selected_option == "--Select--":
            messagebox.showerror("Error", "Please select an attribute to update.")
            return
        
        if not new_value:
            messagebox.showerror("Error", "Input cannot be empty.")
            return

        student_id = selected_student.split(" - ")[0]  # Extract student ID

        option_to_column = {
            "Primary Contact No.": "primary_no",
            "Secondary Contact No.": "secondary_no",
            "Email-ID": "email",
            "Address": "address",
            "Description": "s_description",
            "Total fees": "total_fees"
        }
        column_name = option_to_column.get(selected_option)



        # Validation rules
        if selected_option == "Primary Contact No." and not re.match(r"^\d{10}$", new_value):
            messagebox.showerror("Error", "Primary number must be exactly 10 digits.")
            return
        
        if selected_option == "Secondary Contact No." and not re.match(r"^\d{10}$", new_value):
            messagebox.showerror("Error", "Secondary number must be exactly 10 digits.")
            return
        
        if selected_option == "Email-ID" and not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", new_value):
            messagebox.showerror("Error", "Invalid email format.")
            return
        
        if selected_option == "Address" and len(new_value) == 0:
            messagebox.showerror("Error", "Address cannot be empty.")
            return
        
        if selected_option == "Total fees" and len(new_value) == 0:
            messagebox.showerror("Error", "Total fees cannot be empty.")
            return
        
        if selected_option == "Total fees" and not new_value.isdigit():
            messagebox.showerror("Error", "Total fees must be in digit")
            return
        
        if selected_option == "Total fees":
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                
                query = "SELECT total_paid FROM students_detail WHERE student_id = %s"
                cursor.execute(query, (student_id,))
                # total_paid = [f"{row[0]}".strip() for row in cursor.fetchone()]
                total_paid = cursor.fetchone()
                conn.close()

                if total_paid is None:
                    messagebox.showerror("Error", f"No data found for student ID {student_id}")
                    return
                
                if float(total_paid[0]) > float(new_value):
                    messagebox.showerror("Error", f"Total Fees Cannot be less than Total Fees Paid")
                    return
                
            except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    return
        



        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if the value already exists
            query = f"SELECT {column_name} FROM students_detail WHERE {column_name} = %s AND student_id = %s"
            cursor.execute(query, (new_value, student_id))
            if cursor.fetchone():
                messagebox.showerror("Error", f"The {selected_option} already exists for student id {student_id}.")
                return
            
            # Update the value
            query = f"UPDATE students_detail SET {column_name} = %s WHERE student_id = %s"
            cursor.execute(query, (new_value, student_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Student info updated successfully!")
            clear_info_u()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating data: {err}")


    for row in range(4):
        editing_student.grid_rowconfigure(row, weight=0)
    for col in range(3):
        editing_student.grid_columnconfigure(col, weight=1)

    # Select Student
    ctk.CTkLabel(editing_student, text="Select Student", font=("Gudea", 15, "bold")).grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    students_name_u = get_student_name()

    #select_student_name_u = ctk.StringVar()
    student_dropdown_u = ctk.CTkComboBox(editing_student, values=students_name_u, state="readonly", font=("Gudea", 12, "bold"))
    student_dropdown_u.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
    student_dropdown_u.set("--Select--")

    # Select Attribute to Update
    ctk.CTkLabel(editing_student, text="Select to update", font=("Gudea", 15, "bold")).grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    #select_option_var_u = ctk.StringVar()
    select_option_u = ctk.CTkComboBox(editing_student, values=["Primary Contact No.", "Secondary Contact No.", "Email-ID", "Address", "Description", "Total fees"], state="readonly", font=("Gudea", 12, "bold"))
    select_option_u.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
    select_option_u.set("--Select--")

    #select_option_u.trace_add("write", update_input_field)
    select_option_u.configure(command=update_input_field)

    input_for_update = ctk.CTkEntry(editing_student, font=("Gudea", 12, "bold"))

    update_btn = ctk.CTkButton(editing_student, text="UPDATE", font=("Gudea", 15, "bold"), command=update_student_info)
    update_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=50)

    clear_btn = ctk.CTkButton(editing_student, text="CLEAR / REFRESH", font=("Gudea", 15, "bold"), command=clear_info_u)
    clear_btn.grid(row=3, column=1, sticky="ew", padx=10, pady=50)



    # deleting Student

    def delete_student():

        msg = CTkMessagebox(
            title="Deleting Student", 
            message="It is not Recommended to delete student if minimum 1 Fees, Attendance, Marks is done \n\nYou can't undo it \n\nDo you really want to Delete Student",
            icon="warning",  # "info", "warning", "error"
            option_1="Cancel",
            option_2="Yes"
        )
        
        # Get user's choice
        response = msg.get()
        
        if response != "Yes":
            return False
        

        selected_student = student_dropdown.get().strip()
        
        if not selected_student or selected_student == "--Select Student--":
            messagebox.showerror("Error", "Please select a student.")
            return
        
        student_id = selected_student.split(" - ")[0]  # Extract student ID
        
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
            query = "DELETE FROM students_detail WHERE student_id = %s"
            cursor.execute(query, (student_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Student record deleted successfully!")
            refresh_student_list()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting data: {err}")

    def refresh_student_list():
        students_name = get_student_name()
        students_name.insert(0, "--Select Student--")
        student_dropdown.configure(values=students_name)
        student_dropdown.set("--Select Student--")

    for i in range(1):
        deleting_student.grid_rowconfigure(i,weight=0)
    for j in range(2):
        deleting_student.grid_columnconfigure(j,weight=1)


    # Dropdown: Select Student
    students_name = get_student_name()
    students_name.insert(0, "--Select Student--")

    #select_student_name = ctk.StringVar()
    student_dropdown = ctk.CTkComboBox(deleting_student, values=students_name, state="readonly",font=("Arial", 12, "bold"))
    student_dropdown.grid(row=0,column=0,sticky="ew",padx=15, pady=10)
    student_dropdown.set("--Select Student--")

    # Delete Button
    delete_btn = ctk.CTkButton(deleting_student, text="Delete Student", font=("Arial", 12, "bold"), fg_color="red", text_color="white", command=delete_student)
    delete_btn.grid(row=0, column=1, sticky="ew", columnspan=2,padx=15, pady=10)

        

    
    def view_student(s_id):

        # Create new window
        view_student_detail = ctk.CTkToplevel()  # Use CTkToplevel instead of CTk for child windows
        view_student_detail.geometry("800x600")
        view_student_detail.title(f"Teacher Details - {s_id}")
        
        # This prevents the DPI scaling errors
        view_student_detail.after(100, lambda: view_student_detail.focus_force())
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier access
            
            # Fetch teacher data
            query = """SELECT student_id, first_name, middle_name, last_name, uid, dob, gender, class, s_medium, school, address, date_of_addmission, mother_name, father_occupation, mother_occupation, primary_no, secondary_no, email, s_description, reference_via, total_fees, academic_year, total_paid, pending_fees 
                    FROM students_detail WHERE student_id = %s"""
            cursor.execute(query, (s_id,))
            student = cursor.fetchone()
            
            if not student:
                ctk.CTkLabel(view_student_detail, text="Student not found").pack()
                return
                
            # Create display frame

            scroll_frame = ctk.CTkScrollableFrame(view_student_detail)
            scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

            info_frame = ctk.CTkFrame(scroll_frame)
            info_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # Display teacher info in a grid
            labels = [
                ("Student ID", student['student_id']),
                ("Name", f"{student['first_name']} {student['middle_name']} {student['last_name']}"),
                ("UID No", student['uid']),
                ("Date of Birth", student['dob']),
                ("Gender", student['gender']),
                ("Class", student['class']),
                ("Medium", student['s_medium']),
                ("School", student['school']),
                ("Address", student['address']),
                ("Date of Admission", student['date_of_addmission']),
                ("Mother Name", student['mother_name']),
                ("Father Occupation", student['father_occupation']),
                ("Mother Occupation", student['mother_occupation']),
                ("Primary Phone", student['primary_no']),
                ("Secondary Phone", student['secondary_no']),
                ("Email", student['email']),
                ("Description", student['s_description']),
                ("Reference Via", student['reference_via']),
                ("Total Fees", student['total_fees']),
                ("Total Fees Paid", student['total_paid']),
                ("Pending Fees", student['pending_fees'])
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
            view_student_detail.destroy()
            
        view_student_detail.protocol("WM_DELETE_WINDOW", on_close)
    
    
    
   
    def setup_student_display():
        # Initialize the items list
        items = []
        
        # Function to fetch data from database
        def fetch_student_data():
            nonlocal items
            S_class = select_course.get()
            batch = select_batch.get()

            if (S_class == "All" and batch == "All"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT student_id, first_name, middle_name, last_name FROM students_detail"
                    cursor.execute(query)
                    items = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []
                
            if (S_class == "All" and batch != "All"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT student_id, first_name, middle_name, last_name FROM students_detail WHERE academic_year = %s"
                    cursor.execute(query,(batch,))
                    items = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

            if (S_class != "All" and batch == "All"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT student_id, first_name, middle_name, last_name FROM students_detail WHERE class = %s"
                    cursor.execute(query, (S_class,))
                    items = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

            if (S_class != "All" and batch != "All"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT student_id, first_name, middle_name, last_name FROM students_detail WHERE class = %s and academic_year = %s"
                    cursor.execute(query, (S_class,batch))
                    items = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []
        
        # Function to refresh the display
        def refresh_display():
            nonlocal items
            # Destroy existing widgets
            for widget in display_student.winfo_children():
                widget.destroy()
            
            # Fetch fresh data
            fetch_student_data()
            
            # Rebuild the display
            for i in range(len(items)+1):
                display_student.grid_rowconfigure(i, weight=0)
            for j in range(4):
                display_student.grid_columnconfigure(j, weight=1)
            
            # Header row
            ctk.CTkLabel(display_student, text="Serial No.").grid(row=0, column=0)
            ctk.CTkLabel(display_student, text="Student ID").grid(row=0, column=1)
            ctk.CTkLabel(display_student, text="Student Name").grid(row=0, column=2)
            ctk.CTkLabel(display_student, text="Action").grid(row=0, column=3)
            
            # Data rows
            for i, item in enumerate(items, start=1):
                student_id, student_name = item.split(" - ")
                ctk.CTkLabel(display_student, text=str(i)).grid(row=i, column=0)
                ctk.CTkLabel(display_student, text=student_id).grid(row=i, column=1)
                ctk.CTkLabel(display_student, text=student_name).grid(row=i, column=2)
                ctk.CTkButton(
                    display_student,
                    text="View",
                    command=lambda sid=student_id: view_student(sid)
                ).grid(row=i, column=3, pady=5)

        

        set_search_frame = ctk.CTkFrame(showing_student)
        set_search_frame.pack(side = ctk.TOP, fill = ctk.X, padx = 10, pady = 10, anchor = "n")

        for i in range(5):
            set_search_frame.grid_columnconfigure(i, weight = 1)
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT course_name FROM Courses"
            cursor.execute(query)
            course = [f"{row[0]}".strip() for row in cursor.fetchall()]
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            course = []

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT batch_year FROM batch"
            cursor.execute(query)
            batch = [f"{row[0]}".strip() for row in cursor.fetchall()]
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            batch = []


        ctk.CTkLabel(set_search_frame, text = "Select Class").grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)
        select_course = ctk.CTkComboBox(set_search_frame, values = course)
        select_course.grid(row = 0, column = 1, sticky = "ew", padx = 5, pady = 5)
        select_course.set("All")

        ctk.CTkLabel(set_search_frame, text = "Select Batch Year").grid(row = 0, column = 2, sticky = "ew", padx = 5, pady = 5)
        select_batch = ctk.CTkComboBox(set_search_frame, values = batch)
        select_batch.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)
        select_batch.set("All")


        ctk.CTkComboBox(showing_student)

        
        # Create scrollable frame (only once)
        scrollable_frame_student = ctk.CTkScrollableFrame(showing_student)
        scrollable_frame_student.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # Create display frame (only once)
        display_student = ctk.CTkFrame(scrollable_frame_student)
        display_student.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10, expand=True)
        
        # Add refresh button
        refresh_btn = ctk.CTkButton(
            showing_student,
            text="Refresh",
            command=refresh_display
        )
        refresh_btn.pack(side=ctk.TOP, pady=10)
        
        # Initial data load
        refresh_display()

    # Call the setup function
    setup_student_display()
    return student_screen