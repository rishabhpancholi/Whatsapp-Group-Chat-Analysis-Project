import re
import pandas as pd
def preprocess(data):
    pattern = '\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s\w{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M\u202f%p - ')

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns={'user_message'}, inplace=True)
    df['year'] = df['message_date'].dt.year
    df['month'] = df['message_date'].dt.month_name()
    df.rename(columns={'message_date': 'date'}, inplace=True)
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['month_num'] = df['date'].dt.month
    df['onlydate'] = df['date'].dt.date
    df['dayname']=df['date'].dt.day_name()

    period = []
    for hour in df['hour']:
        if hour == 23:
            period.append(str(hour) + "-00")
        elif hour == 0:
            period.append("00-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df