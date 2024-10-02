import smtplib
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import datetime as dt
import os


# Email Automation GUI
class Email:
   # Authentication details
   auth = ('OneFlowAutomation@gmail.com', 'npiv sqhm msnh acgw')

   def __init__(self):
      # Initialize email list and CSV path
      self.email_list = []
      self.current_csv = ""

   # Function to send mass email
   def send_mass_email(self, subject, body):
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login(self.auth[0], self.auth[1])

      for email in self.email_list:
         message = f"From: {self.auth[0]}\nTo: {email}\nSubject: {subject}\n\n{body}"
         try:
               server.sendmail(self.auth[0], email, message)
         except Exception as e:
               messagebox.showerror("Error", f"Failed to send email to {email}: {e}")

      server.quit()
      messagebox.showinfo("Success", "Emails have been sent successfully!")

   # Function to upload CSV
   def upload_csv(self):
      self.current_csv = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
      if self.current_csv:
         email_frame = pd.read_csv(self.current_csv)
         self.email_list = email_frame.dropna().values.flatten().tolist()
         messagebox.showinfo("Success", "CSV file uploaded successfully!")

   # Function to display CSV content
   def display_csv(self, csv_view):
      if self.current_csv:
         email_frame = pd.read_csv(self.current_csv).dropna()
         csv_view.delete(1.0, tk.END)
         csv_view.insert(tk.END, email_frame.to_string(index=False))
      else:
         messagebox.showwarning("Warning", "No CSV uploaded!")

   # Function to send email (from email screen)
   def send_email(self, subject_entry, body_entry):
      subject = subject_entry.get()
      body = body_entry.get("1.0", tk.END).strip()

      if self.current_csv and subject and body:
         self.send_mass_email(subject, body)
      else:
         messagebox.showwarning("Warning", "Please upload a CSV, and enter subject and body.")

   # Navigation functions
   @staticmethod
   def show_frame(frame):
      frame.tkraise()

   def tkinter_gui(self):
      root = tk.Tk()
      root.title("OneFlow E-Mail Automation")
      root.geometry("800x500")
      root.resizable(False, False)

      # Set theme
      style = ttk.Style()
      style.theme_use("clam")

      # Define custom styles
      style.configure("TFrame", background="#f0f0f0")
      style.configure("TButton", font=("Helvetica", 12), background="#4CAF50", foreground="white")
      style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 14))
      style.configure("TEntry", padding=5, font=("Helvetica", 12))
      style.configure("TText", font=("Helvetica", 12))

      # Create the frames for each section
      main_menu = ttk.Frame(root, padding=100, style="TFrame")
      csv_upload = ttk.Frame(root, padding=20, style="TFrame")
      email_screen = ttk.Frame(root, padding=20, style="TFrame")
      csv_view_screen = ttk.Frame(root, padding=20, style="TFrame")

      for frame in (main_menu, csv_upload, email_screen, csv_view_screen):
         frame.grid(row=0, column=0, sticky="nsew")

      # Main menu layout (centered)
      main_title = ttk.Label(main_menu, text="OneFlow Automation - E-Mail Automater", font=("Arial", 24))
      main_title.pack(pady=0)

      upload_btn = ttk.Button(main_menu, text="Upload CSV", command=lambda: Email.show_frame(csv_upload), width=30)
      upload_btn.pack(pady=10)

      view_csv_btn = ttk.Button(main_menu, text="View Current CSV", command=lambda: Email.show_frame(csv_view_screen), width=30)
      view_csv_btn.pack(pady=10)

      email_btn = ttk.Button(main_menu, text="Send Mass E-Mail", command=lambda: Email.show_frame(email_screen), width=30)
      email_btn.pack(pady=10)

      exit_btn = ttk.Button(main_menu, text="Exit", command=root.quit, width=30)
      exit_btn.pack(pady=10)

      # CSV Upload Screen (centered)
      csv_upload_title = ttk.Label(csv_upload, text="Upload CSV", font=("Arial", 24))
      csv_upload_title.pack(pady=20)

      upload_csv_btn = ttk.Button(csv_upload, text="Select CSV File", command=self.upload_csv, width=30)
      upload_csv_btn.pack(pady=10)

      back_btn = ttk.Button(csv_upload, text="Back to Main Menu", command=lambda: Email.show_frame(main_menu), width=30)
      back_btn.pack(pady=10)

      # Email Sending Screen (centered)
      email_screen_title = ttk.Label(email_screen, text="Send Mass E-Mail", font=("Arial", 24))
      email_screen_title.pack(pady=20)

      subject_label = ttk.Label(email_screen, text="E-Mail Subject:")
      subject_label.pack()
      subject_entry = ttk.Entry(email_screen, width=50)
      subject_entry.pack(pady=5)

      body_label = ttk.Label(email_screen, text="E-Mail Body:")
      body_label.pack()
      body_entry = tk.Text(email_screen, height=10, width=50)
      body_entry.pack(pady=5)

      send_email_btn = ttk.Button(email_screen, text="Send E-Mail", command=lambda: self.send_email(subject_entry, body_entry), width=30)
      send_email_btn.pack(pady=10)

      back_to_main_btn = ttk.Button(email_screen, text="Back to Main Menu", command=lambda: Email.show_frame(main_menu), width=30)
      back_to_main_btn.pack(pady=10)

      # CSV Viewing Screen (centered)
      csv_view_title = ttk.Label(csv_view_screen, text="Current CSV", font=("Arial", 24))
      csv_view_title.pack(pady=20)

      csv_view = tk.Text(csv_view_screen, height=10, width=60)
      csv_view.pack(pady=10)

      refresh_btn = ttk.Button(csv_view_screen, text="Refresh CSV", command=lambda: self.display_csv(csv_view), width=30)
      refresh_btn.pack(pady=10)

      back_to_menu_btn = ttk.Button(csv_view_screen, text="Back to Main Menu", command=lambda: Email.show_frame(main_menu), width=30)
      back_to_menu_btn.pack(pady=10)

      # Show the main menu first
      Email.show_frame(main_menu)

      # Start the Tkinter loop
      root.mainloop()


