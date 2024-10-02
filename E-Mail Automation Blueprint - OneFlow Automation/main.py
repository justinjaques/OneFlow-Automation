# E-Mail Automating Script for OneFlow
import smtplib

# TODO: HANDLE INPUT FOR OPENING A CSV FILES CONTAINING EMAILS, THEN SCRAPING SAID EMAILS INTO BELOW LIST
    

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
        
            
            
send_mass_email("Testing the OneFlow automation system.", "Joy economy!")
        