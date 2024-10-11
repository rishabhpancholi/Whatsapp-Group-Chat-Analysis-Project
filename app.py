import streamlit as st
import seaborn as sns
import preprocessor, helper
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")

def centered_header_and_title(header, title):
    st.markdown(f"<h4 style='text-align: center;'>{header}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; color:green;'>{title}</h2>", unsafe_allow_html=True)

st.sidebar.image('https://imgs.search.brave.com/xdiWkrjs8ThqbjCN2LKvPQ77rqMrwClqru82iNKKTaY/rs:fit:500:0:0:0/g:ce/aHR0cHM6Ly90My5m/dGNkbi5uZXQvanBn/LzA1LzAxLzcxLzc4/LzM2MF9GXzUwMTcx/Nzg3OV83UldlY3Mz/VEwwelZKSlhkN1FB/V3puMzlaMkNiRXI0/Qy5qcGc')
st.sidebar.title("Whatsapp Group Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    user_list = df['user'].unique().tolist()
    user_list.remove("group notification")
    user_list.sort()
    user_list.insert(0, "Overall")
    selected_user = st.sidebar.selectbox("Analyse with respect to", user_list)

    if st.sidebar.button("Analyse"):

        num_messages, words, num_media_msg,links= helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            centered_header_and_title("Total Messages", num_messages)
        with col2:
            centered_header_and_title("Total Words", words)
        with col3:
            centered_header_and_title("Media Shared", num_media_msg)
        with col4:
            centered_header_and_title("Links Shared", links)
        st.header("")
        st.markdown("<hr style='border:2px solid green;'>", unsafe_allow_html=True)

        st.title("Message Count Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax= plt.subplots()
        ax = plt.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical',fontsize = 5)
        st.pyplot(fig)

        st.header("")
        st.markdown("<hr style='border:2px solid green;'>", unsafe_allow_html=True)

        st.title("Message Count Daily Timeline")
        timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax = plt.plot(timeline['onlydate'], timeline['message'], color='green')
        plt.xticks(rotation='vertical', fontsize=5)
        st.pyplot(fig)

        st.header("")
        st.markdown("<hr style='border:2px solid green;'>", unsafe_allow_html=True)

        st.title("Activity Maps")
        col1,col2=st.columns(2)

        with col1:
            busy_day=helper.week_activity_map(selected_user, df)
            fig,ax=plt.subplots()
            plt.xticks(rotation='vertical')

            ax.bar(busy_day['dayname'],busy_day['count'],color='green')
            st.pyplot(fig)

        with col2:
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            plt.xticks(rotation='vertical')

            ax.bar(busy_month['month'], busy_month['count'], color='green')
            st.pyplot(fig)

        st.header("")
        st.markdown("<hr style='border:2px solid green;'>", unsafe_allow_html=True)

        st.title("Weekly Activity Heatmap")

        fig, ax = plt.subplots()
        user_heatmap = helper.activity_heatmap(selected_user, df)
        sns.heatmap(user_heatmap, ax=ax, cmap='Greens')

        st.pyplot(fig)

        st.header("")
        st.markdown("<hr style='border:2px solid green;'>", unsafe_allow_html=True)


        if selected_user == 'Overall':
            st.title('Top 5 Busy Users')
            x,new_df= helper.fetch_most_busy_users(df)
            fig,ax=plt.subplots()
            plt.xticks(rotation='vertical')

            col1,col2=st.columns(2)

            with col1:
                ax.bar(x.index, x.values,color='green')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

            st.header("")
            st.markdown("<hr style='border:2px solid green;'>", unsafe_allow_html=True)

        st.title('WordCloud')
        df_wc=helper.create_word_cloud(selected_user, df)
        fig,ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.header("")
        st.markdown("<hr style='border:2px solid green;'>", unsafe_allow_html=True)

        st.title('Most Common Words')
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        plt.xticks(rotation='vertical')
        ax.barh(most_common_df['Word'],most_common_df['Count'],color='green')

        col1, col2 = st.columns(2)

        with col1:
            st.pyplot(fig)
        with col2:
            st.dataframe(most_common_df)

        st.header("")
        st.markdown("<hr style='border:2px solid green;'>", unsafe_allow_html=True)

        st.title('Most Common Emojis')
        most_common_df = helper.most_common_emojis(selected_user, df)



        col1,col2= st.columns(2)

        top_most_common=most_common_df.head(5)

        emoji_list=[]
        for emoji in top_most_common['Emoji']:
            emoji_list.append(emoji)

        emoji_count_list=[]
        for count in top_most_common['Count']:
            emoji_count_list.append(count)

        plt.rcParams['font.family'] = 'Segoe UI Emoji'

        with col1:
            st.dataframe(most_common_df)
        with col2:
            fig = px.pie(values=emoji_count_list, names=emoji_list)
            st.plotly_chart(fig)

        st.header("")
        st.markdown("<hr style='border:2px solid green;'>", unsafe_allow_html=True)
