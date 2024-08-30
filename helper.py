from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extractor=URLExtract()
def fetch_stats(selected_user, df):
    if selected_user!= 'Overall':
       df=df[df['Users']==selected_user]

    #fetch number of messages
    numOfMessages=df.shape[0]

    #fetch number of total words
    words=[]
    for message in df['Message']:
        words.extend(message.split())

    #fetch number of media shared
    numOfMedia=df[df['Message']=='<Media omitted>'].shape[0]

    #fetch number of links
    links=[]
    for message in df['Message']:
        links.extend(extractor.find_urls(message))

    return numOfMessages,len(words),numOfMedia,len(links)

#fetch 5 most active users in group
def mostActiveUsers(df):
    x=df['Users'].value_counts().head()
    df=round((df['Users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'count':'Percentage','Users':'Name' })
    return x,df

def create_wordcloud(selected_user, df):
    f=open('stopwords.txt','r')
    stop_words=f.read()
    if selected_user!='Overall':
        df=df[df['Users']==selected_user]
        #to remove group notification
    temp=df[df['Users']!='group notification']
    def remove_stopwords(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    wc=WordCloud(width=500, height=500,min_font_size=10,background_color='white')
    temp['Message']=temp['Message'].apply(remove_stopwords)
    df_wc=wc.generate(temp['Message'].str.cat(sep=' '))
    return df_wc.to_array()

def most_common_words(selected_user,df):
    f=open('stopwords.txt','r')
    stop_words=f.read()
    if selected_user!='Overall':
        df=df[df['Users']==selected_user]
        #to remove group notification
    temp=df[df['Users']!='group notification']
       #to remove stopwords
    words=[]
    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
            #words.extend(message.split())
    most_common_df=pd.DataFrame(Counter(words).most_common(25))
    return most_common_df

def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
    print("Extracted emojis:", emojis)  # Debugging line
    emoji_counts = Counter(emojis)
    emoji_df = pd.DataFrame(emoji_counts.most_common(len(emoji_counts)), columns=['Emoji', 'Times used'])
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['Users']==selected_user]
    timeline=df.groupby(['Year','Month', 'Month_num']).count()['Message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i]+'-'+str(timeline['Year'][i]))
        if len(time) == len(timeline):
            timeline['Time'] = time
        else:
            print(f"Length mismatch: time has {len(time)} elements, but timeline has {len(timeline)} rows.")

    return timeline

def daily_timeline(selected_user, df):
    if selected_user!='Overall':
        df=df[df['Users']==selected_user]
    daily_timeline=df.groupby('Only_date').count()['Message'].reset_index()
    return daily_timeline

def week_activity(selected_user, df):
    if selected_user!='Overall':
        df=df[df['Users']==selected_user]
    return df['Day_name'].value_counts()

def month_activity(selected_user, df):
    if selected_user!='Overall':
        df=df[df['Users']==selected_user]
    return df['Month'].value_counts()

def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['Users'] == selected_user]
    
    # Pivot table to create the heatmap data
    heatmap_df = df.pivot_table(index='Day_name', columns='Period', values='Message', aggfunc='count').fillna(0)
    
    # Debugging prints
    print("Heatmap DataFrame Shape:", heatmap_df.shape)
    
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    heatmap_df = heatmap_df.reindex(days_order)
    return heatmap_df
