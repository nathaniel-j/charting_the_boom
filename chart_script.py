import pandas as pd
from sodapy import Socrata
import matplotlib.pyplot as plt

# set chart theme
sns.set_theme(context='notebook',
              style='darkgrid',
              palette='deep',
              font='sans-serif',
              font_scale=1.3,
              color_codes=True,
              rc=None)

# set notebook display options
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# turning off warnings
import warnings
warnings.filterwarnings('ignore')

# ----- downloading data set -------

URL ='data.austintexas.gov'

client = Socrata(URL,
                 None,
                 timeout=100) #replace None with my token when I get one

query = """
    select
            permittype,
            work_class,
            housing_units,
            completed_date,
            calendar_year_issued,
            permit_class,
            status_current,
            certificate_of_occupancy
    where
            permittype = "BP"
            and work_class in ("New", "Shell")
            and permit_class in ( 
                                "C- 101 Single Family Houses", 
                                "C- 103 Two Family Bldgs",
                                "C- 104 Three & Four Family Bldgs", 
                                "C- 105 Five or More Family Bldgs", 
                                "C- 106 Mixed Use", 
                                "R- 101 Single Family Houses", 
                                "R- 102 Secondary Apartment",
                                "R- 103 Two Family Bldgs", 
                                "R- 436 Addn to increase housing units" 
)
    limit 
            1000000
            
"""

results = client.get("3syk-w9eu", query=query)

df = pd.DataFrame.from_dict(results)

client.close()

# -------- manipulating the data ------

# turning issue year into integer
df['Calendar Year Issued'] = df['calendar_year_issued'].astype('int')

# turning housing units value into integer
df['housing_units'].fillna(0, inplace=True)
df['Housing Units'] = df['housing_units'].astype('int')

#adding a year complete column

def year_complete(date):
    try:
        date = date.split('-')[0]
        date = int(date)
        return date
    except:
        # to account for NaN values
        return date

df['Year Completed'] = df['completed_date'].apply(year_complete)

# selecting the permits to avoid redundancy & non-residential buildings

# a filter for housing units by permit issue date -- PERMITS ISSUED DF
mask =  (
        (df['status_current'].isin(['Final', 'Active']))
        )
apply_date = df[mask].groupby(['Calendar Year Issued']).sum()

# this is  the df for units by permit issue year
yearly_permit_units = apply_date['Housing Units']

# ---------

# a filter for housing units by completion year -- PERMITS COMPLETED DF
mask =  (
    (df['certificate_of_occupancy']=='Yes') & 
    (df['status_current']=='Final')
        )

final_date = df[mask].groupby(['Year Completed']).sum()

# this is the df for units by completion year
final_permit_units = final_date['Housing Units']

# merging annual permitted and built units into DF with one year column for indexing
housing_data = pd.merge(
    left = yearly_permit_units,
    right = final_permit_units,
    how = 'inner',
    left_on = yearly_permit_units.index,
    right_on = final_permit_units.index
    )

# combined and aggregated dataframe
housing_data.columns = ['year', 'permitted', 'built'] 

# ----- Visualizing the data -------

def build_chart(df):
    """Plot the chart for the housing data df with columns ['year', 'permitted', 'built']"""
    
    plt.figure(figsize=(18,14))
    # units permited per year
    plt.plot(df['year'], df['permitted'], label='Permitted Housing Units', marker='o')
    # units finished per year
    plt.plot(df['year'], df['built'], label='Actual Housing Supply', marker='o')
    plt.legend()
    plt.xlim([1977, 2023])
    plt.title('AUSTIN NEW HOUSING UNITS PERMITS ISSUED & UNITS BUILT')
    plt.xlabel('Year')
    plt.ylabel('# of Housing Units')
    plt.savefig('chart.png', format='png')
    plt.close()

# creating chart and saving to file
build_chart(housing_data)
