import smtplib
from email.mime.text import MIMEText
import pickle
from datetime import datetime
import os
import sys
from dotenv import load_dotenv
load_dotenv(dotenv_path="config\.env")

sender = "adri2007900@gmail.com"
password = os.getenv("GOOGLE_PASSWORD")

def main(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join([recipients])
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())

    # Generate a unique filename using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"storage\\emails\\email_{timestamp}.epkg"

    with open(filename, "wb") as file:
        pickle.dump(msg, file)

    #! This is how you would decode the message
    #with open(filename, "rb") as file:
    #    decoded_msg = pickle.load(file)
    #    print("Decoded message:", decoded_msg)

    print(f"Message regarding {subject} sent to {recipients} and saved...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        recipients = sys.argv[1]
        subject = sys.argv[2]
        body = sys.argv[3]
        main(subject, body, sender, recipients, password)
    else:
        print("Please relevant information for sending email.")