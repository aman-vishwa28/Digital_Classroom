import customtkinter as ctk
from tkinter import messagebox
from db_connection import get_db_connection
import mysql.connector
import re
from datetime import datetime, date

def payment_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen):
    dashboard_screen.pack_forget()
    student_screen.pack_forget()
    teacher_screen.pack_forget()
    fees_screen.pack_forget()
    attendance_screen.pack_forget()
    exam_screen.pack_forget()
    profile_screen.pack_forget()
    expense_screen.pack_forget()
    payment_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)


def create_payment_screen(root, screen_width, menu_bar_color):
    payment_screen = ctk.CTkFrame(root,fg_color="white")
    payment_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    payment_screen.configure(width=screen_width - 50)

    #Payment title strip
    payment_title_bar = ctk.CTkFrame(payment_screen, fg_color = menu_bar_color, corner_radius=0, border_width=0)
    payment_title_bar.pack(side = ctk.TOP, fill=ctk.X, pady=0)
    payment_title_bar.configure(height=100)

    #Payment Panel Title
    payment_title = ctk.CTkLabel(payment_title_bar,text="Payment Section",fg_color=menu_bar_color,text_color="white", font=("Gudea", 20,"bold"))
    payment_title.pack(expand=True,anchor="center", pady=15)

    button_frame = ctk.CTkFrame(payment_screen, corner_radius=0)
    button_frame.pack(side= ctk.TOP,fill=ctk.X, padx=0,pady=0)
    button_frame.configure(width=200)

    def change_add_payment():
        transaction_frame.pack_forget()
        pay_frame.pack(side=ctk.TOP,fill=ctk.BOTH,pady=0,expand=True,anchor="n")

    def change_payment_history():
        pay_frame.pack_forget()
        transaction_frame.pack(side=ctk.TOP,fill=ctk.BOTH,pady=0,expand=True,anchor="n")

    

    for i in range(2):
        button_frame.grid_columnconfigure(i,weight=1)

    #add update delete show 

    add_payment = ctk.CTkButton(button_frame,text="Add Payment",font=("Gudea",15,"bold"), corner_radius=0, command=lambda:change_add_payment())
    add_payment.grid(row=0,column=0,sticky="ew",padx=0,pady=0)

    view_history = ctk.CTkButton(button_frame,text="View Transaction History",font=("Gudea",15,"bold"), corner_radius=0,command=lambda:change_payment_history())
    view_history.grid(row=0,column=1,sticky="ew",padx=0,pady=0)

    pay_frame = ctk.CTkFrame(payment_screen,corner_radius=0)
    pay_frame.pack(side=ctk.LEFT,fill=ctk.BOTH,pady=0,expand=True,anchor="n")

    transaction_frame = ctk.CTkFrame(payment_screen,corner_radius=0)
    transaction_frame.pack(side=ctk.LEFT,fill=ctk.BOTH,pady=0,expand=True,anchor="n")

    for i in range(4):
        pay_frame.grid_columnconfigure(i,weight=1)
    for j in range(5):
        pay_frame.grid_rowconfigure(j,weight=0)

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
        
    teachers_name = get_teacher_name()
    def clear_payment():
        # clear Payment screen
        pay_name_entry.set("--Select--")
        pay_amt_entry.delete(0, ctk.END)
        pay_date_entry.delete(0, ctk.END)
        desc_month.set("--Select--")
        desc_installment.set("--Select--")
        desc_installment.grid_forget()
        desc_month.grid_forget()

        select_day_entry.configure(state = "normal")
        select_day_entry.delete(0, ctk.END)
        select_day_entry._activate_placeholder()
        select_day_entry.configure(state = "disable")

        pay_via.set("--Select--")
        pay_type.set("--Select--")
        pay_year.set("--Select--")
        # pay_desc_entry.delete(0, ctk.END)

        # placeholder
        pay_amt_entry._activate_placeholder()
        pay_date_entry._activate_placeholder()
        # pay_desc_entry._activate_placeholder()

        payment_screen.focus_set()

    def payment_validation():

        errors = []
        date_str = pay_date_entry.get().strip()
        
        try:
            # Try to parse the date in the format yyyy-mm-dd
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # If successful, calculate the day of the week
            day_of_week = date_obj.strftime("%A")  # Get the full name of the day (e.g., Monday)
            
            # Update the select_day_entry with the day of the week
            select_day_entry.configure(state="normal")
            select_day_entry.delete(0, ctk.END)
            select_day_entry.insert(0, day_of_week)
            select_day_entry.configure(state = "disable")
        except ValueError:
            messagebox.showerror("Date Error",f"{pay_date_entry.get()} \nEnter the Valid date")
            pay_date_entry.delete(0, ctk.END)
            return

        amount = int(pay_amt_entry.get())
        if pay_name_entry.get() == "--Select--":
            errors.append("Teacher Name not Selected")

        if not pay_amt_entry.get().strip:
            errors.append("Amount cannot be Empty")

        if not pay_amt_entry.get().isdigit():
            # errors.append("Amount must contain only digits (0-9)")
            messagebox.showerror("Validation Error","Amount must contain only digits (0-9)")
            return False

        if amount < 1:
            errors.append("minimum payment must be 1")

        if not pay_date_entry.get():
            errors.append("Date cannot be Empty")
        
        if pay_via.get() == "--Select--":
            errors.append("Paid Via not Selected")        

        if pay_type.get() == "--Select--":
            errors.append("Type not Selected")

        if pay_type.get() == "Montly" and desc_month.get() == "--Select--":
            errors.append("Payment for Month not Selected")

        if pay_type.get() == "Installment" and desc_installment.get() == "--Select--":
            errors.append("Installment not Selected")

        if pay_year.get() == "--Select--":
            errors.append("Batch Year not Selected")

        if errors:
            messagebox.showerror("Validation Error","\n".join(errors))
            return False
        
        return True

    def insert_payment():
        if not payment_validation():
            return
    
        teacher_id = pay_name_entry.get().split(" - ")[0]
        teacher_name = pay_name_entry.get().split(" - ")[1]
            
        if (desc_installment == "--Select--"):
            desc_installment.set("")

        if (desc_month == "--Select--"):
            desc_month.set("")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO teacher_transaction_detail (teacher_id, teacher_name, payment_date, payment_day, via, batch_year, for_month, installment, amount, updated_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (teacher_id, teacher_name, pay_date_entry.get(), select_day_entry.get(), pay_via.get(), pay_year.get(), desc_month.get(), desc_installment.get(), pay_amt_entry.get(), date.today())
            cursor.execute(query,values)
            
            query = "UPDATE teachers_detail SET total_paid = total_paid + %s where teacher_id = %s"
            cursor.execute(query, (pay_amt_entry.get(), teacher_id))

            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Teachers Payment info updated successfully!")
            clear_payment()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error Retrieving data: {err}")

        # messagebox.showinfo("Test","OK")
        # clear_payment()

    def on_focus_out(event):
        # Get the date string from the pay_date_entry
        date_str = pay_date_entry.get().strip()
        
        try:
            # Try to parse the date in the format yyyy-mm-dd
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            
            # If successful, calculate the day of the week
            day_of_week = date_obj.strftime("%A")  # Get the full name of the day (e.g., Monday)
            
            # Update the select_day_entry with the day of the week
            select_day_entry.configure(state="normal")
            select_day_entry.delete(0, ctk.END)
            select_day_entry.insert(0, day_of_week)
            select_day_entry.configure(state = "disable")
        except ValueError:
            messagebox.showerror("Date Error",f"{pay_date_entry.get()} \nEnter the Valid date")
            pay_date_entry.delete(0, ctk.END)

    def update_type(*args):
        if (pay_type.get() == "Montly"):
            desc_month.set("--Select--")
            desc_installment.set("--Select--")
            desc_installment.grid_forget()
            desc_month.grid(row=3,column=3, padx=10, pady=10, sticky="ew")

        if (pay_type.get() == "Installment"):
            desc_month.set("--Select--")
            desc_installment.set("--Select--")
            desc_month.grid_forget()
            desc_installment.grid(row=3,column=3, padx=10, pady=10, sticky="ew")


    pay_name_lbl = ctk.CTkLabel(pay_frame,text="\tTeacher Name",font=("Gudea", 15,"bold"), anchor="w")
    pay_name_lbl.grid(row=0,column=0, padx=10,pady=10,sticky="ew")

    pay_name_entry = ctk.CTkComboBox(pay_frame, values = teachers_name, state="readonly",font=("Gudea", 12,"bold"))
    pay_name_entry.grid(row=0,column=1, padx=10,pady=10,sticky="ew")
    pay_name_entry.set("--Select--")

    
    pay_amt_lbl = ctk.CTkLabel(pay_frame,text="\tAmount",font=("Gudea", 15,"bold"), anchor="w")
    pay_amt_lbl.grid(row=0,column=2, padx=10,pady=10,sticky="ew")

    pay_amt_entry = ctk.CTkEntry(pay_frame,placeholder_text="Enter Amount",font=("Gudea", 15,"bold"))
    pay_amt_entry.grid(row=0,column=3, padx=10,pady=5,sticky="ew")

    pay_date_lbl = ctk.CTkLabel(pay_frame,text="\tPay Date (yyyy-mm-dd)",font=("Gudea", 15,"bold"), anchor="w")
    pay_date_lbl.grid(row=1,column=0, padx=10,pady=10,sticky="ew")

    # def check(*args):
    #     if (len(entry_var.get()) >= 10):
    #         pay_frame.focus_set()

    # entry_var = ctk.StringVar()
    # entry_var.trace_add("write",check)

    pay_date_entry = ctk.CTkEntry(pay_frame, placeholder_text="YYYY-MM-DD", font=("Gudea", 12,"bold"))
    pay_date_entry.grid(row=1,column=1, padx=10,pady=10,sticky="ew")
    # pay_date_entry.
    pay_date_entry.bind("<FocusOut>", on_focus_out)
    

    pay_day_lbl = ctk.CTkLabel(pay_frame,text="\tDay",font=("Gudea", 15,"bold"), anchor="w")
    pay_day_lbl.grid(row=1,column=2, padx=10,pady=10,sticky="ew")

    select_day_entry = ctk.CTkEntry(pay_frame, placeholder_text="Day of Date appear hear")
    select_day_entry.grid(row=1,column=3,sticky="ew",padx=10,pady=10)
    select_day_entry.configure(state="disable")
    
    pay_via_lbl = ctk.CTkLabel(pay_frame,text="\tPaid via",font=("Gudea", 15,"bold"), anchor="w")
    pay_via_lbl.grid(row=2,column=0, padx=10,pady=10,sticky="ew")

    pay_via = ctk.CTkComboBox(pay_frame, values=["Cash","Online","Cheque"], state="readonly", font=("Gudea",12,"bold"))
    pay_via.grid(row=2,column=1,sticky="ew",padx=10,pady=10)
    pay_via.set("--Select--")

    pay_type_lbl = ctk.CTkLabel(pay_frame,text="\tType",font=("Gudea", 15,"bold"), anchor="w")
    pay_type_lbl.grid(row=2,column=2, padx=10,pady=10,sticky="ew")

    pay_type = ctk.CTkComboBox(pay_frame, values=["Montly", "Installment"], state="readonly", font=("Gudea",12,"bold"))
    pay_type.grid(row=2,column=3,sticky="ew",padx=10,pady=10)
    pay_type.set("--Select--")
    pay_type.configure(command = update_type)

    pay_year_lbl = ctk.CTkLabel(pay_frame,text="\tBatch Year", font=("Gudea", 15,"bold"), anchor="w")
    pay_year_lbl.grid(row=3,column=0, padx=10,pady=10,sticky="ew")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT batch_year FROM batch"
        cursor.execute(query)
        batch_values = [f"{row[0]}".strip() for row in cursor.fetchall()]
        conn.close()
        # return student_names_to_display
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
        batch_values = []

    pay_year = ctk.CTkComboBox(pay_frame, values=batch_values, state="readonly", font=("Gudea",12,"bold"))
    pay_year.grid(row=3,column=1,sticky="ew",padx=10,pady=10)
    pay_year.set("--Select--")

    pay_desc_lbl = ctk.CTkLabel(pay_frame,text="\tDescribe Type",font=("Gudea", 15,"bold"), anchor="w")
    pay_desc_lbl.grid(row=3,column=2, padx=10,pady=10,sticky="ew")

    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    desc_month = ctk.CTkComboBox(pay_frame, values = month_list)
    desc_month.set("--Select")

    installment_list = [1,2,3,4,5,6,7,8,9,10,11,12]
    installment_list = [str(item) for item in installment_list]
    desc_installment = ctk.CTkComboBox(pay_frame,values=installment_list)
    desc_installment.set("--Select--")

    pay_insert_btn = ctk.CTkButton(pay_frame,text="Submit", font=("Gudea", 15,"bold"),command=insert_payment)
    pay_insert_btn.grid(row=4,column=0,columnspan=2 ,padx=10,pady=10,sticky="ew")

    pay_clear_btn = ctk.CTkButton(pay_frame,text="Clear", font=("Gudea", 15,"bold"),command=clear_payment)
    pay_clear_btn.grid(row=4,column=2,columnspan=2, padx=5,pady=5,sticky="ew")

    
    def view_payment(t_id):

        # Create new window
        view_payment_detail = ctk.CTkToplevel()  # Use CTkToplevel instead of CTk for child windows
        view_payment_detail.geometry("800x600")
        view_payment_detail.title(f"Payment Details - {t_id}")
        
        # This prevents the DPI scaling errors
        view_payment_detail.after(100, lambda: view_payment_detail.focus_force())
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)  # Use dictionary cursor for easier access
            
            # Fetch teacher data
            query = """SELECT transaction_id, teacher_id, teacher_name, payment_date, payment_day, via, batch_year, for_month, installment, amount, updated_date 
                    FROM teacher_transaction_detail WHERE transaction_id = %s"""
            cursor.execute(query, (t_id,))
            payment = cursor.fetchone()
            
            if not payment:
                ctk.CTkLabel(view_payment_detail, text="Teachers Payment Transaction not found").pack()
                return
                
            # Create display frame

            scroll_frame = ctk.CTkScrollableFrame(view_payment_detail)
            scroll_frame.pack(pady=20, padx=20, fill="both", expand=True)

            info_frame = ctk.CTkFrame(scroll_frame)
            info_frame.pack(pady=20, padx=20, fill="both", expand=True)
            
            # Display teacher info in a grid
            labels = [
                ("Transaction ID", payment['transaction_id']),
                ("Teacher ID", payment['teacher_id']),
                ("Teacher Name", payment['teacher_name']),
                ("Payment Date", payment['payment_date']),
                ("Payment Day", payment['payment_day']),
                ("Paid Via", payment['via']),
                ("Batch Year", payment['batch_year']),
                ("Paid For Month", payment['for_month']),
                ("Installment", payment['installment']),
                ("Amount", payment['amount']),
                ("Updated Date", payment['updated_date'])
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
            view_payment_detail.destroy()
            
        view_payment_detail.protocol("WM_DELETE_WINDOW", on_close)
    
    
    
   
    def setup_transaction_display():
        # Initialize the items list
        items = []
        
        # Function to fetch data from database
        def fetch_payment_data():
            nonlocal items            
            search_input = search_by.get()
            search_val = input_field.get()
            combo_box = select_from_combobox.get()

            if (search_input == "All"):
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT transaction_id, teacher_id, teacher_name, payment_date, amount FROM teacher_transaction_detail"
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
                    query = "SELECT transaction_id, teacher_id, teacher_name, payment_date, amount FROM teacher_transaction_detail Where transaction_id = %s"
                    cursor.execute(query,(search_val,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

                    
            elif (search_input == "Teacher ID"):
                if not input_field.get() or not input_field.get().isdigit():
                    messagebox.showerror("Validation Error", "Input cannot be empty and digits are allowed")
                    return False
                
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT transaction_id, teacher_id, teacher_name, payment_date, amount FROM teacher_transaction_detail Where teacher_id = %s"
                    cursor.execute(query,(search_val,))
                    items = [f"{row[0]},{row[1]},{row[2]},{row[3]},{row[4]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    items = []

            elif (search_input == "Teachers Name"):
                
                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT transaction_id, teacher_id, teacher_name, payment_date, amount FROM teacher_transaction_detail WHERE teacher_name = %s"
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
                    query = "SELECT transaction_id, teacher_id, teacher_name, payment_date, amount FROM teacher_transaction_detail Where batch_year = %s"
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
            for widget in display_payment.winfo_children():
                widget.destroy()
            
            # Fetch fresh data
            fetch_payment_data()
            
            # Rebuild the display
            for i in range(len(items)+1):
                display_payment.grid_rowconfigure(i, weight=0)
            for j in range(6):
                display_payment.grid_columnconfigure(j, weight=1)
            
            # Header row
            ctk.CTkLabel(display_payment, text="Transaction ID").grid(row=0, column=0)
            ctk.CTkLabel(display_payment, text="Teacher ID").grid(row=0, column=1)
            ctk.CTkLabel(display_payment, text="Teacher Name").grid(row=0, column=2)
            ctk.CTkLabel(display_payment, text="Payment Date").grid(row=0, column=3)
            ctk.CTkLabel(display_payment, text="Payment Amount").grid(row=0, column=4)
            ctk.CTkLabel(display_payment, text="Action").grid(row=0, column=5)
            
            # Data rows
            for i, item in enumerate(items, start=1):
                transaction_id, teacher_id, teacher_name, date, amt = item.split(",")
                ctk.CTkLabel(display_payment, text=transaction_id).grid(row=i, column=0)
                ctk.CTkLabel(display_payment, text=teacher_id).grid(row=i, column=1)
                ctk.CTkLabel(display_payment, text=teacher_name).grid(row=i, column=2)
                ctk.CTkLabel(display_payment, text=date).grid(row=i, column=3)
                ctk.CTkLabel(display_payment, text=amt).grid(row=i, column=4)
                ctk.CTkButton(
                    display_payment,
                    text="View",
                    command=lambda tid=transaction_id: view_payment(tid)
                ).grid(row=i, column=5, pady=5)

        

        set_search_frame = ctk.CTkFrame(transaction_frame)
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

            elif (search_by.get() == "Transaction ID"):
                input_lbl.configure(text = f"Enter {search_by.get()}")
                select_from_combobox.grid_forget()
                input_field.delete(0, ctk.END)
                input_lbl.grid(row = 0, column = 2, sticky = "ew", padx = 5, pady = 5)
                input_field.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)

            elif (search_by.get() == "Teacher ID"):
                input_lbl.configure(text = f"Enter {search_by.get()}")
                select_from_combobox.grid_forget()
                input_field.delete(0, ctk.END)
                input_lbl.grid(row = 0, column = 2, sticky = "ew", padx = 5, pady = 5)
                input_field.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)

            elif (search_by.get() == "Teachers Name"):
                input_lbl.configure(text = f"Select {search_by.get()}")
                input_field.grid_forget()

                try:
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    query = "SELECT first_name, middle_name, last_name FROM teachers_detail"
                    cursor.execute(query)
                    search_teacher = [f"{row[0]} {row[1]} {row[2]}".strip() for row in cursor.fetchall()]
                    conn.close()
                except mysql.connector.Error as err:
                    messagebox.showerror("Database Error", f"Error retrieving data: {err}")
                    search_teacher = []
                
                input_lbl.grid(row = 0, column = 2, sticky = "ew", padx = 5, pady = 5)
                select_from_combobox.configure(values = search_teacher)
                select_from_combobox.set("-Select--")
                select_from_combobox.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)

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

                input_lbl.grid(row = 0, column = 2, sticky = "ew", padx = 5, pady = 5)
                select_from_combobox.configure(values = search_batch)
                select_from_combobox.set("-Select--")
                select_from_combobox.grid(row = 0, column = 3, sticky = "ew", padx = 5, pady = 5)


        ctk.CTkLabel(set_search_frame, text = "Search By").grid(row = 0, column = 0, sticky = "ew", padx = 5, pady = 5)

        search_by = ctk.CTkComboBox(set_search_frame, values = ["All", "Transaction ID", "Teacher ID", "Teachers Name", "Batch Year"])
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
        scrollable_frame_payment = ctk.CTkScrollableFrame(transaction_frame)
        scrollable_frame_payment.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True, padx=20, pady=20)
        
        # Create display frame (only once)
        display_payment = ctk.CTkFrame(scrollable_frame_payment)
        display_payment.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=10, expand=True)
        
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
    return payment_screen
