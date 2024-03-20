from datetime import datetime,date
import pandas as pd
from send import SendAuto
import os
from dotenv import load_dotenv

email=SendAuto()

class CheckToSend():
    
    def __init__(self) -> None:
        self.current_dir=os.getcwd()
        self.env_file="new_sender/.env"
        self.join_file=os.path.join(self.current_dir,self.env_file)
        load_dotenv(self.join_file)
        self.url= os.getenv("USER_TABLE")
        

    def load_df(self):
        df = pd.read_csv(self.url,usecols=["due_date"],encoding="utf-8")
        return df

    def query_data_and_send_email(self,df):
        present =date.today()
        email_count=0
        for _,row in df.iterrows():
            due_date_str = row["due_date"]
            due_date = datetime.strptime(due_date_str, '%m/%d/%y').date()
            if (present >= due_date):
                email.send_email(
                    subject ="Påminelse",
                    receiver_email= row["email"],
                    name= row["name"],
                    task=row["task"],
                    due_date=due_date
                )
                email_count+=1
        print("sent!")
        return f"email sent:{email_count}"

if __name__=="__main__":
    init= CheckToSend()
    df=init.load_df()
    result = init.query_data_and_send_email(df)
    print(result)