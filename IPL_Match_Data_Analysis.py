#!/usr/bin/env python
# coding: utf-8

# In[37]:


import numpy as nm
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)


# In[27]:


match_data=pd.read_csv("F:/Data_Analyst/Pyton_project/IPL Matches 2008-2020.csv",parse_dates=['date'], dayfirst=True)
ball_data=pd.read_csv("F:/Data_Analyst/Pyton_project/IPL Ball-by-Ball 2008-2020.csv")


# In[25]:


match_data.head()


# In[10]:


ball_data.head()


# In[11]:


match_data.isnull().sum()


# In[12]:


ball_data.isnull().sum()


# In[13]:


match_data.shape #shape store the count of column and rows


# In[14]:


match_data.shape[0]#store count of rows


# In[15]:


match_data.shape[1]#store count of column


# In[16]:


ball_data.shape


# In[17]:


ball_data.shape[0]


# In[18]:


ball_data.shape[1]


# In[19]:


match_data.columns# it shows the columnname


# In[20]:


ball_data.columns


# In[21]:


print("Match Played So far:",match_data.shape[0])
print("\nCities Of matches:",match_data["city"].unique())
print("\nParticipated Teams:",match_data["team1"].unique())


# In[28]:


match_data['Season'] =pd.DatetimeIndex(match_data['date']).year
match_data.head()


# In[31]:


match_per_season=match_data.groupby(['Season'])['id'].count().reset_index().rename(columns={'id':'Matches'})
match_per_season


# In[44]:


sns.countplot(match_data['Season'])
plt.xticks(rotation=45,fontsize=10)
plt.xticks(fontsize=10)
plt.xlabel('Season',fontsize=10)
plt.ylabel('Count',fontsize=10)
plt.title('Total matches played in each season',fontsize=12 ,fontweight='bold')


# In[45]:


season_data=match_data[['id','Season']].merge(ball_data,left_on='id',right_on='id',how='left').drop('id',axis=1)
season_data.head()


# In[60]:


season=season_data.groupby(['Season'])['total_runs'].sum().reset_index()
p=season.set_index(['Season'])
ax=plt.axes()
ax.set(facecolor='lightgray')

sns.lineplot(data=p,palette='magma')
plt.title("Total runs in each season",fontsize=12 ,fontweight='bold')
plt.show()


# In[64]:


runs_per_season=pd.concat([match_per_season,season.iloc[:,1]],axis=1)
runs_per_season["Runs Scored Per Match"]=runs_per_season['total_runs']/runs_per_season['Matches']
runs_per_season.set_index('Season',inplace=True)
runs_per_season


# In[74]:


toss=match_data['toss_winner'].value_counts()
ax=plt.axes()
ax.set(facecolor='lightgray')
sns.set(rc={'figure.figsize':(15,10)},style='darkgrid')
ax.set_title("No. of tosses win by each team:",fontsize=15 ,fontweight='bold')
sns.barplot(y=toss.index,x=toss,orient='h',palette='magma',saturation=1)
plt.xlabel('# No of tosses win',fontsize=12,fontweight='bold')
plt.ylabel('Teams',fontsize=12,fontweight='bold')
plt.show()


# In[77]:


ax=plt.axes()
ax.set(facecolor='lightgray')
sns.countplot(x='Season',hue='toss_decision',data=match_data,palette='magma',saturation=1)
plt.xticks(rotation=90,fontsize=10)
plt.xticks(fontsize=15)
plt.xlabel('\nSeason',fontsize=15)
plt.ylabel('Count',fontsize=15)
plt.title('Toss Dicision Across Season',fontsize=15 ,fontweight='bold')
plt.show()


# In[82]:


print("Result Of matches:\n",match_data['result'].value_counts())


# In[90]:


print("Best stadium for chossing field first:\n",match_data.venue[match_data.result!='runs'].mode())


# In[92]:


print("Best stadium for chossing batting first:\n",match_data.venue[match_data.result!='wickets'].mode())


# In[93]:


print("Stadium with no draw  matches:\n",match_data.venue[match_data.result!='tie'].mode())


# In[94]:


print("Lucky Stadium(Toss winner=Match Winner):\n",match_data.venue[match_data.toss_winner=='Mumbai Indians'][match_data.winner=='Mumbai Indians'].mode())


# In[95]:


print("The Best chasing team:\n",match_data.winner[match_data.result!='runs'].mode())


# In[96]:


print("The Best chasing team:\n",match_data.winner[match_data.result!='wickets'].mode())


# In[98]:


toss=match_data['toss_winner']==match_data['winner']
plt.figure(figsize=(10,5))
sns.countplot(toss)
plt.show()


# In[99]:


plt.figure(figsize=(10,5))
sns.countplot(match_data.toss_decision[match_data.toss_winner==match_data.winner])
plt.show()


# In[105]:


player=(ball_data['batsman']=='G Gambhir')
df_gambir=ball_data[player]
df_gambir.head()


# In[106]:


player=(ball_data['batsman']=='RG Sharma')
df_sharma=ball_data[player]
df_sharma.head()


# In[107]:


df_sharma['dismissal_kind'].value_counts().plot.pie(autopct='%1.1f%%',shadow=True,rotatelabels=True)
plt.title('Dismissal Kind',fontsize=15 ,fontweight='bold')
plt.show()


# In[113]:


def count(df_sharma,runs):
    return len(df_sharma[df_sharma['batsman_runs']==runs])*runs


# In[114]:


print("Runs scored from 1's:",count(df_sharma,1))
print("Runs scored from 2's:",count(df_sharma,2))
print("Runs scored from 3's:",count(df_sharma,3))
print("Runs scored from 4's:",count(df_sharma,4))
print("Runs scored from 6's:",count(df_sharma,6))


# In[115]:


match_data[match_data['result_margin']==match_data['result_margin'].max()]


# In[117]:


runs=ball_data.groupby(['batsman'])['batsman_runs'].sum().reset_index()
runs.columns=['Batsman','runs']
y=runs.sort_values(by='runs',ascending=False).head(10).reset_index().drop('index',axis=1)
y


# In[118]:


ax=plt.axes()
ax.set(facecolor='lightgray')
sns.barplot(x=y['Batsman'],y=y['runs'],data=match_data,palette='magma',saturation=1)
plt.xticks(rotation=90,fontsize=10)
plt.xticks(fontsize=10)
plt.xlabel('\nPlayers',fontsize=10)
plt.ylabel('Total Runs',fontsize=10)
plt.title('Top 10 Run scorer in IPL',fontsize=15 ,fontweight='bold')


# In[122]:


ax=plt.axes()
ax.set(facecolor='black')
match_data.player_of_match.value_counts()[:10].plot(kind='bar')
plt.xlabel('\nPlayers',fontsize=10)
plt.ylabel('Conts',fontsize=10)
plt.title('Highest MOM Award Winners',fontsize=15 ,fontweight='bold')


# In[ ]:




