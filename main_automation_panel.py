# OneFlow Automation Software License Agreement
#
# For any questions, contact: jmjaques01@gmail.com or (914-467-9943)
#
# Re-distribution or cloning of this software is strictly prohibited without prior written permission from the authors. 
# Any attempts to do so will result in legal actions as outlined under relevant jurisdiction.
#
# Copyright (C) 2024 OneFlow Automation. All rights reserved.
# Unauthorized use of this software is strictly prohibited.
# Commercial and non-commercial use, distribution, or modification of the software must adhere to the terms of this agreement.
# License terms and conditions are available upon request. 
# Contact for further inquiries: jmjaques01@gmail.com


import smtplib
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import datetime as dt
import requests
from tkinter import PhotoImage
import sys
import os
import webbrowser
import google.generativeai as genai
from tkinter import Toplevel
import customtkinter as ctk
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



genai.configure(api_key="AIzaSyDJMgwiv4rTqsicBRphBkleRi_ZnyWpbF8")

model = genai.GenerativeModel("gemini-1.5-flash")


# Primary Application Class - Handles All E-Mail and Text Processes
class Home:
   def __init__(self):
      self.current_csv = ''
      self.auth = ('OneFlowAutomation@gmail.com', 'npiv sqhm msnh acgw') # Replace with company automated G-Mail account.
      self.email_list = []
      self.text_list = []
      self.first_name_list = []
      self.last_name_list = []
      self.current_frame = None
      self.final_dataframe = None
      self.client_name = "Justin Jaques"
      self.texts_remaining = ""
      self.root = ctk.CTk()
      self.icon = PhotoImage(file=self.resource_path("OneFlow_Window_Icon.png"))
      self.first_name_reference = "[FirstName]"  
      self.last_name_reference = "[LastName]"
      self.selected_attachment_path = None
  
      
      
   # Loading the CSV Data, and getting the specific credentials such as Name, Email and Phone   
   def load_data(self):
      df = pd.read_csv(self.current_csv)
      df['Phone'] = df['Phone'].fillna("").astype(str).str.replace(".0", "", regex=False)
      self.first_name_list = df['First Name'].dropna().tolist()
      self.last_name_list = df['Last Name'].dropna().tolist()
      self.email_list = df['Email'].dropna().tolist()
      self.text_list = df['Phone'].dropna().tolist()
      
      
  # Opening the window for AI use
   def open_ai_window(self):
     ai_window = ctk.CTkToplevel(self.root)
     ai_window.title("OneAI - Powered by Gemini")
     ai_window.geometry("1000x600")
     ai_window.resizable(False, False)
     ai_window.iconphoto(False, self.icon)
     
     
     ai_response_box = ctk.CTkTextbox(ai_window, height=400, width=940, wrap=tk.WORD)
     ai_response_box.place(x=20, y=20)
     
     
    # Create a vertical scrollbar
     scrollbar = tk.Scrollbar(ai_window, command=ai_response_box.yview)
     scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

     # Configure the text box to use the scrollbar
     ai_response_box.configure(yscrollcommand=scrollbar.set)
     
     ai_query_box = ctk.CTkTextbox(ai_window, height=1, width=800)
     ai_query_box.place(x=90, y=500)
     ai_response_box.insert(tk.END, "OneAi: \n\n" + "Hi! I am OneAI, here to assist you with anything you need. Type a prompt such as: 'Draft a text to a potential client' below to get started!" + "\n")
     ai_response_box.configure(state="disabled")
     ai_query_box.bind("<Return>", lambda event: self.handle_query(ai_query_box, ai_response_box))
     
     
   def handle_query(self, ai_query_box, ai_response_box):
      user_query = ai_query_box.get("1.0", tk.END).strip()
      
      if not user_query:
         return
      
      
      ai_query_box.delete("1.0", tk.END)
      ai_response_box.configure(state="normal")     
      ai_response_box.delete("1.0", tk.END)
      ai_response_box.configure(state="disabled")
      self.send_ai_query(user_query, ai_response_box)

   def send_ai_query(self, user_query, ai_response_box):
      response = model.generate_content(user_query)
      ai_response_box.configure(state="normal")
      ai_response_box.insert(tk.END, "OneAi: \n\n" + response.text + "\n")
      ai_response_box.configure(state="disabled")
      

         
   # Handling uploading the CSV 
   def upload_csv(self):
      self.current_csv = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
      if self.current_csv:
         frame = pd.read_csv(self.current_csv)
         self.list = frame.dropna().values.flatten().tolist()
         messagebox.showinfo("Success", "CSV file uploaded successfully!")
         self.load_data()
         person_dict = {
            'First Name': self.first_name_list,
            'Last Name': self.last_name_list,
            'Phone': self.text_list,
            'Email': self.email_list
         }
         
         final_frame = pd.DataFrame(person_dict)
         self.final_dataframe = final_frame
         
         

   # Displaying the CSV content to the user on the CSV View page
   def display_csv(self, csv_view):
      if self.current_csv:
         df = self.final_dataframe.dropna()
         csv_view.delete(1.0, tk.END)
         csv_view.insert(tk.END, df.to_string(index=False))
      else:
         messagebox.showwarning("Warning", "No CSV uploaded!")
         
   # Function to handle e-mail sending.      
   def send_mass_email(self, subject, body, attachment_path=None):
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login(self.auth[0], self.auth[1])

      for index, email in enumerate(self.final_dataframe['Email']):
         personalized_body = body.replace(self.first_name_reference, self.final_dataframe["First Name"][index])
         personalized_body = personalized_body.replace(self.last_name_reference, self.final_dataframe['Last Name'][index])
         
         personalized_subject = subject.replace(self.first_name_reference, self.final_dataframe["First Name"][index])
         personalized_subject = personalized_subject.replace(self.last_name_reference, self.final_dataframe['Last Name'][index])
         
         message = MIMEMultipart()
         message['From'] = self.auth[0]
         message['To'] = email
         message['Subject'] = personalized_subject
         
         message.attach(MIMEText(personalized_body, 'plain'))
         
         if attachment_path:
            with open(attachment_path, 'rb') as attachment:
               part = MIMEBase('application', 'octet-stream')
               part.set_payload(attachment.read())
               encoders.encode_base64(part)
               part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(attachment_path)}')
               message.attach(part)
         
         try:
               server.sendmail(self.auth[0], email, message.as_string())
         except Exception as e:
               messagebox.showerror("Error", f"Failed to send email to {email}: {e}")

      server.quit()
      messagebox.showinfo("Success", "Emails have been sent successfully!")
      
    # Function to handle sending texts  
   def send_text(self, api_key_entry, text_entry, texts_left_entry, greeting_text_entry, signature_text_entry):
      text = text_entry.get("1.0", tk.END).strip()
      self.text_ids = []
      greeting = greeting_text_entry.get("1.0", tk.END).strip()
      signature = signature_text_entry.get("1.0", tk.END).strip()
      
      if text:
         if self.final_dataframe is not None:
            api_key = api_key_entry.get("1.0", tk.END).strip()
            for index, number in enumerate(self.final_dataframe['Phone']):
               personalized_greeting = greeting.replace(self.first_name_reference, self.final_dataframe["First Name"][index])
               personalized_greeting = personalized_greeting.replace(self.last_name_reference, self.final_dataframe["Last Name"][index])
               
               personalized_signature = signature.replace(self.first_name_reference, self.final_dataframe["First Name"][index])
               personalized_signature = personalized_signature.replace(self.last_name_reference, self.final_dataframe["Last Name"][index])
               
               personalized_text = text.replace(self.first_name_reference, self.final_dataframe["First Name"][index])
               personalized_text = personalized_text.replace(self.last_name_reference, self.final_dataframe["Last Name"][index])
               
               message = f"{personalized_greeting} \n\n" + personalized_text + "\n\n" + f"{personalized_signature},\n" + self.client_name # The format the text will follow
               
               # Sending a request to the textbelt API to send a text
               response = requests.post('https://textbelt.com/text', {
                  'phone': number,  
                  'message': message,
                  'replyWebhookUrl': 'http://107.201.157.230:5000/handle_sms',  
                  'key': api_key,

               })
               
               response_data = response.json()

               
               if 'quotaRemaining' in response_data:
                  self.texts_remaining = response_data['quotaRemaining']
                  texts_left_entry.config(state="normal")
                  texts_left_entry.delete(1.0, tk.END)
                  texts_left_entry.insert(tk.END, str(self.texts_remaining)) 
                  texts_left_entry.config(state="disabled")
            
               if response_data['success']:
                  text_id = response_data['textId']
                  self.text_ids.append((number, text_id))

      else:
         messagebox.showwarning("Warning", "Please upload a CSV, and enter a text.")
         

   # The resource path for files when running the executable         
   def resource_path(self, relative_path):
      try:
         base_path = sys._MEIPASS
      except Exception:
         base_path = os.path.abspath(".")
         print("Error loading resource")

      return os.path.join(base_path, relative_path)


   # Function that actually sending the e-mail after the data has been prepared.
   def send_email(self, subject_entry, body_entry, selected_attachment_path):
      subject = subject_entry.get("1.0", tk.END).strip()
      body = body_entry.get("1.0", tk.END).strip()

      if self.current_csv and subject and body:
         self.send_mass_email(subject, body, selected_attachment_path)
      else:
         messagebox.showwarning("Warning", "Please upload a CSV, and enter subject and body.")
         
   
   # Tkinter GUI methods
   @staticmethod
   def show_frame(frame):
      frame.tkraise()
      
   def switch_frame(self, frame):
      self.current_frame = frame
      self.show_frame(frame)
      
   def handle_email_attachment(self):
      attachment_path = filedialog.askopenfilename(filetypes=[("All files", "*.*"), ("PDF files", "*.pdf"), ("CSV files", "*.csv"), ("Excel files", "*.xls *.xlsx"), ("Images", "*.png *.jpg *.jpeg")])
      
      if attachment_path:
         self.selected_attachment_path = attachment_path
         messagebox.showinfo("Success", f"Image '{os.path.basename(attachment_path)}' has been attached!")
      else:
         self.selected_image_path = None
         messagebox.showwarning("Warning", "No image selected.")
      
   def open_email_window(self):
      email_window = ctk.CTkToplevel(self.root)
      email_window.title("OneFlow Automation - E-mail")
      email_window.geometry("1000x800")
      email_window.resizable(False, False)
      

      subject_label = ctk.CTkLabel(email_window, text="E-Mail Subject:")
      subject_label.place(x=440, y=50)
      
      subject_entry = ctk.CTkTextbox(email_window, width=400, height=20)
      subject_entry.place(x=280, y=100)

      body_label = ctk.CTkLabel(email_window, text="E-Mail Body:")
      body_label.place(x=450, y=200)
      
      body_entry = ctk.CTkTextbox(email_window, height=300, width=800)
      body_entry.place(x=90, y=250)

      send_email_btn = ctk.CTkButton(email_window, text="Send E-Mail", command=lambda: self.send_email(subject_entry, body_entry, self.selected_attachment_path),  width=170, height=40, corner_radius=3, fg_color="#4CAF50")
      send_email_btn.place(x=380, y=650)
      
      
      insert_file_btn = ctk.CTkButton(email_window, text="Attach Image", command=lambda: self.handle_email_attachment(),  width=170, height=40, corner_radius=3, fg_color="#4CAF50")
      insert_file_btn.place(x=600, y=650)
      
      use_ai_email_btn = ctk.CTkButton(email_window, text="Use AI", command=lambda: self.open_ai_window(),  width=170, height=40, corner_radius=3, fg_color="#4CAF50")
      use_ai_email_btn.place(x=160, y=650)
      
      insert_first_name_email_btn = ctk.CTkButton(email_window, text="Insert First Name", command=lambda: body_entry.insert("insert", "[FirstName]"),  width=170, height=40, corner_radius=3, fg_color="#4CAF50")
      insert_first_name_email_btn.place(x=160, y=720)
      
      insert_last_name_email_btn = ctk.CTkButton(email_window, text="Insert Last Name", command=lambda: body_entry.insert("insert", "[LastName]"),  width=170, height=40, corner_radius=3, fg_color="#4CAF50")
      insert_last_name_email_btn.place(x=380, y=720)
      
      use_ai_email_btn = ctk.CTkButton(email_window, text="Use AI", command=lambda: self.open_ai_window(),  width=170, height=40, corner_radius=3, fg_color="#4CAF50")
      use_ai_email_btn.place(x=160, y=650)



   
   def open_text_window(self):
      text_window = ctk.CTkToplevel(self.root)
      text_window.title("OneFlow Automation - Text")
      text_window.geometry("800x520")
      text_window.resizable(False, False)
      
      
      api_key_label = ctk.CTkLabel(text_window, text="API Key:")
      api_key_label.pack(pady=0)
      api_key_entry = ctk.CTkTextbox(text_window, height=1, width=480)
      api_key_entry.pack(pady=0)
      api_key_entry.insert(tk.END, key)
      
      texts_left_label = ctk.CTkLabel(text_window, text="Texts left:")
      texts_left_label.place(x=63, y=90)
      texts_left_entry = ctk.CTkTextbox(text_window, height=1, width=100)
      texts_left_entry.place(x=45, y=120)
      texts_left_entry.insert(tk.END, str(self.texts_remaining))
      texts_left_entry.configure(state="disabled") 
      
      
      
      text_screen_label = ctk.CTkLabel(text_window, text="Text:")
      text_screen_label.pack(pady=0)
      text_entry = ctk.CTkTextbox(text_window, height=340, width=340)
      text_entry.pack(pady=0)
      
      
      
      text_send_btn = ctk.CTkButton(text_window, text="Send", command=lambda: self.send_text(api_key_entry, text_entry, texts_left_entry, greeting_text_entry, signature_text_entry), width=110, height=32, corner_radius=3, fg_color="#4CAF50")
      text_send_btn.pack(pady=7)
      
      text_ai_btn = ctk.CTkButton(text_window, text="Use AI", command=lambda: self.open_ai_window(), width=120, height=38, corner_radius=3, fg_color="#4CAF50")
      text_ai_btn.place(x=620, y=150)
      
      insert_first_name_btn = ctk.CTkButton(text_window, text="Insert First Name", command=lambda: text_entry.insert("insert", "[FirstName]"), width=120, height=30, corner_radius=3, fg_color="#4CAF50")
      insert_first_name_btn.place(x=620, y=300)
      
      
      insert_last_name_btn = ctk.CTkButton(text_window, text="Insert Last Name", command=lambda: text_entry.insert("insert", "[FirstName]"), width=120, height=30, corner_radius=3, fg_color="#4CAF50")
      insert_last_name_btn.place(x=620, y=340)


      greeting_text_label = ctk.CTkLabel(text_window, text="Greeting:", font=("Arial", 10))
      greeting_text_label.place(x=20, y=250)
      
      greeting_text_entry =  ctk.CTkTextbox(text_window, height=1, width=200)
      greeting_text_entry.place(x=20, y=280)
      greeting_text_entry.insert("1.0", "Good afternoon [FirstName]")
      
      
      signature_text_label = ctk.CTkLabel(text_window, text="Signature:", font=("Arial", 10))
      signature_text_label.place(x=20, y=330)
      
      signature_text_entry = ctk.CTkTextbox(text_window, height=1, width=200)
      signature_text_entry.place(x=20, y=360)
      signature_text_entry.insert("1.0", "Sincerely")
      

      get_more_credits_btn = ctk.CTkButton(text_window, text="Buy More", command=lambda: webbrowser.open("https://textbelt.com/purchase/?generateKey=1"), width=120, height=32, corner_radius=3, fg_color="#4CAF50")
      get_more_credits_btn.place(x=36, y=160)
  
   
   

   def gui(self):
      
      ctk.set_appearance_mode("System")
      ctk.set_default_color_theme("blue")

      
      self.root.title("OneFlow Automation Home Panel")
      self.root.geometry("800x520")
      self.root.resizable(False, False)

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
      main_menu = ttk.Frame(self.root, width=800, height=800, style="TFrame")
      csv_upload = ttk.Frame(self.root, width=200, height=200, style="TFrame")
      csv_view_screen = ttk.Frame(self.root, width=200, height=200, style="TFrame")



      for frame in (main_menu, csv_upload, csv_view_screen):
         frame.grid(row=0, column=0, sticky="nsew")

      
      email_btn = ctk.CTkButton(main_menu, text="Send E-Mails", command=lambda: self.open_email_window(), width=200, height=40, corner_radius=3, fg_color="#4CAF50")
      email_btn.place(x=150, y=300)
      email_btn.configure(cursor="hand2")
      
      text_btn =  ctk.CTkButton(main_menu, text="Send Texts", command=lambda: self.open_text_window(), width=200, height=40, corner_radius=3, fg_color="#4CAF50")
      text_btn.place(x=150, y=360)
      text_btn.configure(cursor="hand2")
      
      oneflow_label = ctk.CTkLabel(main_menu, text="OneFlow", font=("Helvetica", 48, "bold"), text_color="black")
      oneflow_label.place(x=300, y=20)
         


      # Add copyright text at the bottom
      copyright_label = ttk.Label(
        main_menu, 
        text="© Justin Jaques, 2024. Re-distribution prohibited.", 
        font=("Helvetica", 8), 
    )
      copyright_label.place(x=0, y=510, anchor="w", width=800)  
      

      view_csv_btn = ctk.CTkButton(main_menu, text="View Current CSV", command=lambda: self.switch_frame(csv_view_screen), width=200, height=40, corner_radius=3, fg_color="#4CAF50")
      view_csv_btn.place(x=450, y=300)
      view_csv_btn.configure(cursor="hand2")

      upload_btn = ctk.CTkButton(main_menu, text="Upload CSV", command=lambda: self.switch_frame(csv_upload), width=200, height=40, corner_radius=3, fg_color="#4CAF50")
      upload_btn.place(x=450, y=360)
      upload_btn.configure(cursor="hand2")

      exit_btn = ctk.CTkButton(main_menu, text="Exit", command=self.root.quit, width=200, height=40, corner_radius=3, fg_color="#4CAF50")
      exit_btn.place(x=300, y=440)
      exit_btn.configure(cursor="hand2")


      upload_csv_btn = ctk.CTkButton(csv_upload, text="Select CSV File", command=self.upload_csv, width=160, height=70, corner_radius=3, fg_color="#4CAF50")
      upload_csv_btn.place(x=325, y=200)

      back_btn = ctk.CTkButton(csv_upload, text="Back to Main Menu", command=lambda: self.show_frame(main_menu), width=160, height=70, corner_radius=3, fg_color="#4CAF50")
      back_btn.place(x=325, y=300)

  
      # CSV Viewing Screen 
      csv_view_title = ctk.CTkLabel(csv_view_screen, text="Current CSV", font=("Arial", 24), text_color="black")
      csv_view_title.place(x=335, y=55)
      

      csv_view = ctk.CTkTextbox(csv_view_screen, height=220, width=500)
      csv_view.place(x=150, y=100)
      

      refresh_btn = ctk.CTkButton(csv_view_screen, text="Refresh CSV", command=lambda: self.display_csv(csv_view), width=200, height=40, corner_radius=3, fg_color="#4CAF50")
      refresh_btn.place(x=150, y=350)

      back_to_menu_btn = ctk.CTkButton(csv_view_screen, text="Back to Main Menu", command=lambda: self.show_frame(main_menu), width=200, height=40, corner_radius=3, fg_color="#4CAF50")
      back_to_menu_btn.place(x=450, y=350)


   
      self.switch_frame(main_menu) # Make main menu the starting frame


      
      
      self.root.iconphoto(False, self.icon)
      self.root.mainloop()
         


key = "553df227ee6b5643502d4fd312f13bc7cd833472vxmQm2Xy3anpwHqi07x33Pric" # Companies will have to use their own API Key.



if __name__ == "__main__":
    app = Home()  
    app.gui() 

