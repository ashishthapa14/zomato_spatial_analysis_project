#!/usr/bin/env python
# coding: utf-8

# # Importing Relevant Library:

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#it will ignore conda warnings:
import warnings
warnings.filterwarnings('ignore')


# # Loading CSV File:

# In[2]:


#dealing with na_values:
data= pd.read_csv('D:\\Dataset_ash\\zomato.csv', na_values = '[]')
data


# In[3]:


#checking how many null values in dataset:
data.isnull().sum()


# In[4]:


#checking percentage of missing values:
data.isnull().sum()/data.shape[0]*100


# In[5]:


#droping na values of location for Spatial Analysis:
data.dropna(subset = ['location'] , inplace = True)


# In[6]:


#rechecking how many na_values:
data.isnull().sum()


# In[7]:


#checking length of distinct category
len(data['location'].unique())


# In[8]:


#location for geo spatial analysis 
locations = pd.DataFrame()
locations['Name of city'] = data['location'].unique()


# In[9]:


locations.head(4)


# In[10]:


#!pip install geopy #install this library:


# In[11]:


#importing geopy


# In[12]:


from geopy.geocoders import Nominatim


# In[13]:


geolocator=Nominatim(user_agent="app")


# In[14]:


lat = []
long = []
for location in locations['Name of city']:
    location = geolocator.geocode(location)
    if location  is None: #if location doesnt have latitude or longitude 
        lat.append(np.nan)
        long.append(np.nan)
    else:  #if location has latitude and longitude
        lat.append(location.latitude)
        long.append(location.longitude)


# In[15]:


#printing latitude 
lat


# In[16]:


#printing the longitude:
long


# In[17]:


#in this values of latitude and longitude assigned to a locations dataframe columns:
locations['latitude'] = lat
locations['longitude'] = long


# In[18]:


locations


# # This will create csv file with latitude and longitude:

# In[19]:


locations.to_csv("D:\\Dataset_ash\\zomato_locations.csv",index = False)


# In[20]:


#creating data frame for how many restaurant in specific area 
restaurent = pd.DataFrame(data['location'].value_counts().reset_index())


# In[21]:


restaurent


# # Merging locations and restaurants

# In[22]:


restaurent.columns = ['Name of city' , 'Count']


# In[23]:


restaurent_locations = restaurent.merge(locations,on = 'Name of city' ,how = 'left' ).dropna()
restaurent_locations


# In[24]:


def generateBaseMap(default_location=[12.97, 77.59], default_zoom_start=12):
    base_map = folium.Map(location=default_location, zoom_start=default_zoom_start)
    return base_map


# In[25]:


#install folium for map representation:
#!pip install folium


# In[26]:


import folium
from folium.plugins import HeatMap
basemap=generateBaseMap()


# In[27]:


basemap


# # Heatmap of Bengalore Restuarants

# In[28]:


HeatMap(restaurent_locations[['latitude','longitude','Count']],zoom=20,radius=15).add_to(basemap)


# In[29]:


basemap


# # Geo Analysis: where are the restaurants located in Bengaluru using Marker Cluster?

# In[30]:


from folium.plugins import FastMarkerCluster


# In[31]:


# Plugin: FastMarkerCluster
FastMarkerCluster(restaurent_locations[['latitude','longitude','Count']].values.tolist()).add_to(basemap)
basemap


# Where are the restaurant with average rate?

# In[32]:


data.head(5)


# In[33]:


data['rate'].unique()


# In[34]:


#removing na_values 
data.dropna(axis=0,subset=['rate'],inplace=True)


# In[35]:


data['rate'].unique()


# In[36]:


#removing /n:
def split(x):
    return x.split('/')[0]


# In[37]:


data['rating'] = data['rate'].apply(split)


# In[38]:


data.head()


# In[39]:


data['rating'].unique()


# In[40]:


#replacing NEW and '-' with 0:

data.replace('NEW',0,inplace = True)
data.replace('-',0,inplace = True)


# In[41]:


data.head(20)


# In[42]:


data['rating'].unique()


# In[43]:


#data.groupby(['location'])['rating'].mean() #it will through error: 


# In[44]:


data['rating']  =  pd.to_numeric(data['rating'])


# In[45]:


data['rating'].dtype


# In[46]:


avg_rating = data.groupby(['location'])['rating'].mean().sort_values(ascending=False).values
avg_rating


# In[47]:


loc_ = data.groupby(['location'])['rating'].mean().sort_values(ascending=False).index
loc_


# In[48]:


rating = pd.DataFrame()


# In[49]:


geolocator=Nominatim(user_agent="app")


# In[50]:


lat=[]
lon=[]
for location in loc_:
    location = geolocator.geocode(location)    
    if location is None:
        lat.append(np.nan)
        lon.append(np.nan)
    else:
        lat.append(location.latitude)
        lon.append(location.longitude)


# In[51]:


rating['Latitude'] = lat
rating['Longitude'] = lon
rating['Location'] = loc_
rating['avg_rating'] = avg_rating


# In[52]:


rating


# In[53]:


rating.isnull().sum()


# In[54]:


rating.dropna(inplace = True)


# In[56]:


HeatMap(rating[['Latitude','Longitude','avg_rating']]).add_to(basemap)


# In[57]:


basemap


# # heat map for specific zone:

# In[58]:


data.head()


# In[59]:


data_1= data[data['cuisines']=='North Indian']  #boolean indexing:
data_1.head()


# In[65]:


north_india=data_1.groupby('location')['url'].count().reset_index()
north_india.columns=['Name of city','count']
north_india.head()


# In[66]:


north_india=north_india.merge(locations,on="Name of city",how='left').dropna()


# In[67]:


north_india.head()


# In[69]:


basemap=generateBaseMap()
HeatMap(north_india[['latitude','longitude','count']].values.tolist(),zoom=20,radius=15).add_to(basemap)
basemap


# Automate Above Stuffs, & create for South India, & many other zones
# 

# In[70]:


def Heatmap_Zone(zone):
    data_2=data[data['cuisines']==zone]
    df_zone=data_2.groupby(['location'],as_index=False)['url'].agg('count')
    df_zone.columns=['Name of city','count']
    df_zone=df_zone.merge(locations,on="Name of city",how='left').dropna()
    basemap=generateBaseMap()
    HeatMap(df_zone[['latitude','longitude','count']].values.tolist(),zoom=20,radius=15).add_to(basemap)
    return basemap


# In[71]:


data['cuisines'].unique()


# In[72]:


Heatmap_Zone('South Indian')


# In[ ]:




