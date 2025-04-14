import re
import pandas as pd

def preprocess(data):
    # Regular expression pattern to match WhatsApp datetime format (e.g. 12/02/24, 9:20 PM - )
    pattern = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s\w{2}\s-\s'

    # Split messages using the pattern (dates will be separators)
    messages = re.split(pattern, data)[1:]  # First element is empty if data starts with a date
    dates = re.findall(pattern, data)  # Extract all datetime strings using the same pattern

    # Create initial DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert the message_date column to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M\u202f%p - ')

    # Separate usernames from messages
    users = []
    messages = []
    for message in df['user_message']:
        # Split on the first colon followed by a space to separate user and message
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # If message is sent by a user
            users.append(entry[1])
            messages.append(entry[2])
        else:  # If it's a system message (e.g., user joined, user left, etc.)
            users.append('group notification')
            messages.append(entry[0])

    # Add separated columns to DataFrame
    df['user'] = users
    df['message'] = messages
    df.drop(columns={'user_message'}, inplace=True)

    # Extract date and time features
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['onlydate'] = df['date'].dt.date
    df['dayname'] = df['date'].dt.day_name()

    # Create time period column (e.g., 23-00, 00-1, 1-2, ...)
    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append("23-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df
