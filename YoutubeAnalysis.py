import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import Dataset
df = pd.read_csv('GlobalYouTubeStatistics.csv', encoding='unicode escape')

# Data Understanding

print(df.head())
print(df.info())
print(df.shape)
print(df.isnull().sum())

'''Data Cleaning'''

print(df.duplicated().sum())

# Finding number of unique rows
print(df[-df.duplicated()].shape[0])

# Handling Missing Values in Dataset

NaNnumerical = df.select_dtypes(include=['float64','int64']).columns
NaNcategorical = df.select_dtypes(include='object').columns
df[NaNnumerical] = df[NaNnumerical].fillna(0)
df[NaNcategorical] = df[NaNcategorical].fillna('Others')
print(df.isnull().sum())

# Overview on Numerical columns
print(df.describe())

# Converting Subscribers, Video, Views and Population, urban population in millions

df['subscribers'] = (df['subscribers'] / 1000000).round(2)
df['video views'] = (df['video views'] / 1000000).round(2)
df['Population'] = (df['Population'] / 1000000).round(2)
df['Urban_population'] = (df['Urban_population'] / 1000000).round(2)
print(df[['subscribers','video views','Population','Urban_population']].tail())

''' Data Manipulation '''

# Rename of columns
df.rename(columns={'Unemployment rate':'Unemployment rate(%)'}, inplace=True)

# Display the modified DataFrame
# print(df.columns())
print(df.head())

# Filter the row where the videos views are not equale to 0
video = df[df['video views'] != 0]
print(video)

# Create a new column in dataset name "AverageYearEarning"
df["AverageYearEarning"] = (df['lowest_yearly_earnings'] + df['highest_yearly_earnings'])
df["AverageYearEarning"] = (df["AverageYearEarning"] / 1000000).round(2)
print(df)

''' Data Analysis And Visualization '''

# Company wants to run advertisement in the country with maximum subscribe

# Find out which country has most subscribers

countrySubscribers = df.groupby(['Country'])['subscribers'].sum().sort_values(ascending=False).head()
print(countrySubscribers)

plt.pie(countrySubscribers.values, labels=countrySubscribers.index, autopct="%0.1f%%")
plt.title('Country-Wise Subscribers Distribution ')
plt.show()

'''
The distrubution of country-wise subscribers reveals that the Unites States has the highest percentage 
of subscribers at 43.9% and India has 25.8%, Unknow regions at 17.5%., Brazil has 7.3% and UK has 5.5%
'''

# Find out top 10 Indian Channels having most subscribers

indianCountry = df[df['Country'] == 'India']
top_10_Channel = indianCountry[['Youtuber','subscribers']].sort_values(by='subscribers',ascending=False).head(10)
print(top_10_Channel)

plt.figure(figsize=(10,8))
plt.bar(top_10_Channel['Youtuber'],top_10_Channel['subscribers'])
plt.xticks(rotation=45,ha='right')
plt.title('Top 10 YouTube Channel by Subscribers')
plt.xlabel('YouTuber Channels')
plt.ylabel('Subscribers')
plt.xticks(rotation=45,ha='right')
plt.show()

''' T-Series leads with the highest YouTube subscribers in India. Followed by SET India and Zee Music Company '''

# Find out percentage of each Category out of Total subscribers

category = df.groupby(['category'])['subscribers'].sum()
totalSubscribers = df['subscribers'].sum()
subscriberPercentage = (category / totalSubscribers) * 100
subscriberPercentage = subscriberPercentage.reset_index().sort_values(by='subscribers',ascending=True)
print(subscriberPercentage)

plt.figure(figsize=(13,6))
plt.barh(subscriberPercentage['category'],subscriberPercentage['subscribers'])
for index, value in enumerate(subscriberPercentage['subscribers']):
    plt.text(value,index,f'{value:.2f}%', va='center')

plt.title('Category-Wise Distribution of Subscribers')
plt.xlabel('Percentage Of Subscribers')
plt.ylabel('Category')
plt.show()

'''
Music and Entertaiment categories have the highest percentage of subscribers, indicating a strong 
audience preference of these  genre
'''

# Give list of top 10 YouTubers by highest average yearly earnings for giving gift hampers

highestYouTuber = df[['Youtuber','AverageYearEarning']].sort_values(by='AverageYearEarning',ascending=False).head(10)
print(highestYouTuber)

plt.figure(figsize=(10,8))
plt.bar(highestYouTuber['Youtuber'],highestYouTuber['AverageYearEarning'])

for index, value in enumerate(highestYouTuber['AverageYearEarning']):
    plt.text(value, index,f'${value:.2f}')

plt.xlabel('YouTuber')
plt.ylabel('Average Yearly Earning')
plt.title('Top 10 YouTubers by Average Yearly Earnings')
plt.xticks(rotation=45,ha='right')
plt.show()

''' 
KIMPRO tops the list with the highest average yearly earning, followed by Boom and T-Series, indicating varied 
revenue streams and successfull monetization strategies
'''

# Correlation of Video Views, Yearly earning ,Subscriber, Uploads

corrVYS = df[['video views','highest_yearly_earnings','subscribers','uploads']]
corr = corrVYS.corr()
print(corr)

plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True)
plt.show()

'''
KIMPRO tops the list with the highest average yearly earning, followed by Boom and T-Series, indicating varied 
revenue streams and successful monetization strategies
'''

# Find out which category of channel are most viewed. Give Top 5 Channel type with their percentage

channelCategories = df.groupby(['channel_type'])['video views'].sum().sort_values(ascending=False).reset_index().head()
print(channelCategories)

plt.pie(channelCategories['video views'],labels=channelCategories['channel_type'], autopct='%0.1f%%')
plt.show()

'''
The pie chart visually represents the distribution of Top 5 channel type in the countries by video views, revealing
the dominant channel types in these video views regions.
'''

# Which country earns the most from YouTube. Give list of top 10 countries

countriesList = df.groupby(['Country'])['highest_monthly_earnings'].max().sort_values(ascending=False).head(10)
print(countriesList)

plt.figure(figsize=(10,8))
sns.barplot(x=countriesList.values,y=countriesList.index, hue=countriesList.index, palette='viridis', legend=False)
plt.show()

''' The top earners are not concentrated in a specific region, indicating a global distribution of successful 
YouTube content creators '''

# Video Views Distribution by Channel Category

plt.figure(figsize=(12,6))
sns.barplot(x='category', y='video views',data=df,errorbar=None,palette='viridis',legend=False,hue='category')
plt.xticks(rotation=45,ha='right')
plt.xlabel('category')
plt.ylabel('video views')
plt.show()

'''The bar plot illustrates the distribution of video views across different content categories, highlighting 
variations in popularity'''


# Make code of relation of Subscribers and Video Views

plt.figure(figsize=(10,6))
plt.scatter(df['subscribers'],df['video views'],alpha=0.7)
plt.title('Relation between Subscribers and Video Views')
plt.xlabel('Subscribers')
plt.ylabel('Video Views')
plt.grid()
plt.show()

'''As the number of subscribers increases, there is a tendency for video views to also increase '''

# Find the category with the maximum occurrence in India

indiaOccur = df[df['Country'] == 'India']
top_5_Categories = indiaOccur['category'].value_counts().reset_index().head()
print(top_5_Categories)

plt.figure(figsize=(10,6))
sns.barplot(x='category',y='count',data=top_5_Categories, palette='viridis',hue='category',legend=False)

plt.title('Top 5 Categories in India by Number of Channel')
plt.xlabel('Category')
plt.ylabel('Number of Channel')
plt.xticks(rotation=45,ha='right')
plt.show()


'''
The bar plot reveals that the majority of YouTube channels in India fall under the "Entertainment" category, indicating a
significationn interest in divers entertainment content content among  the Indian audience. While Entertainment is dominate,
the presence of other categories. The presence of the "Education" category in the top 5 indicates a growing interest in 
educational content, presenting an opportunity for content creators to focus on providing educational videos.
'''