class Text:
   def __init__(self):
      self.text_list = []
      self.current_csv = ""

   def tkinter_gui():
      root = tk.Tk()
      root.title("OneFlow Text Automation")
      root.geometry("800 x 500")
      root.resizeable(False, False)

      # Styling
      style = ttk.Style()
      style.theme_use('clam')
      style.configure("TFrame", background="#f0f0f0")
      style.configure("TButton", font=("Helvetica", 12), background="#4CAF50", foreground="white")
      style.configure("TLabel", background="#f0f0f0", font=("Helvetica", 14))
      style.configure("TEntry", padding=5, font=("Helvetica", 12))
      style.configure("TText", font=("Helvetica", 12))

      # Frames for each menu
      main_menu = ttk.Frame(root, padding=100, style="TFrame")
      csv_upload = ttk.Frame(root, padding=100, style="TFrame")
      send_text_screen = ttk.Frame(root, padding=100, style="TFrame")

      for frame in (main_menu, csv_upload, send_text_screen):
         frame.grid(row=0, column=0, sticky="nsew")

      main_title = ttk.Label(main_menu, text="OneFlow Text Automation", font="Arial")


   text_csv = pd.read_csv("AutoText.csv")
   user_frame = pd.DataFrame(text_csv)
   user_frame.columns = user_frame.columns.str.strip()
   people = {}

   for index, row in user_frame.iterrows():
      name = row['Name']
      phone_number = row['Phone']
      people[name] = phone_number




key = "553df227ee6b5643502d4fd312f13bc7cd833472vxmQm2Xy3anpwHqi07x33Pric"




if __name__ == "__main__":
   email_app = Email()
   email_app.tkinter_gui()
