'''
Data acquisition
'''

import datetime
from datetime import date
import requests
import sqlite3 as sl
import pandas as pd

class Data():
    '''
    This class downloads data from covid19-API, transforms in a dataframe and
     saves in a database or as a csv file.
    '''
    def __init__(self, days, country):
        self.days = days
        self.country =country

    def url(self):
        '''
        This function builts up a functional url for data fetching.
        variable days means the amount of days backwards from today.
        :return api_url (String).
        '''
        # completed url
        # https://api.covid19api.com/country/germany?from=2020-03-01T00:00:00Z&to=2021-06-25T00:00:00Z
        url_root = 'https://api.covid19api.com/country/'

        to_date_1 = date.today()
        to_date_2 = to_date_1.strftime('%Y-%m-%dT%H:%M:%SZ')
        from_date = to_date_1 - datetime.timedelta(days=self.days)
        from_date_2 = from_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.url_api = url_root + self.country + '?from=' + from_date_2 + '&to=' + to_date_2
        return self.url_api

    def data_fetch(self):
        '''
        This function extracts the desired columns from json files.
        :return data_selected (List of Lists)
        '''
        connect_api = requests.get(self.url_api)
        data = connect_api.json()
        self.data_selected = []
        for item in range(0, len(data)):
            data_f = [data[item]['Country'], data[item]['Date'][:10], data[item]['Confirmed'],
                      data[item]['Deaths'], data[item]['Recovered'], data[item]['Active']]
            self.data_selected.append(data_f)

        self.df = pd.DataFrame(self.data_selected)
        self.df.columns = ['Country', 'Date', 'Confirmed', 'Deaths', 'Recovered', 'Active']
        return self.df

    def save_data_to_db(self):
        '''
        This function saves the selected data from the API in a database.
        I use 'DBeaver' to manage the database.
        :return .db file or possible .csv file.
        '''
        connection = sl.connect('Covid19_API.db')
        table_name = self.country + '_' + str(self.days)
        table = self.df.to_sql(table_name, connection)
        return table

    def read_data_from_db(self):
        '''
        :return Data Frame (df) from database
        '''
        connection = sl.connect('Covid19_API.db')
        table_name = self.country + '_' + str(self.days)
        self.df = pd.read_sql(f'''SELECT* FROM {table_name}''', connection)
        return self.df






# D1 = Data(100, 'germany')
#
# # data_db = D1.read_data_from_db()
# # print(data_db)
#
# url = D1.url()
# print(url)
# data_live = D1.data_fetch()
# print(data_live)

