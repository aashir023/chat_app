import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title('Whatsapp Chat Analyzer')
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocess(data)
    #st.dataframe(df)

    # Fetch unique users
    user_list = df['Users'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0, 'Overall')

    selected_user = st.sidebar.selectbox('Show Analysis wrt', user_list)
    numOfMessages, words, numOfMedia, links = helper.fetch_stats(selected_user, df)
    
    # This block will execute only when the 'Show Analysis' button is clicked
    if st.sidebar.button('Show Analysis'):
        st.title('Top Statistics')
        # Displaying the statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header('Total Messages')
            st.subheader(numOfMessages)
        with col2:
            st.header('Total Words')
            st.subheader(words)
        with col3:
            st.header('Media Shared')
            st.subheader(numOfMedia)
        with col4:
            st.header('Links Shared')
            st.subheader(links)

        #monthly timeline
        st.header('Monthly Timeline')
        timeline=helper.monthly_timeline(selected_user, df)
        fig, ax=plt.subplots()
        plt.plot(timeline['Time'], timeline['Message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.header('Daily Timeline')
        daily_timeline=helper.daily_timeline(selected_user, df)
        fig, ax=plt.subplots()
        plt.plot(daily_timeline['Only_date'], daily_timeline['Message'], color='red')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #acivity map
        st.header('Activity Map')
        col1,col2=st.columns(2)
        with col1:
            st.subheader('Most Busy Day')
            busy_day=helper.week_activity(selected_user,df)
            fig, ax=plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color='red')
            ax.set_xticklabels(busy_day.index, rotation=90)
            st.pyplot(fig)
        with col2:
            st.subheader('Most Busy Month')
            busy_month=helper.month_activity(selected_user, df)
            fig, ax=plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='red')
            ax.set_xticklabels(busy_month.index, rotation=90)
            st.pyplot(fig)

        st.header('Weekly Activity Heatmap')
        heatmap_df=helper.activity_heatmap(selected_user, df)
        fig, ax=plt.subplots()
        ax=sns.heatmap(heatmap_df)
        st.pyplot(fig)
        

        
        # Most active users in group
        if selected_user == 'Overall':
            st.header('Most Active Users')
            X, new_df = helper.mostActiveUsers(df)
            fig, ax = plt.subplots()  # Define ax here
            col1, col2 = st.columns(2)
            with col1:
                ax.bar(X.index, X.values, color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df.head())

        # WordCloud
        st.header('WordCloud')
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc, interpolation='bilinear')
        st.pyplot(fig)

        # Most common 25 words used
        most_common_df = helper.most_common_words(selected_user, df)

        fig, ax=plt.subplots()
        ax.barh(most_common_df[0], most_common_df[1],color='red')
        plt.xticks(rotation='vertical')
        st.header('Most Common Words')
        st.pyplot(fig)

        #emoji analysis
        emoji_df=helper.emoji_helper(selected_user, df)
        st.header("Emoji Analysis")
        col1, col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig, ax=plt.subplots()
            ax.pie(emoji_df['Times used'].head(), labels=emoji_df['Emoji'].head(), autopct='%.02f')
            st.pyplot(fig)
        


            
