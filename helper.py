from pygments.styles.dracula import green
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import string
import emoji
extractor=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split(" "))

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    num_media_msg = df[df['message']=='<Media omitted>\n'].shape[0]
    return num_messages, len(words), num_media_msg, len(links)

def fetch_most_busy_users(df):
    df=df[df['user']!='group notification']
    x = df['user'].value_counts().head()
    df = round(100*df['user'].value_counts()/df.shape[0],2).reset_index().rename(columns={'user':'User','count':'Percentage'}).head()
    return x,df

def create_word_cloud(selected_user,df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    df = df[df['user'] != 'group notification']
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['message'] != 'This message was deleted\n']

    words = []
    for message in df['message']:
        message_cleaned = message.lower().translate(str.maketrans('', '', string.punctuation))
        for word in message_cleaned.split():
            if word not in stop_words and word.isalpha():  # Ensure it's not a stop word or number
                words.append(word)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='green')
    most_common_df = pd.DataFrame(Counter(words).most_common(len(Counter(words))), columns=['Word','Count'])
    df_wc= wc.generate(most_common_df['Word'].str.cat(sep=" "))
    return df_wc

def most_common_words(selected_user,df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']


    words = []
    for message in temp['message']:
        message_cleaned = message.lower().translate(str.maketrans('', '', string.punctuation))
        for word in message_cleaned.split():
            if word not in stop_words and word.isalpha():  # Ensure it's not a stop word or number
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])
    return most_common_df

def most_common_emojis(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis=[]
    for message in df['message']:
        emojis.extend([m for m in message if m in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))),columns=['Emoji','Count'])
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby('onlydate').count()['message'].reset_index()
    return timeline

def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['dayname'].value_counts().reset_index()

def month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts().reset_index()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    user_heatmap = df.pivot_table(index='dayname',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap