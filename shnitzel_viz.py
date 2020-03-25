import pandas as pd 
import json
from pandas.io.json import json_normalize
import seaborn as sns
import matplotlib.pyplot as plt

infile = open('./raddas.json')
data = json.load(infile)

df1 = json_normalize(data['seasons'],record_path='season_one')
df2 = json_normalize(data['seasons'],record_path='season_two')
df3 = json_normalize(data['seasons'],record_path='season_three')

s1 = df1.T.reset_index().rename(columns={'index':'segment',0:'raddas'})
s2 = df2.T.reset_index().rename(columns={'index':'segment',0:'raddas'})
s3 = df3.T.reset_index().rename(columns={'index':'segment',0:'raddas'})

s1.insert(loc=0,column='season',allow_duplicates=True,value='season_one')
s2.insert(loc=0,column='season',allow_duplicates=True,value='season_two')
s3.insert(loc=0,column='season',allow_duplicates=True,value='season_three')


first = s1.append(s2)
total = first.append(s3).reset_index()
total.insert(loc=2,column='episode',value=0)

for i in range(0,len(total)):
    total['episode'].loc[i] = total.loc[i].segment.split('.')[0].split('p')[1]
    total['segment'].loc[i] = total.loc[i].segment.split('.')[1]

total = total.drop(columns='index')
by_episode = total.groupby('episode').agg('sum').reset_index()

df = by_episode.astype(int)
df.sort_values(['episode'])

by_season = total.groupby('season').agg('sum').reset_index()
by_season['season'] = by_season['season'].replace({'season_one':1,'season_two':2,'season_three':3})
by_season.sort_values(['season'])

# plt.figure(figsize=(10,10))
# ax = sns.barplot(x='season', y='raddas',data=by_season)
# ax.set_xticklabels(ax.get_xticklabels(),fontsize=7)
# ax.set_title('Raddas By Season')
# plt.tight_layout()
# for p in ax.patches:
    # count = int(p.get_height())
    # x = p.get_x() + p.get_width()/2 - 0.02
    # y = p.get_y() + p.get_height() + 0.5
    # ax.annotate(count,(x,y))
# figure = ax.get_figure()
# figure.savefig('seasons.png')

# plt.figure(figsize=(10,10))
# ax = sns.barplot(x='episode', y='raddas',data=df)
# ax.set_xticklabels(ax.get_xticklabels(),fontsize=7,linespacing=2)
# ax.set_title('Raddas By Episode')
# plt.tight_layout()
# for p in ax.patches:
#     count = int(p.get_height())
#     if count < 10:
#         x = p.get_x() + p.get_width()/4
#         y = p.get_y() + p.get_height() + 0.5
#     elif count >= 10 and count < 100:
#         x = p.get_x() + p.get_width()/8 - 0.1
#         y = p.get_y() + p.get_height() + 0.5
#     elif count >= 100: 
#         x = p.get_x() + p.get_width()/8 - 0.5
#         y = p.get_y() + p.get_height() + 0.5
#     ax.annotate(count,(x,y))
# figure = ax.get_figure()
# figure.savefig('episodes.png')

# plt.figure(figsize=(10,10))
# ax = sns.barplot(x='segment',y='raddas',data=total)
# ax.set_xticklabels(ax.get_xticklabels(),fontsize=7,rotation=90)
# ax.set_title('Raddas By Segment')
# plt.tight_layout()
# figure = ax.get_figure()
# figure.savefig('segments.png')
