# -*- coding: utf-8 -*-
"""
Created on Mon Nov 13 11:29:04 2023

@author: Ravit
"""

import pandas as pd
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt

# In[]
def extract_year_from_string(date_string):
    """
    Extracts the year from a given datetime string.

    :param date_string: A string representing a datetime.
    :return: The year as an integer.
    """
    try:
        # Attempting to parse the datetime string
        date_obj = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f000')
        return date_obj.year
    except ValueError as e:
        # Return an error message if the parsing fails
        # return f"Error: {str(e)}"
        return 0
# In[]

df = pd.read_csv(r"C:\Users\Ravit\Downloads\f8f.csv")

extract_year_from_string('1971-01-01 00:00:00.000000000')
nan_index = df[df['year'].isna()]

# In[]
df['year'] = df['year'].fillna('')
df['year'] = df['year'].convert_dtypes()

# In[]
copy_df = df.copy()
copy_df['year'] = df['year'].apply(extract_year_from_string)

copy_df = copy_df[copy_df['year']>1960]
copy_df = copy_df[copy_df['year']<2024]

# In[]
#new_df = df[df['year']>2000]

portion_df = copy_df[['doi', 'year', 'datePublished', 'documentType_type', 'fullText']]

# drop all missing years
portion_df = portion_df[portion_df['year']!=0]

portion_df['year'].value_counts()
# In[]

d_res = {}
d_missing_res = {}

#get all unique years

uniq_years = portion_df['year'].unique()

for year in uniq_years:
    year_articles = portion_df[portion_df['year']==year]
    try:
        d_res[year] = len(year_articles) - year_articles['doi'].value_counts()['None']
        d_missing_res[year] = year_articles['doi'].value_counts()['None']
    except:
        d_res[year] = len(year_articles)
        d_missing_res[year] = 0
        
# In[]

# Plotting with contrasting colors
plt.bar(d_res.keys(), d_res.values(), color='blue', alpha=0.7, label='Existing DOI')
plt.bar(d_missing_res.keys(), d_missing_res.values(), color='pink', alpha=0.7, label='Missing DOI')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Number of DOIs and Missing DOIs per Year')

# Adding legend
plt.legend()

# Show plot
plt.show()
# In[]
#count from the missing doi values how many are with publish dates

missin_doi_df = portion_df[portion_df['doi'] == 'None']
exist_doi_df = portion_df[portion_df['doi'] != 'None']

no_pub_dates_miss = len(missin_doi_df[missin_doi_df['datePublished'].isna()]) 
no_pub_dates_exist = len(exist_doi_df[exist_doi_df['datePublished'].isna()]) 

old_dates_missin = len(missin_doi_df[missin_doi_df['year'] < 1990]) 
old_dates_exist = len(exist_doi_df[exist_doi_df['year'] < 1990]) 

no_text_missin = len(missin_doi_df[missin_doi_df['fullText']=='None']) 
no_text_exist = len(exist_doi_df[exist_doi_df['fullText']=='None']) 

doctype_missin_count = missin_doi_df['documentType_type'].value_counts()
doctype_exist_count = exist_doi_df['documentType_type'].value_counts()

# Plot missing publication dates 
plt.bar([0], [no_pub_dates_exist], color = 'blue', alpha=0.5, label='Existing DOI')
plt.bar([1], [no_pub_dates_miss], color = 'pink', alpha=0.5, label='Misstng DOI')


# Adding labels and title (if needed)
plt.ylabel("Missing Publication year Counts")


# Set axis ranges here
plt.xlim(-0.5, 1.5)  # Set the limit for the x-axis
plt.ylim(0, 20000)   # Set the limit for the y-axis

# Adding a legend
plt.legend()

# Display the plot
plt.show()

#plot count of old dates
plt.bar([0], [old_dates_exist], color = 'blue', alpha=0.5, label='Existing DOI')
plt.bar([1], [old_dates_missin], color = 'pink', alpha=0.5, label='Misstng DOI')


# Adding labels and title (if needed)
plt.ylabel("Dates before 1990's Count")


# Set axis ranges here
plt.xlim(-0.5, 1.5)  # Set the limit for the x-axis
plt.ylim(0, 4000)   # Set the limit for the y-axis

# Adding a legend
plt.legend()

# Display the plot
plt.show()


#plot missing text
plt.bar([0], [no_text_exist], color = 'blue', alpha=0.5, label='Existing DOI')
plt.bar([1], [no_text_missin], color = 'pink', alpha=0.5, label='Misstng DOI')

# Adding labels and title (if needed)
plt.ylabel("Missing texts")

# In[]
# plot documents types count
#get x axis keys
keys = doctype_exist_count.keys()
n_groups = len(keys)

# Create an array with the position of each bar along the x-axis
index = np.arange(n_groups)

bar_width = 0.35  # Width of the bars

# Plot the bars
plt.bar(index, doctype_exist_count.values, bar_width, color='blue', alpha=0.7, label='Existing DOI')
plt.bar(index + bar_width, doctype_missin_count.values, bar_width, color='pink', alpha=0.7, label='Missing DOI')

# Add labels and title
plt.xlabel('Document type')
plt.ylabel('Count')
plt.title('Count by Document Type and DOI Status')

# Specify the location and labels of the x-ticks
plt.xticks(index + bar_width / 2, keys)

# Adding legend
plt.legend()

# Show plot
plt.show()

# In[]
# Plot missing dois again after removing old articles and rows with missing texts. 
copy_df = copy_df[copy_df['year']>1990] 
copy_df = copy_df[copy_df['fullText']!='None']
copy_df = copy_df[copy_df['documentType_type'].isin(['None', 'research'])]

d_res = {}
d_missing_res = {}

#get all unique years

uniq_years = copy_df['year'].unique()

for year in uniq_years:
    year_articles = copy_df[copy_df['year']==year]
    try:
        d_res[year] = len(year_articles) - year_articles['doi'].value_counts()['None']
        d_missing_res[year] = year_articles['doi'].value_counts()['None']
    except:
        d_res[year] = len(year_articles)
        d_missing_res[year] = 0
        

# Plotting with contrasting colors
plt.bar(d_res.keys(), d_res.values(), color='blue', alpha=0.7, label='Existing DOI')
plt.bar(d_missing_res.keys(), d_missing_res.values(), color='pink', alpha=0.7, label='Missing DOI')

# Add labels and title
plt.xlabel('Year')
plt.ylabel('Count')
plt.title('Number of DOIs and Missing DOIs per Year')

# Adding legend
plt.legend()

# Show plot
plt.show()

# In[]

copy_df.to_csv(r'C:\Users\Ravit\Documents\rnd\horizon_scanning_lab\SQL_database\docs\core_parsed_files\20Nov2023_filtered_articles_for_doi_retreival.csv', index=False)
