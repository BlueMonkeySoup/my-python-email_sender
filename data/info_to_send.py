import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime, timedelta
import csv
import pandas as pd
              
class Note():
    
    def __init__(self,root) -> None:
        #Byt till list ifall jag ska skicka till flera.
        self.receiver_email=""
        self.name=""
        self.due_date=""
        self.task=""
        # self.now = datetime.datetime.now()
        self.send_week_before=False
        self.send_three_days_before=False

        self.get_email=False
        self.get_date=False
        self.get_now=False
        self.get_task=False
        self.check_ok=0


        self.root=root
        self.geometry = self.root.geometry("800x800")
        try:
            self.label_header= tk.Label(root,text="Hejsan! här är en automatisk epost skickare")
            self.label_header.pack()

            self.label1= tk.Label(root,text="Epost den ska skickas till")
            self.label1.pack()

            self.entry = tk.Entry(self.root)
            self.entry.pack()

            self.button = tk.Button(self.root, text="lägg till epost", command=self.show_emails)
            self.button.pack()

            self.label = tk.Label(self.root, text="", padx=8, pady=8, font=("Helvetica", 10))
            self.label.pack()


            #Påminelse
            self.label2= tk.Label(root,text="Vad vill du skicka påminelse om?")
            self.label2.pack()

            self.entry2 = tk.Entry(self.root)
            self.entry2.pack()

            self.button2 = tk.Button(self.root, text="påminelse", command=self.show_reminder)
            self.button2.pack()

            self.label2 = tk.Label(self.root, text="", padx=8, pady=8, font=("Helvetica", 10))
            self.label2.pack()


            #Datum 
            self.label3 = tk.Label(root, text="När ska den skickas?")
            self.label3.pack()

            self.cal = Calendar(root, selectmode='day', )
            self.cal.pack()

            #CheckBoxes
            self.var = tk.IntVar()
            c = tk.Checkbutton(self.root, text="Påmin en vecka före", command=self.check_box)
            c.pack()

            self.var2 = tk.IntVar()
            c2 = tk.Checkbutton(self.root, text="Påmin tre dagar före", command=self.check_box2)
            c2.pack()


            button = tk.Button(self.root, text="lägg till", command=self.show_due_date)
            button.pack(padx=10, pady=10)

            self.label3 = tk.Label(self.root, text="", padx=8, pady=8, font=("Helvetica", 10))
            self.label3.pack()


            #Namn
            self.label4= tk.Label(root,text="Från vem?")
            self.label4.pack()

            self.entry4 = tk.Entry(self.root)
            self.entry4.pack()

            self.button4 = tk.Button(self.root, text="lägg till namn", command=self.show_name)
            self.button4.pack()

            self.label4 = tk.Label(self.root, text="", padx=8, pady=8, font=("Helvetica", 10))
            self.label4.pack()

            self.label5 = tk.Label(self.root, text="", padx=8, pady=8, font=("Helvetica", 10))
            self.entry5 = tk.Entry(self.root)

            self.button5 = tk.Button(self.root, text="klar", command=self.check_valid)
            self.button5.pack()

        except Exception:
            self.label6 = tk.Label(self.root, text="Var vänlig och skriv under alla värden", padx=8, pady=8, font=("Helvetica", 10))
            self.label6.pack()
            return "Something went wrong"

    def check_valid(self):
        email_input=self.entry5.get()
        self.label5.config(text=email_input)

        if(self.get_task==True and self.get_email==True and self.get_date==True and self.get_now==True):
            self.send_to_file(self.name,self.receiver_email,self.due_date,self.task)
            self.label7 = tk.Label(self.root, text="Skickades! Du kan nu stänga programet eller skicka till en annan mail :)", padx=8, pady=8, font=("Helvetica", 10))
            self.label7.pack()
        else:
            self.label6 = tk.Label(self.root, text="Var vänlig och skriv under alla värden", padx=8, pady=8, font=("Helvetica", 10))
            self.label6.pack()

    def button_command(self):
        self.send_to_file(self.name, self.receiver_email, self.due_date, self.task)
    
    def show_emails(self):
        email_input=self.entry.get()
        self.label.config(text=email_input)

        self.receiver_email=email_input
        self.get_email=True

    def show_reminder(self):
        reminder_input=self.entry2.get()
        self.label2.config(text=reminder_input)

        self.task=reminder_input
        self.get_task=True

    def show_due_date(self):

        date=self.cal.get_date()
        self.label3.config(text=date)

        self.due_date= date
        self.get_date=True

    def check_box(self):
        self.send_week_before=True
    def check_box2(self):
        self.send_three_days_before=True
        

    def show_name(self):
        name_input=self.entry4.get()
        self.label4.config(text=name_input)

        self.name=name_input
        self.get_now=True

    #Påmin tidigare.  
    def send_to_file_add_days(self,email,name,date,task,add):
        
        # tkCalendar använder month/day/year
        now=date
        new_date=datetime.strptime(now, "%m/%d/%y")
        add_date = new_date+timedelta(days=add)
        add_date=add_date.strftime('%m/%d/%y')
       
    
        return [email, name, add_date, task]
    def send_to_file(self,email,name,date,task):
        try:
            
            data = [email, name, date, task]
            print(date)
                
            if self.send_three_days_before:
                data3=self.send_to_file_add_days(email,name,date,task,3)

            if self.send_week_before:
                data2=self.send_to_file_add_days(email,name,date,task,7)

            with open('"skicka till csv/db"', 'a',encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(data)
                if self.send_three_days_before:
                    writer.writerow(data3)
                if self.send_week_before:
                    writer.writerow(data2)
        except ValueError:
            return "something went wrong. try later"

if __name__=="__main__":

    # make_csv()
    root=tk.Tk()
    start= Note(root)
    root.mainloop()


# def make_csv():
    
#     df = pd.DataFrame(columns=['email', 'name', 'due_date', 'task'])

#     df.to_csv('csv name', index=False)