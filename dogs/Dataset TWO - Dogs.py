#!/usr/bin/env python
# coding: utf-8

# # Homework 7, Part Two: A dataset about dogs.
# 
# Data from [a FOIL request to New York City](https://www.muckrock.com/foi/new-york-city-17/pet-licensing-data-for-new-york-city-23826/)

# ## Do your importing and your setup

# In[1]:


import pandas as pd


# ## Read in the file `NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx` and look at the first five rows

# In[2]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx")


# In[3]:


df.head(5)


# ## How many rows do you have in the data? What are the column types?
# 
# If there are more than 30,000 rows in your dataset, go back and only read in the first 30,000.
# 
# * *Tip: there's an option with `.read_csv` to only read in a certain number of rows*

# In[4]:


df.shape


# In[5]:


df.dtypes


# ## Describe the dataset in words. What is each row? List two column titles along with what each of those columns means.
# 
# For example: “Each row is an animal in the zoo. `is_reptile` is whether the animal is a reptile or not”

# In[6]:


# Each row is a dog
# "Animal Name" is the name of the dog
# "Animal Gender" is the gender of the dog


# # Your thoughts
# 
# Think of four questions you could ask this dataset. **Don't ask them**, just write them down in the cell below. Feel free to use either Markdown or Python comments.

# In[7]:


# 1 - What's the most common breed of dog?
# 2 - What's the average age of a dogs?
# 3 - How many dogs are trained?
# 4 - What percent is male and what percent is female?


# # Looking at some dogs

# ## What are the most popular (primary) breeds of dogs? Graph the top 10.

# In[8]:


df["Primary Breed"].value_counts().head(10).sort_values(ascending=True).plot(kind="barh")


# ## "Unknown" is a terrible breed! Graph the top 10 breeds that are NOT Unknown
# 
# * *Tip: Maybe you want to go back to your `.read_csv` and use `na_values=`? Maybe not? Up to you!*

# In[46]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", na_values="Unknown")


# In[57]:


df["Primary Breed"].value_counts().head(10).sort_values(ascending=True).plot(kind="barh")


# ## What are the most popular dog names?

# In[60]:


df = pd.read_excel("NYC_Dog_Licenses_Current_as_of_4-28-2016.xlsx", na_values="UNKNOWN")


# In[61]:


df["Animal Name"].value_counts().head(10)


# ## Do any dogs have your name? How many dogs are named "Max," and how many are named "Maxwell"?

# In[11]:


len(df[df["Animal Name"] == "Andrew"])


# In[12]:


len(df[df["Animal Name"] == "Max"])


# In[13]:


len(df[df["Animal Name"] == "Maxwell"])


# ## What percentage of dogs are guard dogs?

# In[14]:


(len(df[df["Guard or Trained"] == "Yes"]) / df.shape[0]) * 100


# ## What are the actual numbers?

# In[15]:


len(df[df["Guard or Trained"] == "Yes"])


# ## Wait... if you add that up, is it the same as your number of rows? Where are the other dogs???? How can we find them??????
# 
# Use your `.head()` to think about it, then you'll do some magic with `.value_counts()`. Think about missing data!

# In[62]:


df["Guard or Trained"]


# In[16]:


len(df[df["Guard or Trained"] == "Yes"]) + len(df[df["Guard or Trained"] == "No"])


# In[17]:


df["Guard or Trained"].value_counts()


# In[18]:


df["Guard or Trained"].value_counts().sum()


# ## Maybe fill in all of those empty "Guard or Trained" columns with "No"? Or as `NaN`? 
# 
# Can we make an assumption either way? Then check your result with another `.value_counts()`

# In[93]:


# df = df.dropna(subset=['Treatment_Date'])
# df.dropna()
# df["Guard or Trained"].head(100).sample(100)
# df["Guard or Trained"].replace("NaN", "No").value_counts()


# ## What are the top dog breeds for guard dogs? 

# In[95]:


import numpy as np


# In[148]:


df[df["Guard or Trained"] == "Yes"]["Primary Breed"].replace("Unknown", np.nan).dropna().value_counts().head(10)


# ## Create a new column called "year" that is the dog's year of birth
# 
# The `Animal Birth` column is a datetime, so you can get the year out of it with the code `df['Animal Birth'].apply(lambda birth: birth.year)`.

# In[83]:


df["year"] = df["Animal Birth"].apply(lambda birth: birth.year)


# ## Calculate a new column called “age” that shows approximately how old the dog is. How old are dogs on average?

# In[22]:


import datetime


# In[23]:


current_year = datetime.datetime.now().year
current_year


# In[89]:


df["age"] = current_year - df["year"]


# In[90]:


df.head(1)


# # Joining data together

# ## Which neighborhood does each dog live in?
# 
# You also have a (terrible) list of NYC neighborhoods in `zipcodes-neighborhoods.csv`. Join these two datasets together, so we know what neighborhood each dog lives in. **Be sure to not read it in as `df`, or else you'll overwrite your dogs dataframe.**

# In[124]:


df_n = pd.read_csv("zipcodes-neighborhoods.csv", na_values="Unknown")


# In[125]:


merged = df.merge(df_n, left_on="Owner Zip Code", right_on="zip")
merged.head(2)


# ## What is the most popular dog name in all parts of the Bronx? How about Brooklyn? The Upper East Side?
# 
# You'll want to do these separately, and filter for each.

# In[179]:


merged[merged["borough"] == "Bronx"]["Animal Name"].mode()


# In[165]:


#### FIX
merged[merged["borough"] == "Brooklyn"]["Animal Name"].value_counts()


# In[182]:


merged[merged["neighborhood"] == "Upper East Side"]["Animal Name"].mode()


# ## What is the most common dog breed in each of the neighborhoods of NYC?
# 
# * *Tip: There are a few ways to do this, and some are awful (see the "top 5 breeds in each borough" question below).*

# In[196]:


merged.groupby("neighborhood")["Primary Breed"].value_counts()


# ## What breed of dogs are the least likely to be spayed? Male or female?
# 
# * *Tip: This has a handful of interpretations, and some are easier than others. Feel free to skip it if you can't figure it out to your satisfaction.*

# In[211]:


merged[merged["Spayed or Neut"] == "Yes"]["Primary Breed"].value_counts().tail(5)


# In[212]:


merged[(merged["Spayed or Neut"] == "Yes") & (merged["Animal Gender"] == "M")]["Primary Breed"].value_counts().tail(5)


# In[213]:


merged[(merged["Spayed or Neut"] == "Yes") & (merged["Animal Gender"] == "F")]["Primary Breed"].value_counts().tail(5)


# ## Make a new column called `monochrome` that is True for any animal that only has black, white or grey as one of its colors. How many animals are monochrome?

# In[45]:


merged["monochrome"] = "True"
merged.head(1)

## SEARCH TWO COLUMNS WITH CONDITIONAL VALUES
df[['Animal Dominant Color','Animal Secondary Color','Animal Third Color']].head(1)
# df[['Animal Dominant Color','Animal Secondary Color','Animal Third Color']] [df['Promoted'] == True]

# Animal Secondary Color
# Animal Third Color

# len(df[df["Animal Dominant Color"] == "BLACK"])
# df[(df["Animal Dominant Color"] == "Black") | (df["Animal Dominant Color"] == "White") | (df["Animal Dominant Color"] == "Grey")]


# ## How many dogs are in each borough? Plot it in a graph.

# In[221]:


# merged.groupby(by="borough").value_counts().hist()


# ## Which borough has the highest number of dogs per-capita?
# 
# You’ll need to merge in `population_boro.csv`

# In[117]:


df_boro = pd.read_csv("boro_population.csv")


# In[118]:


merged = merged.merge(df_boro, left_on="borough", right_on="borough")


# In[113]:


# merged["borough"].value_counts() / merged["population"]


# ## Make a bar graph of the top 5 breeds in each borough.
# 
# How do you groupby and then only take the top X number? You **really** should ask me, because it's kind of crazy.

# In[222]:


merged.head(5)


# In[229]:


merged.groupby("borough")["Primary Breed"].value_counts().hist()


# In[ ]:




