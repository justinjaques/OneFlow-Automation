# Text automation.
# Justin Jaques
import requests
import pandas as pd
import datetime as date
import os
import time


text_csv = pd.read_csv("AutoText.csv")
user_frame = pd.DataFrame(text_csv)
user_frame.columns = user_frame.columns.str.strip()
people = {}

for index, row in user_frame.iterrows():
    name = row['Name']
    phone_number = row['Phone']
    people[name] = phone_number
 



key = "553df227ee6b5643502d4fd312f13bc7cd833472vxmQm2Xy3anpwHqi07x33Pric"

name = input("Enter your name: ")

def main_screen():
    os.system('cls')
    print(f"Hello, {name}")
    print("Todays date: " +  date.datetime.now().strftime("%Y-%m-%d"))
    print("_____________________________\n")
    print("Your options:")
    print("1. Send global text message")
    print("2. Send individual text message")
    print("3. Display CSV information")
    print("4. Upload new CSV")
    print("5. Exit")


def send_to_main():
    time.sleep(2)
    main()


def send_global_message(message):
    for name, phone_number in people.items():
        try:
            resp = requests.post('https://textbelt.com/text', {
                'phone': phone_number,  
                'message': message,  
                'key': key
                
            })
            print(f"Message sent to {name}: {resp.json()}")
    
            print(resp.json())
        except Exception as e:
            print(e)
            

def send_individual_message(name, message):
    resp = requests.post('https://textbelt.com/text', {
        'phone': people[name],  
        'message': message,  
        'key': key
    })
    print(f"Message sent to {name}: {resp.json()}")
    
    
def main():
    while True:
        main_screen()
        choice = input(" > ")
        answer = choice.strip()
        
        if answer == '1':
            os.system('cls')
            message = input("Enter your global message and press enter: ")
            send_global_message(message)
        elif choice == '2':
            os.system('cls')
            name = input("Enter the name of the person: ")
            message = input("Enter your message: ")
            send_individual_message(name, message)
        elif choice == '3':
            os.system('cls')
            print(user_frame)
            print("Type menu to return to the menu.")
            choice_3 = input(" > ")
            answer = choice_3.strip()
            
            if choice_3 == 'menu' or choice_3 == 'Menu':
                send_to_main()
            else:
                print("Unknown command.")
                send_to_main()
        elif choice == '4':
            os.system('cls')
            print("Implement CSV uploading functionality")
            send_to_main()
        elif choice == '5':
            print("Exiting.")
            break
        else:
            print("Invalid option. Please try again")
            
    
if __name__ == "__main__":
    main()