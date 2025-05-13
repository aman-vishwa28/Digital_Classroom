import customtkinter as ctk
from tkinter import messagebox
import mysql.connector
from db_connection import get_db_connection
from datetime import datetime,date


def fees_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen):
    dashboard_screen.pack_forget()
    student_screen.pack_forget()
    payment_screen.pack_forget()
    teacher_screen.pack_forget()
    attendance_screen.pack_forget()
    exam_screen.pack_forget()
    profile_screen.pack_forget()
    expense_screen.pack_forget()
    fees_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

def create_fees_screen(root, screen_width, menu_bar_color):
    fees_screen = ctk.CTkFrame(root)
    fees_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    fees_screen.configure(width=screen_width - 50)

    #Fees title strip
    fees_title_bar = ctk.CTkFrame(fees_screen, fg_color = menu_bar_color, corner_radius=0, border_width=0)
    fees_title_bar.pack(side = ctk.TOP, fill=ctk.X, pady=0)
    fees_title_bar.configure(height=100)

    #Fees Panel Title
    fees_title = ctk.CTkLabel(fees_title_bar,text="Fees Section",fg_color=menu_bar_color,text_color="white", font=("Gudea", 20,"bold"))
    fees_title.pack(expand=True,anchor="center", pady=15)


    button_frame = ctk.CTkFrame(fees_screen, corner_radius=0)
    button_frame.pack(side= ctk.TOP,fill=ctk.X, padx=0,pady=0)
    button_frame.configure(width=200)

    def change_add_fees():
        transaction_frame.pack_forget()
        fees_frame.pack(side=ctk.TOP,fill=ctk.BOTH,pady=0,expand=True,anchor="n")

    def change_fees_history():
        fees_frame.pack_forget()
        transaction_frame.pack(side=ctk.TOP,fill=ctk.BOTH,pady=0,expand=True,anchor="n")

    for i in range(2):
        button_frame.grid_columnconfigure(i,weight=1)

    #add update delete show 

    add_fees = ctk.CTkButton(button_frame,text="Add Fees",font=("Gudea",15,"bold"), corner_radius=0, command=lambda:change_add_fees())
    add_fees.grid(row=0,column=0,sticky="ew",padx=0,pady=0)

    view_history = ctk.CTkButton(button_frame,text="View Transaction History",font=("Gudea",15,"bold"), corner_radius=0,command=lambda:change_fees_history())
    view_history.grid(row=0,column=1,sticky="ew",padx=0,pady=0)

    fees_frame = ctk.CTkFrame(fees_screen,corner_radius=0)
    fees_frame.pack(side=ctk.LEFT,fill=ctk.BOTH,pady=0,expand=True,anchor="n")

    transaction_frame = ctk.CTkFrame(fees_screen,corner_radius=0)
    transaction_frame.pack(side=ctk.LEFT,fill=ctk.BOTH,pady=0,expand=True,anchor="n")

    for i in range(4):
        fees_frame.grid_columnconfigure(i,weight=1)
    for j in range(5):
        fees_frame.grid_columnconfigure(i,weight=1)


        
    def clear_fees():
        # clear Payment screen
        fees_std_entry.set("--Select--")
        fees_name_entry.set("--Select--")
        fees_amt_entry.delete(0, ctk.END)
        fees_date_entry.delete(0, ctk.END)

        fees_day_entry.configure(state = "normal")
        fees_day_entry.delete(0, ctk.END)
        fees_day_entry._activate_placeholder()
        fees_day_entry.configure(state = "disabled")

        fees_received_via.set("--Select--")
        fees_type.set("--Select--")
        fees_year_entry.set("--Select--")
        

        # placeholder
        fees_amt_entry._activate_placeholder()
        fees_date_entry._activate_placeholder()

        fees_screen.focus_set()

    def fees_validation():

        errors = []
        date_str = fees_date_entry.get().strip()
        
        try:
            # Try to parse the date in the format yyyy-mm-dd
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # If successful, calculate the day of the week
            day_of_week = date_obj.strftime("%A")  # Get the full name of the day (e.g., Monday)
            
            # Update the select_day_entry with the day of the week
            fees_day_entry.configure(state="normal")
            fees_day_entry.delete(0, ctk.END)
            fees_day_entry.insert(0, day_of_week)
            fees_day_entry.configure(state = "disabled")
        except ValueError:
            messagebox.showerror("Date Error",f"{fees_date_entry.get()} \nEnter the Valid date")
            fees_date_entry.delete(0, ctk.END)
            return

        if fees_std_entry.get() == "--Select--":
            errors

        if fees_name_entry.get() == "--Select--":
            errors.append("Teacher Name not Selected")

        if not fees_amt_entry.get().strip:
            errors.append("Amount cannot be Empty")

        if not all(c.isdigit() for c in fees_amt_entry.get()):
             errors.append("Amount must be in digit")

        if not fees_date_entry.get():
            errors.append("Date cannot be Empty")
        
        if fees_received_via.get() == "--Select--":
            errors.append("Fees Received via not Selected")        

        if fees_type.get() == "--Select--":
            errors.append("Type not Selected")

        if fees_type.get() == "Montly" and desc_month.get() == "--Select--":
            errors.append("Payment for Month not Selected")

        if fees_type.get() == "Installment" and desc_installment.get() == "--Select--":
            errors.append("Installment not Selected")

        if fees_year_entry.get() == "--Select--":
            errors.append("Batch Year not Selected")
            
        if errors:
            messagebox.showerror("Validation Error","\n".join(errors))
            return False
        
        try:
            student_id = fees_name_entry.get().split(" - ")[0]
            conn = get_db_connection()
            cursor = conn.cursor()

            query = "SELECT total_fees, total_paid, pending_fees FROM students_detail WHERE student_id = %s and academic_year = %s;"
            cursor.execute(query, (student_id, fees_year_entry.get()))

            # Get a single row (fetchone) since we're querying for one student
            row = cursor.fetchone()
            
            if not row:  # If no record found
                messagebox.showerror("Error", "Student record not found")
                return False
            
            total_fees, total_paid, pending_fees = row
            try:
                amount_entered = float(fees_amt_entry.get())
                pending_fees = float(pending_fees)
            except ValueError:
                messagebox.showerror("Error", "Invalid amount format")
                return False

            if (amount_entered > pending_fees):
                messagebox.showerror("Amount Error",f"Amount Entered is greater than Pending Fees \n\nTotal fees : {total_fees}\nTotal Paid : {total_paid}\nPending Fees : {pending_fees}")
                return False
            
            return True
        
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")

        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()
        
        return True
        
    def insert_fees():
        if not fees_validation():
            return
        
        messagebox.showinfo("Test","OK")
        student_id = fees_name_entry.get().split(" - ")[0]
        student_name_to_insert = fees_name_entry.get().split(" - ")[1]

        #print(student_id, student_name_to_insert, fees_std_entry.get(), fees_date_entry.get(), fees_day_entry.get(), fees_received_via.get(), fees_year_entry.get(), desc_month.get(), desc_installment.get(), fees_amt_entry.get(), date.today())
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "Insert into student_transaction_detail (student_id, student_name, class, payment_date, payment_day, via, batch_year, for_month, installment, amount, updated_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (student_id, student_name_to_insert, fees_std_entry.get(), fees_date_entry.get(), fees_day_entry.get(), fees_received_via.get(), fees_year_entry.get(), desc_month.get(), desc_installment.get(), fees_amt_entry.get(), date.today())
            cursor.execute(query,values)

            query = "UPDATE students_detail SET total_paid = total_paid + %s WHERE student_id = %s and academic_year = %s"
            cursor.execute(query, (fees_amt_entry.get(), student_id, fees_year_entry.get()))
            conn.commit()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error inserting data: {err}")
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

        clear_fees()
        
    def on_focus_out(event):
        # Get the date string from the pay_date_entry
        date_str = fees_date_entry.get().strip()
        
        try:
            # Try to parse the date in the format yyyy-mm-dd
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # If successful, calculate the day of the week
            day_of_week = date_obj.strftime("%A")  # Get the full name of the day (e.g., Monday)
            
            # Update the select_day_entry with the day of the week
            fees_day_entry.configure(state="normal")
            fees_day_entry.delete(0, ctk.END)
            fees_day_entry.insert(0, day_of_week)
            fees_day_entry.configure(state = "disabled")
        except ValueError:
            messagebox.showerror("Date Error",f"{fees_date_entry.get()} \nEnter the Valid date")
            fees_date_entry.delete(0, ctk.END)

    def update_type(*args):
        if (fees_type.get() == "Montly"):
            desc_month.set("--Select--")
            desc_installment.set("--Select--")
            desc_installment.grid_forget()
            # pay_desc_entry.grid_forget()
            desc_month.grid(row=4,column=3, padx=10, pady=10, sticky="ew")

        if (fees_type.get() == "Installment"):
            desc_month.set("--Select--")
            desc_installment.set("--Select--")
            desc_month.grid_forget()
            # pay_desc_entry.grid_forget()
            desc_installment.grid(row=4,column=3, padx=10, pady=10, sticky="ew")

    def check_std(*args):
        if (fees_std_entry.get() != "--Select--"):
            fees_year_entry.set("--Select--")
            fees_year_entry.configure(state = "readonly")

            fees_name_entry.set("--Select--")
            fees_name_entry.configure(state = "disabled")

        else:
            fees_year_entry.set("--Select--")
            fees_year_entry.configure(state = "disabled")

            fees_name_entry.set("--Select--")
            fees_name_entry.configure(state = "disabled")

    def check_batch(*args):
        # global student_name
        if (fees_year_entry.get() != "--Select--"):
            # fees_name_entry.configure(state="readonly")

            std = fees_std_entry.get()
            year = fees_year_entry.get()
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                query = "SELECT student_id, first_name, middle_name, last_name FROM students_detail where class = %s and academic_year = %s"
                cursor.execute(query, (std, year))
                student_names = [f"{row[0]} - {row[1]} {row[2]} {row[3]}".strip() for row in cursor.fetchall()]
                fees_name_entry.configure(values = student_names, state = "readonly")
                conn.close()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
                return






    fees_std_lbl = ctk.CTkLabel(fees_frame,text="\tSelect Standard",font=("Gudea", 15,"bold"), anchor="w")
    fees_std_lbl.grid(row=0,column=0, padx=10,pady=10,sticky="ew")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT course_name FROM courses"
        cursor.execute(query)
        course_names = [f"{row[0]}".strip() for row in cursor.fetchall()]
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
        

    fees_std_entry = ctk.CTkComboBox(fees_frame, values=course_names, state="readonly",font=("Gudea", 12,"bold"))
    fees_std_entry.set("--Select--")
    fees_std_entry.grid(row=0,column=1, padx=10,pady=10,sticky="ew")
    fees_std_entry.configure(command = check_std)


    fees_year_lbl = ctk.CTkLabel(fees_frame, text="\tBatch Year", font=("Gudea", 15,"bold"), anchor="w")
    fees_year_lbl.grid(row=0,column=2, padx=10,pady=10,sticky="ew")


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

    fees_year_entry = ctk.CTkComboBox(fees_frame, values = batch_values, state="disabled", font=("Gudea",12,"bold"))
    fees_year_entry.grid(row=0,column=3,sticky="ew",padx=10,pady=10)
    fees_year_entry.set("--Select--")
    fees_year_entry.configure(command = check_batch)

    fees_name_lbl = ctk.CTkLabel(fees_frame,text="\tStudent Name",font=("Gudea", 15,"bold"), anchor="w")
    fees_name_lbl.grid(row=1,column=0, padx=10,pady=10,sticky="ew")

    fees_name_entry = ctk.CTkComboBox(fees_frame, values = [], state="readonly",font=("Gudea", 12,"bold"))
    fees_name_entry.set("--Select--")
    fees_name_entry.grid(row=1,column=1, padx=10,pady=10,sticky="ew")

    fees_amt_lbl = ctk.CTkLabel(fees_frame,text="\tFees Amount",font=("Gudea", 15,"bold"), anchor="w")
    fees_amt_lbl.grid(row=1,column=2, padx=10,pady=10,sticky="ew")

    fees_amt_entry = ctk.CTkEntry(fees_frame,placeholder_text="Enter Amount", font=("Gudea", 15,"bold"))
    fees_amt_entry.grid(row=1,column=3, padx=10,pady=10,sticky="ew")

    fees_day_lbl = ctk.CTkLabel(fees_frame,text="\tDay",font=("Gudea", 15,"bold"), anchor="w")
    fees_day_lbl.grid(row=2,column=2, padx=10,pady=10,sticky="ew")

    fees_day_entry = ctk.CTkEntry(fees_frame, placeholder_text="Day of Date appear hear", font=("Gudea",12,"bold"))
    fees_day_entry.grid(row=2,column=3,sticky="ew",padx=10,pady=10)
    fees_day_entry.configure(state="disabled")

    fees_date_lbl = ctk.CTkLabel(fees_frame,text="\tDate",font=("Gudea", 15,"bold"), anchor="w")
    fees_date_lbl.grid(row=2,column=0, padx=10,pady=10,sticky="ew")

    fees_date_entry = ctk.CTkEntry(fees_frame, placeholder_text="YYYY-MM-DD", font=("Gudea", 12,"bold"))
    fees_date_entry.grid(row=2,column=1, padx=10,pady=10,sticky="ew")
    # fees_date_entry.bind("<FocusOut>", on_focus_out)

    fees_via_lbl = ctk.CTkLabel(fees_frame,text="\tReceived via",font=("Gudea", 15,"bold"), anchor="w")
    fees_via_lbl.grid(row=3,column=0, padx=10,pady=10,sticky="ew")

    fees_received_via = ctk.CTkComboBox(fees_frame, values=["Cash","Online","Cheque"], state="readonly", font=("Gudea",12,"bold"))
    fees_received_via.grid(row=3,column=1,sticky="ew",padx=10,pady=10)
    fees_received_via.set("--Select--")

    fees_type_lbl = ctk.CTkLabel(fees_frame,text="\tType",font=("Gudea", 15,"bold"), anchor="w")
    fees_type_lbl.grid(row=3,column=2, padx=10,pady=10,sticky="ew")

    fees_type = ctk.CTkComboBox(fees_frame, values=["Montly", "Installment"], state="readonly", font=("Gudea",12,"bold"))
    fees_type.grid(row=3,column=3,sticky="ew",padx=10,pady=10)
    fees_type.set("--Select--")
    fees_type.configure(command = update_type)

    

    specify_type = ctk.CTkLabel(fees_frame,text="\tSpecify the Type",font=("Gudea", 15,"bold"), anchor="w")
    specify_type.grid(row=4,column=2, padx=10,pady=10,sticky="ew")

    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    desc_month = ctk.CTkComboBox(fees_frame, values = month_list)
    desc_month.set("--Select")

    installment_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    installment_list = [str(item) for item in installment_list]
    desc_installment = ctk.CTkComboBox(fees_frame,values=installment_list)
    desc_installment.set("--Select--")

    fees_insert_btn = ctk.CTkButton(fees_frame,text="Insert", font=("Gudea", 15,"bold"),command=insert_fees)
    fees_insert_btn.grid(row=5,column=0,columnspan=2 ,padx=10,pady=10,sticky="ew")

    fees_clear_btn = ctk.CTkButton(fees_frame,text="Clear", font=("Gudea", 15,"bold"),command=clear_fees)
    fees_clear_btn.grid(row=5,column=2,columnspan=2, padx=10,pady=10,sticky="ew")



    #-------------------------------------------------

    def view_fees(s_id):

        # Create new window
        view_fees_detail = ctk.CTkToplevel()  # Use CTkToplevel instead of CTk for child windows
        view_fees_detail.geometry("800x600")
        view_fees_detail.title(f"Fees Details - {s_id}")
        
        # This prevents the DPI scaling errors
        view_fees_detail.after(100, lambda: view_fees_detail.focus_force())
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier access
            
            # Fetch student data
            query = """SELECT transaction_id, student_id, student_name, class, payment_date, payment_day, via, batch_year, for_month, installment, amount, updated_date 
                    FROM student_transaction_detail WHERE transaction_id = %s"""
            cursor.execute(query, (s_id,))
            fees = cursor.fetchone()
            
            if not fees:
                ctk.CTkLabel(view_fees_detail, text="Fees Transaction not found").pack()
                return
                
            # Create display frame

            scroll_frame = ctk.CTkScrollableFrame(view_fees_detail)
            scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

            info_frame = ctk.CTkFrame(scroll_frame)
            info_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # Display student info in a grid
            labels = [
                ("Transaction ID", fees['transaction_id']),
                ("Student ID", fees['student_id']),
                ("Student Name", fees['student_name']),
                ("Class", fees['class']),
                ("Payment Date", fees['payment_date']),
                ("Payment Day", fees['payment_day']),
                ("Paid Via", fees['via']),
                ("Batch Year", fees['batch_year']),
                ("Paid For Month", fees['for_month']),
                ("Installment", fees['installment']),
                ("Amount", fees['amount']),
                ("Updated Date", fees['updated_date'])
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
            view_fees_detail.destroy()
            
        view_fees_detail.protocol("WM_DELETE_WINDOW", on_close)
    
    
    
   
    def setup_transaction_display():
        # Initialize the items list
        items = []
        
        # Function to fetch data from database
        def fetch_fees_data():
            nonlocal items            
            search_input = search_by.get()
            search_val = input_field.get()
            combo_box = select_from_combobox.get()

            if (search_input == "All"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT transaction_id, student_id, student_name, payment_date, amount FROM student_transaction_detail"
                    cursor.execute(query)
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

            elif (search_input == "Transaction ID"):
                if not input_field.get() or not input_field.get().isdigit():
                    messagebox.showerror("Validation Error", "Input cannot be empty and digits are allowed")
                    return False
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT transaction_id, student_id, student_name, payment_date, amount FROM student_transaction_detail Where transaction_id = %s"
                    cursor.execute(query,(search_val,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}".strip() for row in cursor.fetchall()]
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
                    query = "SELECT transaction_id, student_id, student_name, payment_date, amount FROM student_transaction_detail Where student_id = %s"
                    cursor.execute(query,(search_val,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

            # elif (search_input == "Student Name"):
                
            #     try:
            #         conn = get_db_connection()
            #         cursor = conn.cursor()
            #         query = "SELECT transaction_id, student_id, student_name, payment_date, amount FROM student_transaction_detail WHERE student_name = %s"
            #         cursor.execute(query,(combo_box,))
            #         items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}".strip() for row in cursor.fetchall()]
            #         conn.close()
            #     except mysql.connector.Error as err:
            #         messagebox.showerror("Database Error", f"Error retrieving data: {err}")
            #         items = []

            elif (search_input == "Class"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT transaction_id, student_id, student_name, payment_date, amount FROM student_transaction_detail WHERE class = %s"
                    cursor.execute(query,(combo_box,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []
            

            elif (search_input == "Batch Year"):
                
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT transaction_id, student_id, student_name, payment_date, amount FROM student_transaction_detail Where batch_year = %s"
                    cursor.execute(query,(combo_box,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

        
        # Function to refresh the display
        def refresh_display():
            nonlocal items
            # Destroy existing widgets
            for widget in display_fees.winfo_children():
                widget.destroy()
            
            # Fetch fresh data
            fetch_fees_data()
            
            # Rebuild the display
            for i in range(len(items)+1):
                display_fees.grid_rowconfigure(i, weight=0)
            for j in range(6):
                display_fees.grid_columnconfigure(j, weight=1)
            
            # Header row
            ctk.CTkLabel(display_fees, text="Transaction ID").grid(row=0, column=0)
            ctk.CTkLabel(display_fees, text="Student ID").grid(row=0, column=1)
            ctk.CTkLabel(display_fees, text="Student Name").grid(row=0, column=2)
            # ctk.CTkLabel(display_fees, text="Class").grid(row=0, column=3)
            ctk.CTkLabel(display_fees, text="Payment Date").grid(row=0, column=3)
            ctk.CTkLabel(display_fees, text="Payment Amount").grid(row=0, column=4)
            ctk.CTkLabel(display_fees, text="Action").grid(row=0, column=5)
            
            # Data rows
            for i, item in enumerate(items, start=1):
                transaction_id, student_id, student_name, date, amt = item.split(",")
                ctk.CTkLabel(display_fees, text=transaction_id).grid(row=i, column=0)
                ctk.CTkLabel(display_fees, text=student_id).grid(row=i, column=1)
                ctk.CTkLabel(display_fees, text=student_name).grid(row=i, column=2)
                ctk.CTkLabel(display_fees, text=date).grid(row=i, column=3)
                ctk.CTkLabel(display_fees, text=amt).grid(row=i, column=4)
                ctk.CTkButton(
                    display_fees,
                    text="View",
                    command=lambda sid=transaction_id: view_fees(sid)
                ).grid(row=i, column=5, pady=5)

        

        set_search_frame = ctk.CTkFrame(transaction_frame)
        set_search_frame.pack(side = ctk.TOP, fill = ctk.X, padx = 10, pady = 10, anchor = "n")

        for i in range(7):
            set_search_frame.grid_columnconfigure(i, weight = 1)
        

        def check_search(*args):
            if search_by.get() == "All":
                input_field.delete(0, ctk.END)
                input_lbl.grid_forget()
                input_field.grid_forget()
                select_from_combobox.set("--Select--")
                select_from_combobox.grid_forget()

            elif (search_by.get() == "Transaction ID"):
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

            # elif (search_by.get() == "Student Name"):
            #     input_lbl.configure(text = f"Select {search_by.get()}")
            #     input_field.grid_forget()

            #     try:
            #         conn = get_db_connection()
            #         cursor = conn.cursor()
            #         query = "SELECT first_name, middle_name, last_name FROM students_detail"
            #         cursor.execute(query)
            #         search_student = [f"{row[0]} {row[1]} {row[2]}".strip() for row in cursor.fetchall()]
            #         conn.close()
            #     except mysql.connector.Error as err:
            #         messagebox.showerror("Database Error", f"Error retrieving data: {err}")
            #         search_student = []

            #     select_from_combobox.configure(values = search_student)
            #     select_from_combobox.set("-Select--")
            #     select_from_combobox.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)

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


        ctk.CTkLabel(set_search_frame, text = "Search By").grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)

        search_by = ctk.CTkComboBox(set_search_frame, values = ["All", "Transaction ID", "Student ID", "Class", "Batch Year"])
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
        scrollable_frame_fees = ctk.CTkScrollableFrame(transaction_frame)
        scrollable_frame_fees.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # Create display frame (only once)
        display_fees = ctk.CTkFrame(scrollable_frame_fees)
        display_fees.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10, expand=True)
        
        # Add refresh button
        refresh_btn = ctk.CTkButton(
            transaction_frame,
            text="Refresh",
            command=refresh_display
        )
        refresh_btn.pack(side=ctk.TOP, pady=10)
        
        # Initial data load
        refresh_display()

    # Call the setup function
    setup_transaction_display()
    transaction_frame.pack_forget()

    return fees_screen