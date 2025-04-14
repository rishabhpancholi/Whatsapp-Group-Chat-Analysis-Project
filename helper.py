# Imports for analysis and visualization
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import string
import emoji

# Initialize URL extractor
extractor = URLExtract()

# Function to fetch overall stats
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]  # Filter for selected user

    num_messages = df.shape[0]  # Total messages
    words = []
    for message in df['message']:
        words.extend(message.split(" "))  # Count all words

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))  # Extract links

    # Count media messages
    num_media_msg = df[df['message'] == '<Media omitted>\n'].shape[0]

    return num_messages, len(words), num_media_msg, len(links)

# Function to fetch top active users
def fetch_most_busy_users(df):
    df = df[df['user'] != 'group notification']  # Remove system messages
    x = df['user'].value_counts().head()  # Top 5 users by message count

    # Calculate % contribution
    df = round(100 * df['user'].value_counts() / df.shape[0], 2)\
         .reset_index().rename(columns={'user': 'User', 'count': 'Percentage'})\
         .head()

    return x, df

# Function to generate word cloud
def create_word_cloud(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Filter out system messages and media
    df = df[df['user'] != 'group notification']
    df = df[df['message'] != '<Media omitted>\n']
    df = df[df['message'] != 'This message was deleted\n']

    words = []
    for message in df['message']:
        # Remove punctuation and convert to lowercase
        message_cleaned = message.lower().translate(str.maketrans('', '', string.punctuation))
        for word in message_cleaned.split():
            if word not in stop_words and word.isalpha():
                words.append(word)

    # Generate word cloud from cleaned words
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='green')
    most_common_df = pd.DataFrame(Counter(words).most_common(), columns=['Word', 'Count'])
    df_wc = wc.generate(most_common_df['Word'].str.cat(sep=" "))
    return df_wc

# Function to return most common words
def most_common_words(selected_user, df):
    with open('stop_hinglish.txt', 'r') as f:
        stop_words = f.read().splitlines()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Exclude media and system messages
    temp = df[df['user'] != 'group notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'This message was deleted\n']

    words = []
    for message in temp['message']:
        message_cleaned = message.lower().translate(str.maketrans('', '', string.punctuation))
        for word in message_cleaned.split():
            if word not in stop_words and word.isalpha():
                words.append(word)

    # Return top 20 common words
    most_common_df = pd.DataFrame(Counter(words).most_common(20), columns=['Word', 'Count'])
    return most_common_df

# Function to extract most used emojis
def most_common_emojis(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([m for m in message if m in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])
    return emoji_df

# Function to create monthly message timeline
def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    # Create custom time format (e.g., Jan-2022)
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline

# Function to create daily timeline
def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby('onlydate').count()['message'].reset_index()
    return timeline

# Weekly activity mapping (e.g., Monday, Tuesday, ...)
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['dayname'].value_counts().reset_index()

# Monthly activity mapping (e.g., Jan, Feb, ...)
def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    return df['month'].value_counts().reset_index()

# Function to generate heatmap of activity (days vs time periods)
def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Pivot table to count messages per (day, time period) pair
    user_heatmap = df.pivot_table(index='dayname', columns='period',
                                  values='message', aggfunc='count').fillna(0)
    return user_heatmap
