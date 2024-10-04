# OneFlow Automation Primary Panel Blueprint - for any questions, contact jmjaques01@gmail.com or (914-467-9943)
# Re-Distribution or cloning of this software is strictly prohibited. Any attempts to do so will result in severe legal punishment.
# Copyright, OneFlow Automation, 2024 <- We need to get this copyrighted
# Justin Jaques

import smtplib
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import datetime as dt
import os
import requests
from tkinter import PhotoImage
import time
import threading
from tkinter.scrolledtext import ScrolledText
from flask import Flask, request, jsonify


class Home:
   def __init__(self):
      self.current_csv = ''
      self.auth = ('OneFlowAutomation@gmail.com', 'npiv sqhm msnh acgw') # Replace with company automated G-Mail account.
      self.email_list = []
      self.text_list = []
      self.name_list = []
      self.current_frame = None
      self.final_dataframe = None
      self.company_name = "Blueprint"
      self.texts_remaining = ""
      
   def load_texts(self):
      texts_df = pd.read_csv(self.current_csv)
      texts_df['Phone'] = texts_df['Phone'].fillna("").astype(str).str.replace(".0", "", regex=False)
      for number in texts_df['Phone']:
         self.text_list.append(number)

   def load_emails(self):
      emails_df = pd.read_csv(self.current_csv)
      for email in emails_df['Email']:
         self.email_list.append(email)
   
   def load_names(self):
      names_df = pd.read_csv(self.current_csv)
      for name in names_df['Name']:
         self.name_list.append(name)
      
      
   # Upload CSV
   def upload_csv(self):
      self.current_csv = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
      if self.current_csv:
         frame = pd.read_csv(self.current_csv)
         self.list = frame.dropna().values.flatten().tolist()
         messagebox.showinfo("Success", "CSV file uploaded successfully!")
         self.load_texts()
         self.load_emails()
         self.load_names()
         
         person_dict = {
            'Name': self.name_list,
            'Phone': self.text_list,
            'Email': self.email_list
         }
         
         final_frame = pd.DataFrame(person_dict)
         self.final_dataframe = final_frame
         
         

   # Display CSV content
   def display_csv(self, csv_view):
      if self.current_csv:
         df = self.final_dataframe.dropna()
         csv_view.delete(1.0, tk.END)
         csv_view.insert(tk.END, df.to_string(index=False))
      else:
         messagebox.showwarning("Warning", "No CSV uploaded!")
         
   def send_mass_email(self, subject, body):
      server = smtplib.SMTP("smtp.gmail.com", 587)
      server.starttls()
      server.login(self.auth[0], self.auth[1])

      for email in self.final_dataframe['Email']:
         message = f"From: {self.auth[0]}\nTo: {email}\nSubject: {subject}\n\n + {body}"
         try:
               server.sendmail(self.auth[0], email, message)
         except Exception as e:
               messagebox.showerror("Error", f"Failed to send email to {email}: {e}")

      server.quit()
      messagebox.showinfo("Success", "Emails have been sent successfully!")
      
   def send_text(self, api_key_entry, text_entry, texts_left_entry):
      text = text_entry.get("1.0", tk.END).strip()
      self.text_ids = []
      
      if text:
         api_key = api_key_entry.get("1.0", tk.END).strip()
         for index, number in enumerate(self.final_dataframe['Phone']):
            message = f"Hello, {self.final_dataframe['Name'][index]}\n" + text
            
            response = requests.post('https://textbelt.com/text', {
               'phone': number,  
               'message': message,
               'replyWebhookUrl': 'http://107.201.157.230:5000/handle_sms',  
               'key': api_key,

            })
            
            response_data = response.json()
            
            self.texts_remaining = response_data['quotaRemaining']
            
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
         

   def send_email(self, subject_entry, body_entry):
      subject = subject_entry.get()
      body = body_entry.get("1.0", tk.END).strip()

      if self.current_csv and subject and body:
         self.send_mass_email(subject, body)
      else:
         messagebox.showwarning("Warning", "Please upload a CSV, and enter subject and body.")
         
   
   @staticmethod
   def show_frame(frame):
      frame.tkraise()
      
   def switch_frame(self, frame):
      self.current_frame = frame
      self.show_frame(frame)

   def gui(self):
      root = tk.Tk()
      root.title("OneFlow Automation Panel")
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
      csv_upload = ttk.Frame(root, padding=200, style="TFrame")
      email_screen = ttk.Frame(root, padding=200, style="TFrame")
      csv_view_screen = ttk.Frame(root, width=200, style="TFrame")
      text_screen = ttk.Frame(root, width=500, style='TFrame')


      for frame in (main_menu, csv_upload, email_screen, csv_view_screen, text_screen):
         frame.grid(row=0, column=0, sticky="nsew")

      
      menu_bg_image = tk.PhotoImage(file="menu-background-image.png")
      background_label = tk.Label(main_menu, image=menu_bg_image)
      background_label.place(x = -100, y=-100) 
      
      email_btn = ttk.Button(main_menu, text="Send Mass E-Mail", command=lambda: self.switch_frame(email_screen), width=30)
      email_btn.place(x=150, y=100)
      email_btn.config(cursor="hand2")
      
      text_btn = ttk.Button(main_menu, text="Send Mass Text", command=lambda: self.switch_frame(text_screen), width=30)
      text_btn.place(x=150, y=150)
      text_btn.config(cursor="hand2")

      view_csv_btn = ttk.Button(main_menu, text="View Current CSV", command=lambda: self.switch_frame(csv_view_screen), width=30)
      view_csv_btn.place(x=150, y=200)
      view_csv_btn.config(cursor="hand2")

      upload_btn = ttk.Button(main_menu, text="Upload CSV", command=lambda: self.switch_frame(csv_upload), width=30)
      upload_btn.place(x=150, y=250)
      upload_btn.config(cursor="hand2")

      exit_btn = ttk.Button(main_menu, text="Exit", command=root.quit, width=30)
      exit_btn.place(x=150, y=300)
      exit_btn.config(cursor="hand2")

      # CSV Upload Screen (centered)
      csv_upload_title = ttk.Label(csv_upload, text="Upload CSV", font=("Arial", 24))
      csv_upload_title.place(x=120, y=-90)

      upload_csv_btn = ttk.Button(csv_upload, text="Select CSV File", command=self.upload_csv, width=30)
      upload_csv_btn.pack(pady=10)

      back_btn = ttk.Button(csv_upload, text="Back to Main Menu", command=lambda: self.show_frame(main_menu), width=30)
      back_btn.pack(pady=10)

      # Email Sending Screen (centered)
      email_screen_title = ttk.Label(email_screen, text="Send Mass E-Mail", font=("Arial", 24))
      email_screen_title.place(x=90, y=-190)

      subject_label = ttk.Label(email_screen, text="E-Mail Subject:")
      subject_label.place(x=150, y=-130)
      
      subject_entry = ttk.Entry(email_screen, width=50)
      subject_entry.place(x=50, y=-100)

      body_label = ttk.Label(email_screen, text="E-Mail Body:")
      body_label.place(x=150, y=-30)
      
      body_entry = tk.Text(email_screen, height=10, width=50)
      body_entry.pack(pady=5)

      send_email_btn = ttk.Button(email_screen, text="Send E-Mail", command=lambda: self.send_email(subject_entry, body_entry), width=30)
      send_email_btn.pack(pady=10)

      back_to_main_btn = ttk.Button(email_screen, text="Back to Main Menu", command=lambda: self.show_frame(main_menu), width=30)
      back_to_main_btn.pack(pady=10)
      
      # Text sending screen

      api_key_label = ttk.Label(text_screen, text="API Key:")
      api_key_label.pack(pady=0)
      api_key_entry = tk.Text(text_screen, height=1, width=65)
      api_key_entry.pack(pady=0)
      api_key_entry.insert(tk.END, key)
      
      texts_left_label = ttk.Label(text_screen, text="Texts left:")
      texts_left_label.place(x=50, y=90)
      texts_left_entry = tk.Text(text_screen, height=1, width=15)
      texts_left_entry.place(x=35, y=120)
      texts_left_entry.insert(tk.END, str(self.texts_remaining))
      texts_left_entry.config(state="disabled") 
      
      
      
      text_screen_label = ttk.Label(text_screen, text="Text:")
      text_screen_label.pack(pady=0)
      text_entry = tk.Text(text_screen, height=20, width=50)
      text_entry.pack(pady=0)
      
      
      text_send_btn = ttk.Button(text_screen, text="Send", command=lambda: self.send_text(api_key_entry, text_entry, texts_left_entry), width=20)
      text_send_btn.pack(pady=7)
      
      
      back_to_main_menu_btn = ttk.Button(text_screen, text="Back to Main Menu", command=lambda: self.show_frame(main_menu), width=30)
      back_to_main_menu_btn.pack(pady=0)
      

      # CSV Viewing Screen (centered)
      csv_view_title = ttk.Label(csv_view_screen, text="Current CSV", font=("Arial", 24))
      csv_view_title.pack(pady=20)
      

      csv_view = tk.Text(csv_view_screen, height=10, width=60)
      csv_view.pack(pady=10)
      
      
      
      refresh_btn = ttk.Button(csv_view_screen, text="Refresh CSV", command=lambda: self.display_csv(csv_view), width=30)
      refresh_btn.pack(pady=10)

      back_to_menu_btn = ttk.Button(csv_view_screen, text="Back to Main Menu", command=lambda: self.show_frame(main_menu), width=30)
      back_to_menu_btn.pack(pady=10)



      # Start the Tkinter loop
      self.switch_frame(main_menu) # Make main menu the starting frame


      root.config(background='white')
      icon = PhotoImage(file="OneFlow_Window_Icon.png")  
      root.iconphoto(False, icon)
      root.mainloop()



key = "553df227ee6b5643502d4fd312f13bc7cd833472vxmQm2Xy3anpwHqi07x33Pric" # Companies will have to use their own API Key.




if __name__ == "__main__":
   application = Home()
   application.gui()

