import customtkinter as ctk
import mysql.connector
from PIL import Image, ImageTk
import os
import sys
from tkinter import messagebox
from db_connection import get_db_connection
from admin.admin_dashboard import create_dashboard_screen, dashboard_page
from admin.teacher_section import create_teacher_screen, teacher_page
from admin.student_section import create_student_screen, student_page
from admin.payment_section import create_payment_screen, payment_page
from admin.fees_section import create_fees_screen, fees_page
from admin.exam_section import create_exam_screen, exam_page
from admin.attendance_section import create_attendance_screen, attendance_page
from admin.profile_section import create_profile_screen, profile_page
from admin.expense_section import create_expense_screen, expense_page

class LoginScreen:
    def __init__(self, root):
        self.root = root
        self.setup_login_screen()
        
    def setup_login_screen(self):
        # Configure window
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # Center the login window
        window_width = 400
        window_height = 500
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.title("Login - Digital Classroom")
        
        # Create login frame
        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Login title
        title_label = ctk.CTkLabel(self.login_frame, text="Digital Classroom", font=("Arial", 24, "bold"))
        title_label.pack(pady=(40, 20))
        
        subtitle_label = ctk.CTkLabel(self.login_frame, text="Admin Login", font=("Arial", 16))
        subtitle_label.pack(pady=(0, 30))
        
        # Username entry
        self.username_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Username", width=250)
        self.username_entry.pack(pady=10)
        
        # Password entry
        self.password_entry = ctk.CTkEntry(self.login_frame, placeholder_text="Password", show="*", width=250)
        self.password_entry.pack(pady=10)
        
        # Login button
        login_btn = ctk.CTkButton(self.login_frame, text="Login", command=self.attempt_login, width=250)
        login_btn.pack(pady=20)
        
        # Error label (hidden by default)
        self.error_label = ctk.CTkLabel(self.login_frame, text="", text_color="red")
        self.error_label.pack()
        
    def attempt_login(self):
        

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

        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Replace this with your actual authentication logic
        if username == USERNAME[0] and password == PASSWORD[0]:
            self.login_successful()
        else:
            self.error_label.configure(text="Invalid username or password")
    
    def login_successful(self):
        # Destroy login screen and launch admin interface
        self.login_frame.destroy()
        AdminInterface(self.root)

class AdminInterface:
    def __init__(self, root):
        self.root = root
        self.setup_admin_interface()
        
    def setup_admin_interface(self):
        # Configure window for admin interface
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")
        self.root.minsize(screen_width, screen_height)
        self.root.title("Digital Classroom - Admin")

        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)


        icon_path = resource_path("icons/icon.ico")
        # self.root.iconbitmap(icon_path)

        menu_bar_color = "#2C3E50"

        # Create screens
        dashboard_screen, dashboard_btn, teachers_btn, students_btn, payment_btn, expense_btn, fees_btn, attendance_btn, exam_btn, setting_btn = create_dashboard_screen(self.root, screen_width, menu_bar_color)
        
        teacher_screen = create_teacher_screen(self.root, screen_width, menu_bar_color)
        student_screen = create_student_screen(self.root, screen_width, menu_bar_color)
        payment_screen = create_payment_screen(self.root, screen_width, menu_bar_color)
        fees_screen = create_fees_screen(self.root, screen_width, menu_bar_color)
        attendance_screen = create_attendance_screen(self.root, screen_width, menu_bar_color)
        exam_screen = create_exam_screen(self.root, screen_width, menu_bar_color)
        profile_screen = create_profile_screen(self.root, screen_width, menu_bar_color)
        expense_screen = create_expense_screen(self.root, screen_width, menu_bar_color)

        # Hide all screens initially
        teacher_screen.pack_forget()
        student_screen.pack_forget()
        payment_screen.pack_forget()
        fees_screen.pack_forget()
        attendance_screen.pack_forget()
        exam_screen.pack_forget()
        profile_screen.pack_forget()
        expense_screen.pack_forget()

        # Pack the dashboard screen initially
        dashboard_screen.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)
        
        # Configure button commands
        dashboard_btn.configure(command=lambda: dashboard_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen))
        teachers_btn.configure(command=lambda: teacher_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen))
        students_btn.configure(command=lambda: student_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen))
        payment_btn.configure(command=lambda: payment_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen))
        expense_btn.configure(command=lambda: expense_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen))
        fees_btn.configure(command=lambda: fees_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen))
        attendance_btn.configure(command=lambda: attendance_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen))
        exam_btn.configure(command=lambda: exam_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen))
        setting_btn.configure(command=lambda: profile_page(dashboard_screen, teacher_screen, student_screen, payment_screen, expense_screen, fees_screen, attendance_screen, exam_screen, profile_screen))

def main():

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except AttributeError:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

    root = ctk.CTk()
    
    root.iconbitmap(resource_path("icons/icon.ico"))
    # Start with the login screen
    LoginScreen(root)
    root.mainloop()

if __name__ == "__main__":
    main()