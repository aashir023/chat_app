import re
import pandas as pd

def preprocess(data):
    # Define the pattern for date and time
    pattern = r'\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s[ap]m\s-'
    
    # Split messages and extract dates
    messages = re.split(pattern, data)[1:]  # Exclude the first empty part
    dates = re.findall(pattern, data)
    
    # Create a DataFrame
    df = pd.DataFrame({'User_message': messages, 'Message_date': dates})
    df['Message_date'] = pd.to_datetime(df['Message_date'], format='%d/%m/%Y, %I:%M %p -')
    
    # Rename the column
    df.rename(columns={'Message_date': 'Date'}, inplace=True)
    
    # Initialize lists for users and messages
    users = []
    msgs = []
    
    # Process each message
    for message in df['User_message']:
        match = re.match(r'([^:]+):\s(.*)', message)
        if match:
            users.append(match.group(1))
            msgs.append(match.group(2))
        else:
            users.append('group notification')
            msgs.append(message)  
    
    # Assign lists to DataFrame
    df['Users'] = users
    df['Message'] = msgs
    
    # Remove '<Media omitted>' from the 'Message' column
    df['Message'] = df['Message'].str.replace('<Media omitted>', '', regex=False)
    
    # Drop the original User_message column
    df.drop(columns=['User_message'], inplace=True)
    
    # Extract date components
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Day'] = df['Date'].dt.day_name()
    df['Hour'] = df['Date'].dt.hour
    df['Minute'] = df['Date'].dt.minute
    df['Month_num']=df['Date'].dt.month
    df['Only_date']=df['Date'].dt.date
    df['Day_name']=df['Date'].dt.day_name()
    period=[]
    for hour in df[['Day_name', 'Hour']]['Hour']:
        if hour==23:
            period.append(str(hour)+"-"+str('00'))
        elif hour==0:
            period.append(str('00')+"-"+str(hour+1))
        else:
            period.append(str(hour)+"-"+str(hour+1))
    df['Period']=period
    return df
