#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime, warnings, scipy 
import pandas as pd
import numpy as np
import pyarrow as pa
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import ConnectionPatch
from collections import OrderedDict
from matplotlib.gridspec import GridSpec
#from mpl_toolkits.basemap import Basemap
from sklearn import metrics, linear_model
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_val_score, cross_val_predict
from scipy.optimize import curve_fit
plt.rcParams["patch.force_edgecolor"] = True
plt.style.use('fivethirtyeight')
mpl.rc('patch', edgecolor = 'dimgray', linewidth=1)
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "last_expr"
pd.options.display.max_columns = 50
get_ipython().run_line_magic('matplotlib', 'inline')
warnings.filterwarnings("ignore")
spark.conf.set("spark.sql.execution.arrow.enabled", "true")
spark.conf.set("spark.sql.execution.arrow.fallback.enabled", "true")


# In[2]:


df=spark.read.csv("file:///Users/lavidhaliwal/Downloads/BigData_data/airOT200501.csv",inferSchema=True,header=True)


# In[3]:


#df.show(1)


# In[4]:


#df=df.drop('YEAR','MONTH','DAY_OF_MONTH','DAY_OF_WEEK','TAIL_NUM','FL_NUM','_c44','ORIGIN_STATE_ABR','DEST_STATE_ABR','ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID','CRS_DEP_TIME','DEP_DEL15','DEP_DELAY_GROUP','CRS_ARR_TIME','ARR_DEL15','CANCELLATION_CODE','DIVERTED','CRS_ELAPSED_TIME','ARR_DELAY_GROUP','DISTANCE_GROUP','FLIGHTS','WEATHER_DELAY','NAS_DELAY','SECURITY_DELAY','LATE_AIRCRAFT_DELAY',
#          'TAXI_OUT','WHEELS_OFF','WHEELS_ON','TAXI_IN','CANCELLED','AIR_TIME','DISTANCE','DEP_DELAY','ARR_DELAY','ARR_DELAY_NEW')
df=df.drop('FL_DATE','DAY_OF_WEEK','TAIL_NUM','FL_NUM','_c44','ORIGIN_STATE_ABR','DEST_STATE_ABR','ORIGIN_AIRPORT_ID','DEST_AIRPORT_ID','CRS_DEP_TIME','DEP_DEL15','DEP_DELAY_GROUP','CRS_ARR_TIME','ARR_DEL15','CANCELLATION_CODE','DIVERTED','CRS_ELAPSED_TIME','ARR_DELAY_GROUP','DISTANCE_GROUP','FLIGHTS','WEATHER_DELAY','NAS_DELAY','SECURITY_DELAY','LATE_AIRCRAFT_DELAY',
          'TAXI_OUT','WHEELS_OFF','WHEELS_ON','TAXI_IN','CANCELLED','AIR_TIME','DISTANCE','ARR_DELAY_NEW','DEP_DELAY_NEW')




# In[5]:


df.show(4)
#df.write.csv('file:///Users/lavidhaliwal/mycsv.csv')


# In[6]:


#df.summary()
from pyspark.sql.functions import col
from pyspark.sql.functions import sum as fsum
y=df.select(*(fsum(col(c).isNull().cast("int")).alias(c) for c in df.columns))
y1=df.count()


# In[7]:


z=y.collect()


# In[8]:


dep_d=z[0].DEP_DELAY
print(dep_d*100/y1)
print(y1)


# In[9]:


df1=df.na.drop(subset=['DEP_TIME','DEP_DELAY','ARR_TIME','ACTUAL_ELAPSED_TIME','ARR_DELAY'])
df1=df1.fillna(0,subset=['CARRIER_DELAY'])


# In[10]:


#df.summary()
df1.select(*(fsum(col(c).isNull().cast("int")).alias(c) for c in df.columns)).show()


# In[11]:


df1.registerTempTable("data")


# In[12]:


df2=spark.sql("select count(*) as count,avg(DEP_DELAY)as mean,max(DEP_DELAY) as maximum,UNIQUE_CARRIER from data group by UNIQUE_CARRIER")
df2.registerTempTable("data1")
df2.show()


