import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from dotenv import load_dotenv


PORT = 587
EMAIL_SERVER = "smtp-mail.outlook.com"


class SendAuto():

    def __init__(self) -> None:
        self.current_dir=os.getcwd()
        self.env_file="new_sender/.env"

        self.join_file=os.path.join(self.current_dir,self.env_file)
        load_dotenv(self.join_file)
        self.get_email= os.getenv("EMAIL")
        self.get_password= os.getenv("PASSWORD")
    

    def send_email(self,subject,receiver_email,task,due_date,name):
        msg=EmailMessage()
        msg["Subject"]=subject
        msg["From"]=formataddr(("Påminnelse ",f"{task}"))
        msg["To"]=receiver_email
        msg["BCC"]=self.get_email
    
        msg.set_content(
        f"""\
        ///////

        Hejsan!
        Du har fått en påminnelse om {task} från{name} som ska bli klar den {due_date}
        Hoppas påminnelsen var till nytta!

        Ha det bra!
    
        ///////
        """

        )
        msg.add_alternative(
        f"""\
        <html>
        <body>
            <p>/////////</p>

            <p>Hejsan!</p>
            <p>Du har fått en påminnelse om<strong> {task} från{name} som ska bli klar den {due_date}</strong></p>
            <p>Hoppas påminnelsen var till nytta!</p>
            
            <p>Ha det bra!</p>
            <p>/////////</p>
        </body>
        </html>
            """,
        subtype="html",
        )

        with smtplib.SMTP(EMAIL_SERVER,PORT)as server:
            server.starttls()
            server.login(self.get_email,self.get_password)
            server.sendmail(self.get_email,receiver_email,msg.as_string())


if __name__=="__main__":
    init=SendAuto()
    init.send_email()
