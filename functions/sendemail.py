import smtplib
from email.mime.text import MIMEText
import pickle
from datetime import datetime
import os
from dotenv import load_dotenv
load_dotenv(dotenv_path="config\.env")

subject = "Do you like ass?"
body = "Reply with y/n"
sender = "adri2007900@gmail.com"
recipients = ["jose.minecraft.x@gmail.com", "evjebergadrianhiim@gmail.com"]
password = os.getenv("GOOGLE_PASSWORD")

def main(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
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
    main(subject, body, sender, recipients, password)