# In[13]:


pd1=df1.toPandas()


# In[14]:



# delay grouping
delay_type = lambda x:((0,1)[x > 5],2)[x > 45]
pd1['DELAY_LEVEL'] = pd1['CARRIER_DELAY'].apply(delay_type)
#
fig = plt.figure(1, figsize=(10,7))
ax = sns.countplot(y="UNIQUE_CARRIER", hue='DELAY_LEVEL', data=pd1)
# legends
L = plt.legend()
L.get_texts()[0].set_text('on time (t < 5 min)')
L.get_texts()[1].set_text('small delay (5 < t < 45 min)')
L.get_texts()[2].set_text('large delay (t > 45 min)')
plt.show()


# In[15]:


pd2=pd1[pd1.DELAY_LEVEL>0]
pd3=pd2.groupby('UNIQUE_CARRIER').mean()
pd3.sort_values(by='CARRIER_DELAY')


# In[16]:


ranking=pd3.rank()['CARRIER_DELAY']
ranking.sort_values()


# In[17]:


ranking=pd3.rank()['CARRIER_DELAY']
pd.concat([pd3,ranking],join='inner')
pd4=pd1.join(ranking,on='UNIQUE_CARRIER',lsuffix='D')
pd4=pd4.rename(columns={'CARRIER_DELAY':'RANK','CARRIER_DELAYD':'CARR_DELAY','DAY_OF_MONTH':'DAY'})


# In[ ]:





# In[18]:


pd4=pd4.drop(columns='DELAY_LEVEL')


# In[ ]:





# In[19]:


#set path to where you want to saVE YOUR FILE
pd4.to_csv(r'/Users/lavidhaliwal/Downloads/111ranking.csv',index=False)


# In[20]:


pd4['DATE'] = pd.to_datetime(pd4[['YEAR','MONTH', 'DAY']])


# In[21]:


pd4.index=pd4.DATE


# In[22]:


pd4=pd4.drop(columns=['YEAR','MONTH','DAY','DATE'])


# In[23]:


#pd4.to_csv(r'/Users/lavidhaliwal/rankingcsv.csv')
#df.to_csv(r'C:\Users\Admin\Desktop\file3.csv', index=False) 


# In[24]:


#############VISUALIZARION#######


# In[ ]:





# In[25]:


#pd4.to_csv(r'/Users/lavidhaliwal/Downloads/newranking.csv',index=False)


# In[26]:



# statistical parameters fn
def get_stats(group):
    return {'min': group.min(), 'max': group.max(),
            'count': group.count(), 'mean': group.mean()}
#_______________________________________________________________
# Creation of a dataframe with statitical infos on each airline:
global_stats = pd4['DEP_DELAY'].groupby(pd4['UNIQUE_CARRIER']).apply(get_stats).unstack()
global_stats = global_stats.sort_values('count')
global_stats


# In[27]:


font = {'family' : 'normal', 'weight' : 'bold', 'size'   : 15}
mpl.rc('font', **font)
import matplotlib.patches as mpatches

#
colors = ['royalblue', 'grey', 'wheat', 'c', 'firebrick', 'seagreen', 'lightskyblue',
          'lightcoral', 'yellowgreen', 'gold', 'tomato', 'violet', 'aquamarine', 'chartreuse']
#
fig = plt.figure(1, figsize=(16,15))
gs=GridSpec(2,2)             
ax1=fig.add_subplot(gs[0,0]) 
ax2=fig.add_subplot(gs[0,1]) 
ax3=fig.add_subplot(gs[1,:]) 
#------------------------------
# Pie chart 1: no of flights
#------------------------------
labels = [s for s in  global_stats.index]
sizes  = global_stats['count'].values
explode = [0.3 if sizes[i] < 20000 else 0.0 for i in range(len(global_stats))]
patches, texts, autotexts = ax1.pie(sizes, explode = explode,
                                labels=labels,colors=colors,  autopct='%1.0f%%',
                                shadow=False, startangle=0)
for i in range(len(global_stats)): 
    texts[i].set_fontsize(14)
ax1.axis('equal')
ax1.set_title('% of flights per company', bbox={'facecolor':'midnightblue', 'pad':5},
              color = 'w',fontsize=18)
#_______________________________________________

#----------------------------------------
# Pie chart 2
#----------------------------------------
sizes  = global_stats['mean'].values
sizes  = [max(s,0) for s in sizes]
explode = [0.0 if sizes[i] < 20000 else 0.01 for i in range(len(global_stats))]
patches, texts, autotexts = ax2.pie(sizes, explode = explode, labels = labels,
                                colors = colors, shadow=False, startangle=0,
                                autopct = lambda p :  '{:.0f}'.format(p * sum(sizes) / 100))
for i in range(len(global_stats)): 
    texts[i].set_fontsize(14)
ax2.axis('equal')
ax2.set_title('Mean delay at origin', bbox={'facecolor':'midnightblue', 'pad':5},
              color='w', fontsize=18)
#------------------------------------------------------
# striplot with all the values reported for the delays
#___________________________________________________________________

colors = ['firebrick', 'gold', 'lightcoral', 'aquamarine', 'c', 'yellowgreen', 'grey',
          'seagreen', 'tomato', 'violet', 'wheat', 'chartreuse', 'lightskyblue', 'royalblue']
#___________________________________________________________________
ax3 = sns.stripplot(y="UNIQUE_CARRIER", x="CARR_DELAY", size = 4, palette = colors,
                    data=pd4, linewidth = 0.5,  jitter=True)
plt.setp(ax3.get_xticklabels(), fontsize=14)
plt.setp(ax3.get_yticklabels(), fontsize=14)
ax3.set_xticklabels(['{:2.0f}h{:2.0f}m'.format(*[int(y) for y in divmod(x,60)])
                         for x in ax3.get_xticks()])
plt.xlabel('Carrier delay', fontsize=18, bbox={'facecolor':'midnightblue', 'pad':5},
           color='w', labelpad=20)
ax3.yaxis.label.set_visible(False)
#________________________
plt.tight_layout(w_pad=3) 


# In[28]:


#pd4.head()


# In[29]:


mpl.rcParams.update(mpl.rcParamsDefault)
mpl.rcParams['hatch.linewidth'] = 2.0  

fig = plt.figure(1, figsize=(11,6))
ax = sns.barplot(x="DEP_DELAY", y="UNIQUE_CARRIER", data=pd4, color="lightskyblue", ci=None)
ax = sns.barplot(x="ARR_DELAY", y="UNIQUE_CARRIER", data=pd4, color="r", hatch = '///',
                 alpha = 0.0, ci=None)
#labels = [abbr_companies[item.get_text()] for item in ax.get_yticklabels()]
#ax.set_yticklabels(labels)
ax.yaxis.label.set_visible(False)
plt.xlabel('Mean delay [min] (@departure: blue, @arrival: hatch lines)',
           fontsize=14, weight = 'bold', labelpad=10);


# In[30]:


airport_mean_delays = pd.DataFrame(pd.Series(pd4['ORIGIN'].unique()))
airport_mean_delays.set_index(0, drop = True, inplace = True)

for carrier in global_stats.index:
    pd5 = pd4[pd4['UNIQUE_CARRIER'] == carrier]
    test = pd5['DEP_DELAY'].groupby(pd5['ORIGIN']).apply(get_stats).unstack()
    airport_mean_delays[carrier] = test.loc[:, 'mean'] 


# In[31]:


len(airport_mean_delays)
airport_mean_delays


# In[32]:


sns.set(context="paper")
fig = plt.figure(1, figsize=(6,6))

ax = fig.add_subplot(1,2,1)
subset = airport_mean_delays.iloc[:25,:10]
#
mask = subset.isnull()
sns.heatmap(subset, linewidths=0.01, cmap="Accent", mask=mask, vmin = 0, vmax = 35)
plt.setp(ax.get_xticklabels(), fontsize=10, rotation = 85) ;
ax.yaxis.label.set_visible(False)

ax = fig.add_subplot(1,2,2)    
subset = airport_mean_delays.iloc[25:50,10:19]
#subset = subset.rename(index = identify_airport)
fig.text(0.5, 1.02, "Delays: impact of the origin airport", ha='center', fontsize = 18)
mask = subset.isnull()
sns.heatmap(subset, linewidths=0.01, cmap="Accent", mask=mask, vmin = 0, vmax = 35)
plt.setp(ax.get_xticklabels(), fontsize=10, rotation = 85) ;
ax.yaxis.label.set_visible(False)

plt.tight_layout()


# In[33]:


#### MAP VISUALIZATION USING BASEMAP ######


# In[ ]:


#give own path to the airports file
airports = pd.read_csv("gdrive/My Drive/airports.csv")
identify_airport = airports.set_index('IATA_CODE')['CITY'].to_dict()
latitude_airport = airports.set_index('IATA_CODE')['LATITUDE'].to_dict()
longitude_airport = airports.set_index('IATA_CODE')['LONGITUDE'].to_dict()


# In[34]:


def make_map(df, carrier, long_min, long_max, lat_min, lat_max):
    fig=plt.figure(figsize=(7,3))
    ax=fig.add_axes([0.,0.,1.,1.])
    m = Basemap(resolution='i',llcrnrlon=long_min, urcrnrlon=long_max,
                  llcrnrlat=lat_min, urcrnrlat=lat_max, lat_0=0, lon_0=0,)
    df2 = df[df['UNIQUE_CARRIER'] == carrier]
    count_trajectories = df2.groupby(['ORIGIN', 'DEST']).size()
    count_trajectories.sort_values(inplace = True)
    
    for (origin, dest), s in count_trajectories.iteritems():
        nylat,   nylon = latitude_airport[origin], longitude_airport[origin]
        m.plot(nylon, nylat, marker='o', markersize = 10, markeredgewidth = 1,
                   color = 'seagreen', markeredgecolor='k')

    for (origin, dest), s in count_trajectories.iteritems():
        nylat,   nylon = latitude_airport[origin], longitude_airport[origin]
        lonlat, lonlon = latitude_airport[dest], longitude_airport[dest]
        if pd.isnull(nylat) or pd.isnull(nylon) or                 pd.isnull(lonlat) or pd.isnull(lonlon): continue
        if s < 100:
            m.drawgreatcircle(nylon, nylat, lonlon, lonlat, linewidth=0.5, color='b',
                             label = '< 100')
        elif s < 200:
            m.drawgreatcircle(nylon, nylat, lonlon, lonlat, linewidth=2, color='r',
                             label = '100 <.< 200')
        else:
            m.drawgreatcircle(nylon, nylat, lonlon, lonlat, linewidth=2, color='gold',
                              label = '> 200')    
    #_____________________________________________
    # remove duplicate labels and set their order
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    key_order = ('< 100', '100 <.< 200', '> 200')                
    new_label = OrderedDict()
    for key in key_order:
        if key not in by_label.keys(): continue
        new_label[key] = by_label[key]
    plt.legend(new_label.values(), new_label.keys(), loc = 'best', prop= {'size':8},
               title='flights per month', facecolor = 'palegreen', 
               shadow = True, frameon = True, framealpha = 1)    
    m.drawcoastlines()
    m.fillcontinents()
    ax.set_title('flights for %s'%(carrier))


# In[35]:





# In[ ]:


coord = dict()
coord['AA'] = [-165, -60, 10, 55]
coord['AS'] = [-165, -60, 10, 55]
coord['HA'] = [-165, -60, 10, 55]
coord['FL'] = [-165, -60, 10, 55]
coord['B6'] = [-165, -60, 10, 55]
coord['US'] = [-165, -60, 10, 55]
for carrier in ['AA', 'AS', 'HA','B6','FL','US']: 
    make_map(pd4, carrier, *coord[carrier])


# In[ ]:




