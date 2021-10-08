
import pandas as pd 
import requests 
import os
import numpy as np

#######################################################################################
################################## ACQUIRE FUNCTIONS ##################################
#######################################################################################

##################### GERMANY ENERGY FUNCTION #####################

def get_germany_data():
    '''
    This function creates a csv of germany energy data if one does not exist
    if one already exists, it uses the existing csv 
    and brings it into pandas as dataframe
    '''
    if os.path.isfile('opsd_germany_daily.csv'):
        df = pd.read_csv('opsd_germany_daily.csv', index_col=0)
    
    else:
        url = 'https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv'
        df = pd.read_csv(url)
        df.to_csv('opsd_germany_daily.csv')

    return df

############################# ITEMS ACQUIRE FUNCTION #########################

def items_df():
    '''
    This function pulls in items data from the url provided
    and returns all pages in items as a Pandas DataFrame
    '''

    #create an empty items list
    items_list = []
    #grab data from the url
    url = "https://python.zach.lol/api/v1/items"

    #create the response
    response = requests.get(url)
    data = response.json()
    #identify keys desired
    n = data['payload']['max_page']

    #create for loop to pull in all pages available
    for i in range(1, n+1):
        new_url = url+ '?page=' + str(i)
        response = requests.get(new_url)
        data = response.json()
        page_items = data['payload']['items']
        items_list += page_items

    #create Pandas df and assign it to variable 'items'  
    items = pd.DataFrame.from_dict(items_list)

    return items


############################# STORES ACQUIRE FUNCTION #########################

def stores_df():
    '''
    This function pulls in stores data from the url provided
    and returns all pages in stores as a Pandas DataFrame
    '''
    #create an empty stores list
    stores_list = []
    #grab data from the url
    url = "https://python.zach.lol/api/v1/stores"

    #create the response
    response = requests.get(url)
    data = response.json()
    #identify keys desired
    n = data['payload']['max_page']

    #create for loop to pull in all pages available
    for i in range(1, n+1):
        new_url = url+ '?page=' + str(i)
        response = requests.get(new_url)
        data = response.json()
        page_stores = data['payload']['stores']
        stores_list += page_stores
    
    #create Pandas df and assign it to variable 'stores'  
    stores = pd.DataFrame.from_dict(stores_list)

    return stores


############################# SALES ACQUIRE FUNCTION #########################

def sales_df():
    '''
    This function pulls in sales data from the url provided
    and returns all pages in sales as a Pandas DataFrame
    '''

    #create an empty sales list
    sales_list = []
    #grab data from the url
    url = "https://python.zach.lol/api/v1/sales"

    #create the response
    response = requests.get(url)
    data = response.json()
    #identify keys desired
    n = data['payload']['max_page']

    #create for loop to pull in all pages available
    for i in range(1, n+1):
        new_url = url+ '?page=' + str(i)
        response = requests.get(new_url)
        data = response.json()
        page_sales = data['payload']['sales']
        sales_list += page_sales

    #create Pandas df and assign it to variable 'sales'
    sales_df = pd.DataFrame.from_dict(sales_list)

    #create a csv from that data
    sales_df.to_csv('sales.csv')

    return sales_df

#######################################################################################
################################## CSV FUNCTIONS ##################################
#######################################################################################

############################ STORE CSV  ##############################

def sales_csv():
    if os.path.isfile('sales.csv'):
        df = pd.read_csv('sales.csv', index_col=0)
    
    else:
        df = sales_df()
        df.to_csv('sales.csv')
    
    return df

############################# ITEMS CSV ####################################

def items_csv():
    '''
    This function stores the grocery items locally as a .csv
    '''
    items = items_df()
    return items.to_csv('items.csv')

############################# STORES CSV ####################################


def stores_csv():
    '''
    This function stores the grocery stores locally as a .csv
    '''
    stores = stores_df()
    return stores.to_csv('stores.csv')


#######################################################################################
################################## MERGE FUNCTIONS ##################################
#######################################################################################

############################# NEW Groceries FUNCTION #########################

def new_data():
    '''
    This function takes in 3 seperate csv files
    and merges them together
    then returns a merged pandas dataframe with that data
    '''
    items_df = pd.read_csv('items.csv')
    stores_df = pd.read_csv('stores.csv')
    sales_df = pd.read_csv('sales.csv')
    sales_stores_df = pd.merge(sales_df, stores_df, left_on='store', right_on='store_id', how='left')
    sales_stores_items_df = pd.merge(sales_stores_df, items_df, left_on='item', right_on='item_id', how='left')
    sales_stores_items_df = sales_stores_items_df.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y', 'Unnamed: 0'])
    
    return sales_stores_items_df

############################# MERGE DATA FUNCTION #########################

def all_store_data():
    '''
    This function uses a csv file of merged store data
    if one does not exist, it is created
    and returns the completed merged df
    '''
    if os.path.isfile('allstoredata.csv'):
        df = pd.read_csv('allstoredata.csv', index_col=0)
    
    else:
        df = new_data()
        df.to_csv('allstoredata.csv')

    return df


import pandas as pd
import numpy as np
import os
from env import host, user, password

###################### Acquire Telco Data ######################

def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    It takes in a string name of a database as an argument.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def new_stores_data():
    '''
    This function reads the telco data from the Codeup db into a df.
    '''
    sql_query = """
                SELECT *
                FROM sales
                JOIN items USING(item_id)
                JOIN stores USING(store_id);
                """
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_connection('tsa_item_demand'))
    
    return df


def get_stores_data():
    '''
    This function reads in telco data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('stores_df.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('stores_df.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_stores_data()
        
        # Cache data
        df.to_csv('stores_df.csv')
        
    return df

def get_London_data():
    df = pd.read_csv('GlobalLandTemperaturesByMajorCity.csv', index_col=0)
    #getting only data for London
    df = df[df.City == 'London']
    return df

def prep_london_data(df):
    #resetting index so we can convert the dates to datetime format
    df.reset_index(inplace=True)
    #converting to datetime format
    df.dt = pd.to_datetime(df.dt)
    #resetting the index so that now it's a datetime formatted index
    df = df.set_index('dt').sort_index()
    #trimming df to have consistent data with no nulls
    df = df.loc['1752-10-01':'2013-08-01','AverageTemperature':'AverageTemperatureUncertainty']
    #renaming columns for clarity
    df = df.rename(columns={'AverageTemperature':'monthly_average_temp', 'AverageTemperatureUncertainty':'monthly_average_uncertainty'})
    #creating new columns for possible high and low monthly temps
    df['possible_high_temp'] = df['monthly_average_temp'] + df['monthly_average_uncertainty']
    df['possible_low_temp'] = df['monthly_average_temp'] - df['monthly_average_uncertainty']
    #making df to include only needed columns
    df = df.loc[:,['monthly_average_temp', 'possible_high_temp', 'possible_low_temp']]
    return df