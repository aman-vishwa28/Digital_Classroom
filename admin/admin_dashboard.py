import customtkinter as ctk
from PIL import Image, ImageTk
import os
from db_connection import get_db_connection
import mysql.connector
from customtkinter import CTkImage
from tkinter import messagebox, simpledialog


def dashboard_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen):
    teacher_screen.pack_forget()
    student_screen.pack_forget()
    payment_screen.pack_forget()
    fees_screen.pack_forget()
    attendance_screen.pack_forget()
    exam_screen.pack_forget()
    profile_screen.pack_forget()
    expense_screen.pack_forget()
    dashboard_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

#sidebar resize
def extend_menu_bar(menu_bar_frame, _logo):
    if menu_bar_frame.winfo_width() == 75:
        menu_bar_frame.configure(width=190)  # Expand the menu bar
        _logo.grid()  # Show the logo
    else:
        menu_bar_frame.configure(width=50)  # Collapse the menu bar
        _logo.grid_remove()  # Hide the logo

def create_dashboard_screen(root, screen_width, menu_bar_color):
    # Navigation Menu
    menu_bar_frame = ctk.CTkFrame(root, fg_color=menu_bar_color, corner_radius=0, border_width=0)
    menu_bar_frame.pack(side=ctk.LEFT, fill=ctk.Y, pady=0, padx=0)
    menu_bar_frame.configure(width=50)
    menu_bar_frame.pack_propagate(flag=False)

    # side menu Content
    side_menu_content = ctk.CTkFrame(menu_bar_frame, fg_color=menu_bar_color)
    side_menu_content.place(x=0, y=50)

    # dashboard screen
    dashboard_screen = ctk.CTkFrame(root,corner_radius=0,border_width=0)
    dashboard_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
    dashboard_screen.configure(width=screen_width - 50)

    # Define icons directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icons_dir = os.path.join(base_dir, "..", "icons")

    # Title strip
    Admin_title_bar = ctk.CTkFrame(dashboard_screen, fg_color=menu_bar_color, corner_radius=0, border_width=0)
    Admin_title_bar.pack(side=ctk.TOP, fill=ctk.X, anchor="n", pady=0)
    Admin_title_bar.configure(height=100)

    # Admin Panel Title
    Admin_title = ctk.CTkLabel(Admin_title_bar, text="Admin Panel", fg_color=menu_bar_color, text_color="white", font=("Gudea", 20, "bold"))
    Admin_title.pack(side=ctk.LEFT, expand=True)

    # Profile icon
    profile_img = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "profile.jpg")))
    profile = ctk.CTkButton(Admin_title_bar, text="", width=40,height=40, image=profile_img, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    profile.image = profile_img  # Keep a reference to the image
    profile.pack(side=ctk.RIGHT, padx=0, pady=10)

    
    # Year selection
    year_selection_frame = ctk.CTkFrame(dashboard_screen)
    year_selection_frame.pack(side=ctk.TOP, fill=ctk.X, padx=10, pady=5)

    total_students = 0
    total_courses = 0
    total_teachers = 0
    fees_estimated = 0
    payment_paid = 0
    pending_fee = 0
    total_paid = 0
    profit_amt = 0
    total_expense = 0

    def update_dashboard(*args):
        global total_students
        global total_courses
        global total_teachers
        global fees_estimated
        global payment_paid
        global pending_fee
        global total_paid
        global profit_amt
        global total_expense

        if(select_year.get() != "--Select--"):
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

            password_for_show_account = simpledialog.askstring("Password", "Enter admin password:", show='*')
        
            if password_for_show_account is None:  # If user cancels
                select_year.set("--Select--")
                return
            
            if password_for_show_account != PASSWORD[0]:  # Replace with actual admin password
                messagebox.showerror("Error", "Incorrect password! Deletion not allowed.")
                select_year.set("--Select--")
                return

            
            try:
                conn = get_db_connection()
                cursor1 = conn.cursor()
                query1 = "SELECT COUNT(*) FROM students_detail WHERE academic_year = %s"
                cursor1.execute(query1, (select_year.get(),))
                student_count = cursor1.fetchone()
                total_students = student_count[0]
                total_student.configure(text = f"Total Student's\n{total_students}")


                cursor2 = conn.cursor()
                query2 = "SELECT COUNT(*) FROM courses"
                cursor2.execute(query2)
                course_count = cursor2.fetchone()
                total_courses = course_count[0]
                total_course.configure(text = f"Total Courses\n{total_courses}")


                cursor3 = conn.cursor()
                query3 = "SELECT COUNT(*) FROM teachers_detail"
                cursor3.execute(query3)
                teacher_count = cursor3.fetchone()
                total_teachers = teacher_count[0]
                total_teacher.configure(text = f"Total Teacher's\n{total_teachers}")


                cursor4 = conn.cursor()
                query4 = "SELECT SUM(total_fees) FROM students_detail where academic_year = %s"
                cursor4.execute(query4, (select_year.get(),))
                fees_estimate_count = cursor4.fetchone()
                fees_estimated = fees_estimate_count[0]
                total_fees_estimate.configure(text = f"Total Fees Estimated\n{fees_estimated}")


                cursor5 = conn.cursor()
                query5 = "SELECT SUM(amount) FROM teacher_transaction_detail where batch_year = %s"
                cursor5.execute(query5, (select_year.get(),))
                payment_paid_count = cursor5.fetchone()
                payment_paid = payment_paid_count[0]
                total_payment_paid.configure(text = f"Total Payment Paid\n{payment_paid}")


                cursor6 = conn.cursor()
                query6 = "SELECT SUM(pending_fees) FROM students_detail where academic_year = %s"
                cursor6.execute(query6, (select_year.get(),))
                pending_fees_count = cursor6.fetchone()
                pending_fee = pending_fees_count[0]
                pending_fees.configure(text = f"Pending Fees\n{pending_fee}")


                cursor7 = conn.cursor()
                query7 = "SELECT SUM(total_paid) FROM students_detail where academic_year = %s"
                cursor7.execute(query7, (select_year.get(),))
                collected_fees_count = cursor7.fetchone()
                total_paid = collected_fees_count[0]
                fee_collected.configure(text = f"Fees Collected\n{total_paid}")

                cursor8 = conn.cursor()
                query8 = "SELECT SUM(amount) FROM expenditure where batch_year = %s"
                cursor8.execute(query8, (select_year.get(),))
                expense_count = cursor8.fetchone()
                total_expense = expense_count[0]
                other_expense.configure(text=f"Other Expense\n{total_expense}")

                if total_paid != None and payment_paid != None and pending_fee != None:
                    profit_amt = total_paid - (payment_paid + total_expense)
                    profit.configure(text = f"Profit\n {profit_amt}")
                    if profit_amt < 0:
                        profit.configure(text = f"Loss\n {profit_amt}")

                else:
                    profit.configure(text = f"Profit\n Something is None")

                conn.close()

                # return student_names_to_display
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error Retrieving data: {err}")
                total_students = 0
                total_courses = 0
                total_teachers = 0
                fees_estimated = 0
                payment_paid = 0
                pending_fee = 0
                total_paid = 0
                profit_amt = 0
                total_expense = 0
        else:
            total_students = 0
            total_courses = 0
            total_teachers = 0
            fees_estimated = 0
            payment_paid = 0
            pending_fee = 0
            total_paid = 0
            profit_amt = 0
            total_expense = 0

            profit.configure(text = f"Profit\n{profit_amt}")
            other_expense.configure(text=f"Other Expense\n{total_expense}")
            fee_collected.configure(text = f"Fees Collected\n{total_paid}")
            pending_fees.configure(text = f"Pending Fees\n{pending_fee}")
            total_payment_paid.configure(text = f"Total Payment Paid\n{payment_paid}")
            total_fees_estimate.configure(text = f"Total Fees Estimated\n{fees_estimated}")
            total_teacher.configure(text = f"Total Teacher's\n{total_teachers}")
            total_course.configure(text = f"Total Courses\n{total_courses}")
            total_student.configure(text = f"Total Student's\n{total_students}")




        # total_student.configure
    

    # Retrieving Batch
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



    # batch_values =
    select_year = ctk.CTkComboBox(year_selection_frame, values=["--Select--"] + batch_values, state="readonly",font=("Arial",12,"bold"))
    select_year.pack(side=ctk.LEFT, padx=20, pady=5)
    select_year.set("--Select--")
    select_year.configure(command=update_dashboard)

    # ctk.CTkButton(year_selection_frame).pack(side=ctk.LEFT, padx=20, pady=5)


    # Load side menu icons
    toggle_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "menu-burger.png")))
    toggle_menu_btn = ctk.CTkButton(menu_bar_frame, text="", image=toggle_icon, width=40,height=40, fg_color=menu_bar_color, border_width=0, command=lambda: extend_menu_bar(menu_bar_frame, _logo))
    toggle_menu_btn.image = toggle_icon
    toggle_menu_btn.place(x=10,y=10)
    #toggle_menu_btn.place(x=0, y=10)

    # Load Icons
    home_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "home.png")))
    home_menu_btn = ctk.CTkButton(menu_bar_frame, image=home_icon, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    home_menu_btn.image = home_icon

    dashboard_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "dashboard.png")))
    dashboard_menu_btn = ctk.CTkButton(menu_bar_frame, image=dashboard_icon, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    dashboard_menu_btn.image = dashboard_icon

    teacher_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "teacher.png")))
    teacher_menu_btn = ctk.CTkButton(menu_bar_frame, image=teacher_icon, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    teacher_menu_btn.image = teacher_icon

    student_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "student.png")))
    student_menu_btn = ctk.CTkButton(menu_bar_frame, image=student_icon, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    student_menu_btn.image = student_icon

    payment_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "payment.png")))
    payment_menu_btn = ctk.CTkButton(menu_bar_frame, image=payment_icon, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    payment_menu_btn.image = payment_icon
    
    #======
    expense_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "expenditure.png")))
    expense_menu_btn = ctk.CTkButton(menu_bar_frame, image=expense_icon, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    expense_menu_btn.image = expense_icon
    #======

    fees_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "fees.png")))
    fees_menu_btn = ctk.CTkButton(menu_bar_frame, image=fees_icon, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    fees_menu_btn.image = fees_icon

    attendance_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "attendance.png")))
    attendance_menu_btn = ctk.CTkButton(menu_bar_frame, image=attendance_icon, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    attendance_menu_btn.image = attendance_icon

    exam_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "exam.png")))
    exam_menu_btn = ctk.CTkButton(menu_bar_frame, image=exam_icon, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    exam_menu_btn.image = exam_icon

    setting_icon = ctk.CTkImage(light_image=Image.open(os.path.join(icons_dir, "settings.png")))
    setting_menu_btn = ctk.CTkButton(menu_bar_frame, image=setting_icon, fg_color=menu_bar_color, border_width=0, hover_color=menu_bar_color)
    setting_menu_btn.image = setting_icon


    # Load the logo
    logo_path = os.path.join(icons_dir, "logo.png")
    class_logo = ctk.CTkImage(light_image=Image.open(logo_path), size=(150, 150))

    # Create the logo button
    _logo = ctk.CTkButton(
        side_menu_content,
        text="",
        image=class_logo,
        compound=ctk.LEFT,
        border_width=0,
        fg_color=menu_bar_color,
        hover_color=menu_bar_color
    )
    _logo.image = class_logo
    _logo.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

    # Hide logo initially
    _logo.grid_remove()

    side_menu_content.grid_columnconfigure(0, weight=0)
    for i in range(10):
        side_menu_content.grid_rowconfigure(i,weight=1)

    
    side_text = "white"
    # Navigation buttons
    dashboard_btn = ctk.CTkButton(side_menu_content, text="   Dashboard", image=dashboard_icon, compound=ctk.LEFT, border_width=0, fg_color=menu_bar_color, text_color=side_text, font=("Gudea", 15, "bold"), anchor="w")
    dashboard_btn.grid(row=1, column=0, pady=0, padx=10, sticky="ew")

    teachers_btn = ctk.CTkButton(side_menu_content, text="   Teachers", image=teacher_icon, compound=ctk.LEFT, border_width=0, text_color=side_text, fg_color=menu_bar_color, font=("Gudea", 15, "bold"), anchor="w")
    teachers_btn.grid(row=2, column=0, pady=0, padx=10, sticky="ew")

    students_btn = ctk.CTkButton(side_menu_content, text="   Students", image=student_icon, compound=ctk.LEFT, border_width=0, text_color=side_text, fg_color=menu_bar_color, font=("Gudea", 15, "bold"), anchor="w")
    students_btn.grid(row=3, column=0, pady=0, padx=10, sticky="ew")

    payment_btn = ctk.CTkButton(side_menu_content, text="   Payments", image=payment_icon, compound=ctk.LEFT, border_width=0, text_color=side_text, fg_color=menu_bar_color, font=("Gudea", 15, "bold"), anchor="w")
    payment_btn.grid(row=4, column=0, pady=0, padx=10, sticky="ew")

    #===============
    expense_btn = ctk.CTkButton(side_menu_content, text="   Expense", image=expense_icon, compound=ctk.LEFT, border_width=0, text_color=side_text, fg_color=menu_bar_color, font=("Gudea", 15, "bold"), anchor="w")
    expense_btn.grid(row=5, column=0, pady=0, padx=10, sticky="ew")
    #===============

    fees_btn = ctk.CTkButton(side_menu_content, text="   Fee Collection", image=fees_icon, compound=ctk.LEFT, border_width=0, text_color=side_text, fg_color=menu_bar_color, font=("Gudea", 15, "bold"), anchor="w")
    fees_btn.grid(row=6, column=0, pady=0, padx=10, sticky="ew")

    attendance_btn = ctk.CTkButton(side_menu_content, text="   Attendance", image=attendance_icon, compound=ctk.LEFT, border_width=0, text_color=side_text, fg_color=menu_bar_color, font=("Gudea", 15, "bold"), anchor="w")
    attendance_btn.grid(row=7, column=0, pady=0, padx=10, sticky="ew")

    exam_btn = ctk.CTkButton(side_menu_content, text="   Exam", image=exam_icon, compound=ctk.LEFT, border_width=0, text_color=side_text, fg_color=menu_bar_color, font=("Gudea", 15, "bold"), anchor="w")
    exam_btn.grid(row=8, column=0, pady=0, padx=10, sticky="ew")

    setting_btn = ctk.CTkButton(side_menu_content, text="   Setting Profile", image=setting_icon,  compound=ctk.LEFT, border_width=0, text_color=side_text, fg_color=menu_bar_color, font=("Gudea", 15, "bold"), anchor="w")
    setting_btn.grid(row=9, column=0, pady=0, padx=10, sticky="ew")

    # Cards Container
    cards_container = ctk.CTkFrame(dashboard_screen)
    cards_container.pack(fill=ctk.X, padx=5, pady=5, expand=True, anchor="n")

    for i in range(3):  # Assuming 3 columns
        cards_container.grid_columnconfigure(i, weight=1)

    for j in range(4):
        cards_container.grid_rowconfigure(j, weight=1)

    # Card 1
    card1 = ctk.CTkFrame(cards_container, fg_color="#1E88E5")
    card1.grid(row=0, column=0, padx=15, pady=10, sticky="ew")

    total_student = ctk.CTkLabel(card1, text_color="black", fg_color="#1E88E5", text=f"Total Student's\n{total_students}", font=("Gudea", 20, "bold"))
    total_student.pack(padx=10, pady=10)

    # Card 2
    card2 = ctk.CTkFrame(cards_container, fg_color="#FDD835")
    card2.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

    total_course = ctk.CTkLabel(card2, text_color="black", fg_color="#FDD835", text=f"Total Courses\n{total_courses}", font=("Gudea", 20, "bold"))
    total_course.pack(padx=10, pady=10)

    # Card 3
    card3 = ctk.CTkFrame(cards_container, fg_color="#43A047")
    card3.grid(row=0, column=2, padx=15, pady=10, sticky="ew")

    total_teacher = ctk.CTkLabel(card3, text_color="black", fg_color="#43A047", text=f"Total Teacher's\n{total_teachers}", font=("Gudea", 20, "bold"))
    total_teacher.pack(padx=10, pady=10)

    # Card 4
    card4 = ctk.CTkFrame(cards_container, fg_color="#00ACC1")
    card4.grid(row=1, column=0,columnspan=3, padx=15, pady=10, sticky="ew")

    total_fees_estimate = ctk.CTkLabel(card4, text_color="black", fg_color="#00ACC1", text=f"Total Fees Estimated\n{fees_estimated}", font=("Gudea", 20, "bold"))
    total_fees_estimate.pack(padx=10, pady=10)

    # Card 5
    card5 = ctk.CTkFrame(cards_container, fg_color="#4CAF50")
    card5.grid(row=2, column=0,columnspan=2, padx=15, pady=10, sticky="ew")

    total_payment_paid = ctk.CTkLabel(card5, text_color="black", fg_color="#4CAF50", text=f"Total Payment Paid\n{payment_paid}", font=("Gudea", 20, "bold"))
    total_payment_paid.pack(padx=10, pady=10)

    # Card 6
    card6 = ctk.CTkFrame(cards_container, fg_color="#FFA726")
    card6.grid(row=2, column=2,columnspan=2, padx=15, pady=10, sticky="ew")

    other_expense = ctk.CTkLabel(card6, text_color="black", fg_color="#FFA726", text=f"Other Expense\n{total_expense}", font=("Gudea", 20, "bold"))
    other_expense.pack(padx=10, pady=10)

    # Card 7
    card7 = ctk.CTkFrame(cards_container, fg_color="#EF5350")
    card7.grid(row=3, column=0, padx=15, pady=10, sticky="ew")

    pending_fees = ctk.CTkLabel(card7, text_color="black", fg_color="#EF5350", text=f"Pending Fees\n{pending_fee}", font=("Gudea", 20, "bold"))
    pending_fees.pack(padx=10, pady=10)

    # Card 8
    card8 = ctk.CTkFrame(cards_container, fg_color="white")
    card8.grid(row=3, column=1, padx=15, pady=10, sticky="ew")

    fee_collected = ctk.CTkLabel(card8, text_color="black", fg_color="white", text=f"Fees Collected\n{total_paid}", font=("Gudea", 20, "bold"))
    fee_collected.pack(padx=10, pady=10)

    # Card 9
    card9 = ctk.CTkFrame(cards_container, fg_color="#AB47BC")
    card9.grid(row=3, column=2, padx=15, pady=10, sticky="ew")

    profit = ctk.CTkLabel(card9, text_color="black", fg_color="#AB47BC", text=f"Profit\n{profit_amt}", font=("Gudea", 20, "bold"))
    profit.pack(padx=10, pady=10)
    

    return dashboard_screen, dashboard_btn, teachers_btn, students_btn, payment_btn, expense_btn, fees_btn, attendance_btn, exam_btn, setting_btn