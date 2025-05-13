import customtkinter as ctk
from tkinter import messagebox, simpledialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from db_connection import get_db_connection
import mysql.connector
import re
from datetime import datetime
from db_connection import get_db_connection 
from CTkMessagebox import CTkMessagebox

def teacher_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen):
    dashboard_screen.pack_forget()
    student_screen.pack_forget()
    payment_screen.pack_forget()
    fees_screen.pack_forget()
    attendance_screen.pack_forget()
    exam_screen.pack_forget()
    profile_screen.pack_forget()
    expense_screen.pack_forget()
    teacher_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

def create_teacher_screen(root, screen_width, menu_bar_color):
    teacher_screen = ctk.CTkFrame(root, fg_color="white")
    teacher_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    teacher_screen.configure(width=screen_width - 50)

    # Teacher title strip
    teacher_title_bar = ctk.CTkFrame(teacher_screen, fg_color=menu_bar_color, corner_radius=0, border_width=0)
    teacher_title_bar.pack(side=ctk.TOP, fill=ctk.X, pady=0)
    teacher_title_bar.configure(height=100)

    # Teacher Panel Title
    teacher_title = ctk.CTkLabel(teacher_title_bar, text="Teacher's Section", fg_color=menu_bar_color, text_color="white", font=("Gudea", 20, "bold"))
    teacher_title.pack(expand=True, anchor="center",pady=15)

    def change_to_add_screen():
        adding_teacher.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
        editing_teacher.pack_forget()
        deleting_teacher.pack_forget()
        showing_teacher.pack_forget()

    def change_to_update_screen():
        editing_teacher.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
        adding_teacher.pack_forget()
        deleting_teacher.pack_forget()
        showing_teacher.pack_forget()
    
    def change_to_delete_screen():
        deleting_teacher.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
        adding_teacher.pack_forget()
        editing_teacher.pack_forget()
        showing_teacher.pack_forget()

    def change_to_show_screen():
        showing_teacher.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
        adding_teacher.pack_forget()
        editing_teacher.pack_forget()
        deleting_teacher.pack_forget()

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
    modify_buttons = ctk.CTkFrame(teacher_screen, corner_radius=0)
    modify_buttons.pack(side=ctk.TOP,fill=ctk.X, padx=0,pady=0)
    modify_buttons.configure(width=200)


    for i in range(4):
        modify_buttons.grid_columnconfigure(i,weight=1)
    #add update delete show 

    add_teacher = ctk.CTkButton(modify_buttons,text="Add",font=("Gudea",15,"bold"), corner_radius=0, command=lambda:change_to_add_screen())
    add_teacher.grid(row=0,column=0,sticky="ew",padx=0,pady=0)

    edit_teacher = ctk.CTkButton(modify_buttons,text="Edit/Update",font=("Gudea",15,"bold"), corner_radius=0,command=lambda:change_to_update_screen())
    edit_teacher.grid(row=0,column=1,sticky="ew",padx=0,pady=0)

    delete_teacher = ctk.CTkButton(modify_buttons,text="Delete",font=("Gudea",15,"bold"), corner_radius=0, command=lambda:change_to_delete_screen())
    delete_teacher.grid(row=0,column=2,sticky="ew",padx=0,pady=0)

    show_teacher = ctk.CTkButton(modify_buttons,text="Show",font=("Gudea",15,"bold"), corner_radius=0,command=lambda:change_to_show_screen())
    show_teacher.grid(row=0,column=3,sticky="ew",padx=0,pady=0)


    #operation (Add) Screen
    main_content_teachers_update = ctk.CTkFrame(teacher_screen)
    main_content_teachers_update.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)

    
    adding_teacher = ctk.CTkFrame(main_content_teachers_update, corner_radius=0)
    adding_teacher.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)

    editing_teacher = ctk.CTkFrame(main_content_teachers_update, corner_radius=0)
    editing_teacher.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
    
    deleting_teacher = ctk.CTkFrame(main_content_teachers_update, corner_radius=0)
    deleting_teacher.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)
    
    showing_teacher = ctk.CTkFrame(main_content_teachers_update, corner_radius=0)
    showing_teacher.pack(side=ctk.LEFT, fill=ctk.BOTH, padx=0,pady=0, expand=True)


    editing_teacher.pack_forget()
    deleting_teacher.pack_forget()
    showing_teacher.pack_forget()
    
    

    #Adding teacher Section

    for i in range(4):
        adding_teacher.grid_columnconfigure(i,weight=1)
    for j in range(10):
        adding_teacher.grid_rowconfigure(j,weight=0)


    
    font_family_lbl = "Gudea"
    font_family_entry = "Gudea"
    font_size_lbl = 15
    font_size_entry = 12

    fname_lbl = ctk.CTkLabel(adding_teacher, text="\tFirst Name",font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    fname_lbl.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    fname_entry = ctk.CTkEntry(adding_teacher, placeholder_text="Enter First Name",font=(font_family_entry, font_size_entry, "bold"))
    fname_entry.grid(row=0, column=1,sticky="ew",  padx=10,pady=10)

    mname_lbl = ctk.CTkLabel(adding_teacher, text="\tMiddle Name", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    mname_lbl.grid(row=0, column=2,sticky="ew", padx=10,pady=10)

    mname_entry = ctk.CTkEntry(adding_teacher,placeholder_text="Enter Middle Name", font=(font_family_entry, font_size_entry, "bold"))
    mname_entry.grid(row=0, column=3,sticky="ew", padx=10,pady=10)
    
    lname = ctk.CTkLabel(adding_teacher, text="\tLast Name", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    lname.grid(row=1, column=0,sticky="ew", padx=10,pady=10)

    lname_entry = ctk.CTkEntry(adding_teacher, placeholder_text="Enter Last Name",font=(font_family_entry, font_size_entry, "bold"))
    lname_entry.grid(row=1, column=1,sticky="ew", padx=10,pady=10)

    uid_lbl = ctk.CTkLabel(adding_teacher, text="\tUID (Adhaar No.)", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    uid_lbl.grid(row=1, column=2, sticky="ew", padx=10,pady=10)

    uid_entry = ctk.CTkEntry(adding_teacher, placeholder_text="Enter Adhaar No.", font=(font_family_entry, font_size_entry, "bold"))
    uid_entry.grid(row=1, column=3,sticky="ew",  padx=10,pady=10)



    gender_lbl = ctk.CTkLabel(adding_teacher,text="\tGender", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    gender_lbl.grid(row=2, column=0, sticky="ew", padx=10,pady=10)

    select_gender = ctk.CTkComboBox(adding_teacher, values=["Male","Female","Other"], state="readonly",font=(font_family_entry, font_size_entry, "bold"))
    select_gender.grid(row=2, column=1, sticky="ew", padx=10, pady=10)
    select_gender.set("--Select--")



    mobile_lbl_1 = ctk.CTkLabel(adding_teacher, text="\tPrimary No.", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    mobile_lbl_1.grid(row=2, column=2,sticky="ew", padx=10,pady=10)

    mobile_entry_1 = ctk.CTkEntry(adding_teacher, placeholder_text="Enter Contact No.", font=(font_family_entry, font_size_entry, "bold"))
    mobile_entry_1.grid(row=2, column=3,sticky="ew", padx=10,pady=10)


    mobile_lbl_2 = ctk.CTkLabel(adding_teacher, text="\tSecondary No.", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    mobile_lbl_2.grid(row=3, column=0,sticky="ew", padx=10,pady=10)

    mobile_entry_2 = ctk.CTkEntry(adding_teacher, placeholder_text="Enter Contact No.", font=(font_family_entry, font_size_entry, "bold"))
    mobile_entry_2.grid(row=3, column=1,sticky="ew", padx=10,pady=10)

    email_lbl = ctk.CTkLabel(adding_teacher, text="\tE-Mail-ID", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    email_lbl.grid(row=3, column=2,sticky="ew", padx=10,pady=10)

    email_entry = ctk.CTkEntry(adding_teacher, placeholder_text="Enter Email-ID", font=(font_family_entry, font_size_entry, "bold"))
    email_entry.grid(row=3, column=3,sticky="ew", padx=10,pady=10)

    address_lbl = ctk.CTkLabel(adding_teacher, text="\tAddress", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    address_lbl.grid(row=4, column=0,sticky="ew", padx=10,pady=10)

    address_entry = ctk.CTkEntry(adding_teacher, placeholder_text="Enter Full Address", font=(font_family_entry, font_size_entry, "bold"))
    address_entry.grid(row=4, column=1,columnspan=3, sticky="ew", padx=10,pady=10)

    qualification_lbl = ctk.CTkLabel(adding_teacher, text="\tQualifications",font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    qualification_lbl.grid(row=5, column=0,sticky="ew", padx=10,pady=10)

    qualification_entry = ctk.CTkEntry(adding_teacher, placeholder_text="Enter Qualification", font=(font_family_entry, font_size_entry, "bold"))
    qualification_entry.grid(row=5, column=1, sticky="ew", padx=10,pady=10)

    dob_lbl = ctk.CTkLabel(adding_teacher, text="\tDate of Birth", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    dob_lbl.grid(row=5, column=2,sticky="ew", padx=10,pady=10)

    dob_entry = ctk.CTkEntry(adding_teacher, placeholder_text= "YYYY-MM-DD", font=(font_family_entry, font_size_entry, "bold"))
    dob_entry.grid(row=5, column=3,sticky="ew", padx=10,pady=10)
    
    desc_lbl = ctk.CTkLabel(adding_teacher, text="\tDescription", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    desc_lbl.grid(row=6, column=0,sticky="ew", padx=10,pady=10)

    desc_entry = ctk.CTkEntry(adding_teacher, placeholder_text="Enter Description (optional)", font=(font_family_entry, font_size_entry, "bold"))
    desc_entry.grid(row=6, column=1,sticky="ew", padx=10,pady=10)

    joining_lbl = ctk.CTkLabel(adding_teacher, text="\tJoining Date", font=(font_family_lbl, font_size_lbl, "bold"), anchor="w")
    joining_lbl.grid(row=6, column=2,sticky="ew", padx=10,pady=10)

    joining_entry = ctk.CTkEntry(adding_teacher, placeholder_text="YYYY-MM-DD", font=(font_family_entry, font_size_entry, "bold"))
    joining_entry.grid(row=6, column=3,sticky="ew", padx=10,pady=10)

    def validate_teachers_detail():
        errors = []
        if not fname_entry.get().isalpha():
            errors.append("First name should contain only alphabets.")

        if not mname_entry.get().isalpha():
            errors.append("Middle name should contain only alphabets.")

        if not lname_entry.get().isalpha():
            errors.append("Last name should contain only alphabets.")

        if not re.match(r"^\d{12}$", uid_entry.get()):
            errors.append("UID must be exactly 12 digits.")
        
        if not re.match(r"^\d{10}$", mobile_entry_1.get()):
            errors.append("Primary number must be exactly 10 digits.")
        
        if not re.match(r"^\d{10}$", mobile_entry_2.get()):
            errors.append("Secondary number must be exactly 10 digits.")

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email_entry.get()):
            errors.append("Invalid email format.")

        if not address_entry.get().strip():
            errors.append("Address cannot be empty.")

        if not qualification_entry.get().strip():
            errors.append("Qualification cannot be empty.")
        
        if select_gender.get() == "--Select--":
            errors.append("Gender not selected")

        
        # Get the date from the entry widget
        dob_str = dob_entry.get().strip()
        join_str = joining_entry.get().strip()

        # Check if the date is empty
        if len(dob_str) == 0:
            errors.append("Date of Birth cannot be empty")

        if len(join_str) == 0:
            errors.append("Joining Date cannot be empty")

        if not all(c.isdigit() or c == '-' for c in dob_str):
            errors.append("Date of Birth must contain only numbers and hyphens.")

        if not all(c.isdigit() or c == '-' for c in join_str):
            errors.append("joining of Birth must contain only numbers and hyphens.")

        # Check if the date is in the correct format (yyyy-mm-dd)
        if len(dob_str) != 10 or dob_str[4] != '-' or dob_str[7] != '-':
            errors.append("Invalid Date of Birth Format")

        if len(join_str) != 10 or join_str[4] != '-' or join_str[7] != '-':
            errors.append("Invalid Date of Joining Format")

        # Validate the date
        try:
            dob = datetime.strptime(dob_str, "%Y-%m-%d")  # Parse the date
            current_date = datetime.now().date()  # Get the current date

            # Check if the date is the current date
            if dob.date() == current_date:
                errors.append("Date of Birth cannot be the current date")
        except ValueError:
            errors.append("Invalid Date of Birth")


        try:
            datetime.strptime(join_str, "%Y-%m-%d")  # Parse the date
        except ValueError:
            errors.append("Invalid joining Date")


        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return False  # Stop execution if there are validation errors

        return True  # Proceed if all validations pass



    def insert_teachers():
        #messagebox.showinfo("Success", "Teacher info updated successfully!")
        # print(fname_entry.get(),mname_entry.get(),lname_entry.get(),uid_entry.get(),select_gender.get(),mobile_entry_1.get(),mobile_entry_2.get(),email_entry.get(),address_entry.get(),qualification_entry.get(),dob_entry.get(),desc_entry.get(),joining_entry.get())
        # return
        if not validate_teachers_detail():
            return
        #MySql query
        try: 
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO teachers_detail (first_name,middle_name,last_name,uid_no,gender,primary_no,secondary_no,email_id,address,qualification,dob,t_description,joining_date, total_paid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (fname_entry.get(),mname_entry.get(),lname_entry.get(),uid_entry.get(),select_gender.get(),mobile_entry_1.get(),mobile_entry_2.get(),email_entry.get(),address_entry.get(),qualification_entry.get(),dob_entry.get(),desc_entry.get(),joining_entry.get(),0)
            cursor.execute(query,values)
            conn.commit()    
            conn.close()
            messagebox.showinfo("Success", "Teacher info updated successfully!")
            clear_entries_t()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data: {err}")


    def clear_entries_t():
        fname_entry.delete(0, ctk.END)
        mname_entry.delete(0, ctk.END)
        lname_entry.delete(0, ctk.END)
        uid_entry.delete(0, ctk.END)
        select_gender.set("--Select--")
        mobile_entry_1.delete(0, ctk.END)
        mobile_entry_2.delete(0, ctk.END)
        email_entry.delete(0, ctk.END)
        address_entry.delete(0, ctk.END)
        qualification_entry.delete(0, ctk.END)
        dob_entry.delete(0, ctk.END)
        desc_entry.delete(0, ctk.END)
        joining_entry.delete(0, ctk.END)

        fname_entry._activate_placeholder()
        mname_entry._activate_placeholder()
        lname_entry._activate_placeholder()
        uid_entry._activate_placeholder()
        mobile_entry_1._activate_placeholder()
        mobile_entry_2._activate_placeholder()
        email_entry._activate_placeholder()
        address_entry._activate_placeholder()
        qualification_entry._activate_placeholder()
        dob_entry._activate_placeholder()
        desc_entry._activate_placeholder()
        joining_entry._activate_placeholder()

        adding_teacher.focus_set()

        
        


    add_btn = ctk.CTkButton(adding_teacher,text="Add Teacher",font=("Gudea", 15, "bold"), command=lambda:insert_teachers())
    add_btn.grid(row=7, column=0,columnspan=2,sticky="ew", padx=10,pady=50)

    clear_btn = ctk.CTkButton(adding_teacher,text="Clear",font=("Gudea", 15, "bold"),command=lambda:clear_entries_t())
    clear_btn.grid(row=7, column=2,columnspan=2,sticky="ew", padx=10,pady=50)



    # Editing Updating section


    # Editing / Upating Teacher
    def get_teacher_name():
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT teacher_id, first_name, middle_name, last_name FROM teachers_detail"
            cursor.execute(query)
            teacher_names = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
            conn.close()
            return teacher_names
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            return []

    def update_input_field(*args):
        selected_teacher = teacher_dropdown_u.get()
        selected_option = select_option_u.get()
        
        if selected_teacher != "--Select--" and selected_option != "--Select--":
            input_for_update.delete(0, ctk.END)
            input_for_update.grid(row=2, column=1, sticky="ew", padx=10, pady=10)
        else:
            input_for_update.grid_forget()

    def clear_info_u():
        select_option_u.set("--Select--")
        teacher_dropdown_u.set("--Select--")
        input_for_update.delete(0, ctk.END)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "SELECT teacher_id, first_name, middle_name, last_name FROM teachers_detail"
            cursor.execute(query)
            teacher_names = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
            conn.close()
            
            teacher_dropdown_u.configure(values = teacher_names)

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
            return False

        input_for_update.grid_forget()

    def update_teacher_info():
        selected_teacher = teacher_dropdown_u.get()
        selected_option = select_option_u.get()
        new_value = input_for_update.get().strip()

        if selected_teacher == "--Select--":
            messagebox.showerror("Error", "Please select a teacher.")
            return
        
        if selected_option == "--Select--":
            messagebox.showerror("Error", "Please select an attribute to update.")
            return
        
        if not new_value:
            messagebox.showerror("Error", "Input cannot be empty.")
            return

        teacher_id = selected_teacher.split(" - ")[0]  # Extract teacher ID

        option_to_column = {
            "Primary Contact No.": "primary_no",
            "Secondary Contact No.": "secondary_no",
            "Email-ID": "email_id",
            "Address": "address",
            "Description": "s_description",
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

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Check if the value already exists
            query = f"SELECT {column_name} FROM teachers_detail WHERE {column_name} = %s AND teacher_id != %s"
            cursor.execute(query, (new_value, teacher_id))
            if cursor.fetchone():
                messagebox.showerror("Error", f"The {selected_option} already exists for another teacher.")
                return
            

            #print(column_name,new_value,teacher_id)
            # Update the value
            query = f"UPDATE teachers_detail SET {column_name} = %s WHERE teacher_id = %s"
            cursor.execute(query, (new_value, teacher_id))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Teacher info updated successfully!")
            clear_info_u()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating data: {err}")


    for row in range(4):
        editing_teacher.grid_rowconfigure(row, weight=0)
    for col in range(3):
        editing_teacher.grid_columnconfigure(col, weight=1)

    # Select Teacher
    ctk.CTkLabel(editing_teacher, text="\t\tSelect Teacher", font=("Gudea", 16, "bold"),anchor="w").grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    teachers_name_u = get_teacher_name()

    teacher_dropdown_u = ctk.CTkComboBox(editing_teacher, values=teachers_name_u, state="readonly", font=("Gudea", 12, "bold"))
    teacher_dropdown_u.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
    teacher_dropdown_u.set("--Select--")

    # Select Attribute to Update
    ctk.CTkLabel(editing_teacher, text="\t\tSelect to update", font=("Gudea", 16, "bold"),anchor="w").grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    #select_option_var_u = ctk.StringVar()
    select_option_u = ctk.CTkComboBox(editing_teacher, values=["Primary Contact No.", "Secondary Contact No.", "Email-ID", "Address", "Description"], state="readonly", font=("Gudea", 12, "bold"))
    select_option_u.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
    select_option_u.set("--Select--")

    select_option_u.configure(command=update_input_field)

    input_for_update = ctk.CTkEntry(editing_teacher, font=("Gudea", 12, "bold"))

    update_btn = ctk.CTkButton(editing_teacher, text="UPDATE", font=("Gudea", 15, "bold"), command=update_teacher_info)
    update_btn.grid(row=3, column=0, sticky="ew", padx=10, pady=50)

    clear_btn = ctk.CTkButton(editing_teacher, text="CLEAR / REFRESH", font=("Gudea", 15, "bold"), command=clear_info_u)
    clear_btn.grid(row=3, column=1, sticky="ew", padx=10, pady=50)



    # deleting Teacher

    def delete_teacher():

        msg = CTkMessagebox(
            title="Deleting Teacher", 
            message="It is not Recommended to delete teacher if minimum 1 payment is done \n\nYou can't undo it \n\nDo you really want to Delete Teacher",
            icon="warning",  # "info", "warning", "error"
            option_1="Cancel",
            option_2="Yes"
        )
        
        # Get user's choice
        response = msg.get()
        
        if response != "Yes":
            return False
        
        selected_teacher = teacher_dropdown.get().strip()
        
        if selected_teacher == "--Select Teacher--":
            messagebox.showerror("Error", "Please select a teacher.")
            return
        
        teacher_id = selected_teacher.split(" - ")[0]  # Extract teacher ID
        
        # Show password dialog
        password = simpledialog.askstring("Password", "Enter admin password:", show='*')
        
        if password is None:  # If user cancels
            teacher_dropdown.set("--Select Teacher--")
            return
        
        if password != PASSWORD[0]:  # Replace with actual admin password
            messagebox.showerror("Error", "Incorrect password! Deletion not allowed.")
            return
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "DELETE FROM teachers_detail WHERE teacher_id = %s"
            cursor.execute(query, (teacher_id,))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Teacher record deleted successfully!")
            refresh_teacher_list()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting data: {err}")

    def refresh_teacher_list():
        teachers_name = get_teacher_name()
        teachers_name.insert(0, "--Select Teacher--")
        teacher_dropdown.configure(values=teachers_name)
        teacher_dropdown.set("--Select Teacher--")

    for i in range(1):
        deleting_teacher.grid_rowconfigure(i,weight=0)
    for j in range(2):
        deleting_teacher.grid_columnconfigure(j,weight=1)


    # Dropdown: Select Teacher
    teachers_name = get_teacher_name()
    teachers_name.insert(0, "--Select Teacher--")

    #select_teacher_name = ctk.StringVar()
    teacher_dropdown = ctk.CTkComboBox(deleting_teacher, values=teachers_name, state="readonly", font=(font_family_entry,font_size_entry,"bold"))
    teacher_dropdown.grid(row=0,column=0,sticky="ew",padx=15,pady=15)
    teacher_dropdown.set("--Select Teacher--")

    # Delete Button
    delete_btn = ctk.CTkButton(deleting_teacher, text="Delete Teacher", hover_color="red", text_color="white", command=delete_teacher, font=(font_family_lbl,font_size_entry,"bold"))
    delete_btn.grid(row=0, column=1, sticky="ew", columnspan=2,padx=15,pady=15)

    # Display Teacher

    # def get_teacher_name_to_display():
    #     try:
    #         conn = get_db_connection()
    #         cursor = conn.cursor()
    #         query = "SELECT teacher_id, first_name, middle_name, last_name FROM teachers_detail"
    #         cursor.execute(query)
    #         student_names_to_display = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
    #         conn.close()
    #         return student_names_to_display
    #     except mysql.connector.Error as err:
    #         messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
    #         return []

    def view_teacher(t_id):

        # Create new window
        view_teacher_detail = ctk.CTkToplevel()  # Use CTkToplevel instead of CTk for child windows
        view_teacher_detail.geometry("800x600")
        view_teacher_detail.title(f"Student Details - {t_id}")
        
        # This prevents the DPI scaling errors
        view_teacher_detail.after(100, lambda: view_teacher_detail.focus_force())
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier access
            
            # Fetch teacher data
            query = """SELECT teacher_id, first_name, middle_name, last_name, 
                    uid_no, gender, primary_no, secondary_no, email_id, 
                    address, qualification, dob, t_description, 
                    joining_date, total_paid 
                    FROM teachers_detail WHERE teacher_id = %s"""
            cursor.execute(query, (t_id,))
            teacher = cursor.fetchone()
            
            if not teacher:
                ctk.CTkLabel(view_teacher_detail, text="Teacher not found").pack()
                return
                
            # Create display frame
            scroll_frame = ctk.CTkScrollableFrame(view_teacher_detail)
            scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

            info_frame = ctk.CTkFrame(scroll_frame)
            info_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # Display teacher info in a grid
            labels = [
                ("Teacher ID", teacher['teacher_id']),
                ("Name", f"{teacher['first_name']} {teacher['middle_name']} {teacher['last_name']}"),
                ("UID No", teacher['uid_no']),
                ("Gender", teacher['gender']),
                ("Primary Phone", teacher['primary_no']),
                ("Secondary Phone", teacher['secondary_no']),
                ("Email", teacher['email_id']),
                ("Address", teacher['address']),
                ("Qualification", teacher['qualification']),
                ("Date of Birth", teacher['dob']),
                ("Description", teacher['t_description']),
                ("Joining Date", teacher['joining_date']),
                ("Total Paid", teacher['total_paid'])
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
            view_teacher_detail.destroy()
            
        view_teacher_detail.protocol("WM_DELETE_WINDOW", on_close)


    def setup_teacher_display():
        # Initialize the items list
        teachers = []
        
        # Function to fetch data from database
        def fetch_teacher_data():
            nonlocal teachers
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                query = "SELECT teacher_id, first_name, middle_name, last_name FROM teachers_detail"
                cursor.execute(query)
                teachers = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
                conn.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                teachers = []
        
        # Function to refresh the display
        def refresh_display():
            nonlocal teachers
            # Destroy existing widgets
            for widget in display_teacher.winfo_children():
                widget.destroy()
            
            # Fetch fresh data
            fetch_teacher_data()
            
            # Rebuild the display
            for i in range(len(teachers)+1):
                display_teacher.grid_rowconfigure(i, weight=0)
            for j in range(4):
                display_teacher.grid_columnconfigure(j, weight=1)
            
            # Header row
            ctk.CTkLabel(display_teacher, text="Serial No.").grid(row=0, column=0)
            ctk.CTkLabel(display_teacher, text="Teacher ID").grid(row=0, column=1)
            ctk.CTkLabel(display_teacher, text="Teacher Name").grid(row=0, column=2)
            ctk.CTkLabel(display_teacher, text="Action").grid(row=0, column=3)
            
            # Data rows
            for i, teacher in enumerate(teachers, start=1):
                teacher_id, teacher_name = teacher.split(" - ")
                ctk.CTkLabel(display_teacher, text=str(i)).grid(row=i, column=0)
                ctk.CTkLabel(display_teacher, text=teacher_id).grid(row=i, column=1)
                ctk.CTkLabel(display_teacher, text=teacher_name).grid(row=i, column=2)
                ctk.CTkButton(
                    display_teacher,
                    text="View",
                    command=lambda tid=teacher_id: view_teacher(tid)
                ).grid(row=i, column=3, pady=5)
        
        # Create scrollable frame (only once)
        scrollable_frame_teacher = ctk.CTkScrollableFrame(showing_teacher)
        scrollable_frame_teacher.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # Create display frame (only once)
        display_teacher = ctk.CTkFrame(scrollable_frame_teacher)
        display_teacher.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10, expand=True)
        
        # Add refresh button
        refresh_btn = ctk.CTkButton(
            showing_teacher,
            text="Refresh",
            command=refresh_display
        )
        refresh_btn.pack(side=ctk.TOP, pady=10)
        
        # Initial data load
        refresh_display()

    # Call the setup function
    setup_teacher_display()
    

    return teacher_screen