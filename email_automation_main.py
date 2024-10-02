# E-Mail Automating Script for OneFlow
import smtplib
import subprocess
import datetime as date
import os
import time
import tkinter as tk
from tkinter.filedialog import askopenfilename
import pandas as pd
import sys

# TODO: HANDLE INPUT FOR OPENING A CSV FILES CONTAINING EMAILS, THEN SCRAPING SAID EMAILS INTO BELOW LIST

root = tk.Tk()
root.withdraw()


# Todo, configure login system
name = input("Please enter your name: ")

current_csv = ""

def main_screen():
    os.system('clear')
    print(f"Hello, {name}")
    print("Todays date: " +  date.datetime.now().strftime("%Y-%m-%d"))
    print("_____________________________\n")
    print("Your options:")
    print("1. Send mass e-mail")
    print("2. Display current CSV information")
    print("3. Upload a CSV (always use when starting program)")
    print("4. Exit")


def send_to_main():
   time.sleep(3)
   main()


def main():
    global current_csv

    while True:
        main_screen()
        choice = input(" > ")
        answer = choice.strip()

        if answer == '1':
            os.system('cls')
            subject = input("Enter the e-mail subject: ")
            body = input("")
            send_mass_email(subject, body)
            print("E-mail has been sent!")
            send_to_main()
        elif choice == '2':
            os.system('clear')
            if current_csv != "":
               print("Here is your current CSV information: \n")
               email_frame_path = pd.read_csv(current_csv)
               email_frame = pd.DataFrame(email_frame_path)
               email_frame = email_frame.dropna(how="all")
               print(email_frame)
               send_to_main()
            else:
               print("You have not uploaded a CSV yet!")
               send_to_main()
        elif choice == '3':
            os.system('clear')
            current_csv = askopenfilename()
            print(f"{current_csv} selected!")
            send_to_main()
        elif choice == '4':
            print("Exiting.")
            sys.exit()
            break

        else:
            print("Invalid option. Please try again")



# Store CSV email Info Here.
email_list = ['jmjaques01@gmail.com', 'oneflowautomation@gmail.com']


auth = ('OneFlowAutomation@gmail.com', 'npiv sqhm msnh acgw')

def send_mass_email(subject, body):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.set_debuglevel(1)
    server.starttls()
    server.login(auth[0], auth[1])


    for email in email_list:
        message = f"From: {auth[0]}\nTo: {email}\nSubject: {subject}\n\n{body}"
        try:
            server.sendmail(auth[0], email, message)
        except Exception as e:
            print(f'An error occurred: {e}')


if __name__ == "__main__":
    main()



