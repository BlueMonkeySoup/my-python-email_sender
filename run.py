from data.info_to_send import Note
from data.send_to_cloud import CheckToSend
import tkinter as tk
import datetime
import azure.functions as func
import logging

cloud_send=CheckToSend

#Öppnar en tkinter så det går lättare att skicka. Måste ha tk calendar för att kunna köra. pip i tkcalendar
def send_reminder():
    
    root=tk.Tk()
    Note(root)
    root.mainloop()

send_reminder()

# kör automatisk till cloud och skickar när tiden stämmer
def send_info():

    cloud_send=CheckToSend()
    df = cloud_send.load_df()
    result= cloud_send.query_data_and_send_email(df)
    print(result)
    return "running on a schedule"


def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

   
    send_info()
