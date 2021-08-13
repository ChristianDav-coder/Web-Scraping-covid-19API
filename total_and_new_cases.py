'''
Total cases, new cases and visualization
'''

import matplotlib.pyplot as plt
import matplotlib.colors
import statistics
import data_acquisition

class Total_and_New_Cases():
    '''
    This class calls the dataframe generated in the data acquisition module.
    It makes the visualization of the raw data (cumulative cases),
    it calculates new cases, the mean of 7 days and generates the
    corresponding visualization.
    '''
    def __init__(self, days, country, choice):
        self.days = days
        self.country =country
        self.choice = choice

    def data_frame(self):
        '''
        :return Data Frame (df)
        '''

        if self.choice == 'live':

            D1 = data_acquisition.Data(self.days, self.country)
            url = D1.url()
            print(url)
            self.df = D1.data_fetch()
        else:
            D1 = data_acquisition.Data(self.days, self.country)
            self.df = D1.read_data_from_db()

            return self.df


    def visualization_total_cases(self):
        '''
        This function plots simple evolution of the variables
        :return Plots
        '''
        matplotlib.style.use('ggplot')
        fig = plt.figure(1, figsize=(12, 8))
        fig.add_axes([0,0,1,1])
        fig.suptitle(self.country.upper())
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.bar(self.df['Date'], self.df['Confirmed'], color='royalblue', lw=2, alpha=0.7)
        ax1.set_xticks([self.df['Date'][0], self.df['Date'].iloc[int(len(self.df['Date'])/2)], self.df['Date'].iloc[-1]])
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Confirmed')
        ax1.set_facecolor('#FAEBD7')
        
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.bar(self.df['Date'], self.df['Deaths'], color='royalblue', lw=2, alpha=0.7)
        ax2.set_xticks(
            [self.df['Date'][0], self.df['Date'].iloc[int(len(self.df['Date']) / 2)], self.df['Date'].iloc[-1]])
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Deaths')
        ax2.set_facecolor('#FAEBD7')

        ax3 = fig.add_subplot(2, 2, 3)
        ax3.bar(self.df['Date'], self.df['Recovered'], color='royalblue', lw=2, alpha=0.7)
        ax3.set_xticks(
            [self.df['Date'][0], self.df['Date'].iloc[int(len(self.df['Date']) / 2)], self.df['Date'].iloc[-1]])
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Recovered')
        ax3.set_facecolor('#eafff5')

        ax4 = fig.add_subplot(2, 2, 4)
        ax4.bar(self.df['Date'], self.df['Active'], color='royalblue', lw=2, alpha=0.7)
        ax4.set_xticks(
            [self.df['Date'][0], self.df['Date'].iloc[int(len(self.df['Date']) / 2)], self.df['Date'].iloc[-1]])
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Active')
        ax4.set_facecolor('#FAEBD7')

        plt.show()
        return fig

    def new_cases_calculation(self):
        new_confirmed_list = []
        new_deaths_list = []
        new_recovered_list = []
        new_active_list = []
        for i in range(0, (len(self.df['Confirmed'])-1)):
            df_new_confirmed = (self.df['Confirmed'].iloc[i+1])-(self.df['Confirmed'].iloc[i])
            new_confirmed_list.append(df_new_confirmed)

            df_new_deaths = (self.df['Deaths'].iloc[i+1])-(self.df['Deaths'].iloc[i])
            new_deaths_list.append(df_new_deaths)

            df_new_recovered = (self.df['Recovered'].iloc[i + 1]) - (self.df['Recovered'].iloc[i])
            new_recovered_list.append(df_new_recovered)

            df_new_active = (self.df['Active'].iloc[i + 1]) - (self.df['Active'].iloc[i])
            new_active_list.append(df_new_active)

        new_confirmed_list.insert(0, 0)
        self.df['new_confirmed'] = new_confirmed_list

        new_deaths_list.insert(0, 0)
        self.df['new_deaths'] = new_deaths_list

        new_recovered_list.insert(0, 0)
        self.df['new_recovered'] = new_recovered_list

        new_active_list.insert(0, 0)
        self.df['new_active'] = new_active_list
        return self.df

    def new_cases_median(self):
        mean_new_confirmed_7d = []
        mean_new_deaths_7d = []
        mean_new_recovered_7d = []
        mean_new_active_7d =[]
        for i in range(0, (len(self.df['new_confirmed']))):
            d7_mean_new_confirmed = self.df['new_confirmed'][i:i+7]
            mean_new_confirmed_7d.append(statistics.mean(d7_mean_new_confirmed))

            d7_mean_deaths = self.df['new_deaths'][i:i+7]
            mean_new_deaths_7d.append(statistics.mean(d7_mean_deaths))

            d7_mean_new_recovered = self.df['new_recovered'][i:i+7]
            mean_new_recovered_7d.append(statistics.mean(d7_mean_new_recovered))

            d7_mean_new_active = self.df['new_active'][i:i+7]
            mean_new_active_7d.append(statistics.mean(d7_mean_new_active))

        self.df['new_confirmed_mean_7days'] = mean_new_confirmed_7d
        self.df['new_deaths_mean_7days'] = mean_new_deaths_7d
        self.df['new_recovered_mean_7days'] = mean_new_recovered_7d
        self.df['new_active_mean_7days'] = mean_new_active_7d
        return self.df

    def visualization_new_cases(self):
        '''
        This function plots simple evolution of the calculated variables
        :return Plots
        '''
        matplotlib.style.use('ggplot')
        fig = plt.figure(2, figsize=(12, 8))
        fig.add_axes([0, 0, 1, 1])
        fig.suptitle(self.country.upper())
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.bar(self.df['Date'], self.df['new_confirmed'], color='green', lw=2, alpha=0.4)
        ax1.plot(self.df['Date'], self.df['new_confirmed_mean_7days'], color='orange', lw=3, alpha=1)
        ax1.set_xticks(
            [self.df['Date'][0], self.df['Date'].iloc[int(len(self.df['Date']) / 2)], self.df['Date'].iloc[-1]])
        ax1.set_xlabel('Date')
        ax1.set_ylabel('New_Confirmed')
        ax1.set_facecolor('#FAEBD7')

        ax2 = fig.add_subplot(2, 2, 2)
        ax2.bar(self.df['Date'], self.df['new_deaths'], color='green', lw=2, alpha=0.4)
        ax2.plot(self.df['Date'], self.df['new_deaths_mean_7days'], color='orange', lw=3, alpha=1)
        ax2.set_xticks(
            [self.df['Date'][0], self.df['Date'].iloc[int(len(self.df['Date']) / 2)], self.df['Date'].iloc[-1]])
        ax2.set_xlabel('Date')
        ax2.set_ylabel('New_Deaths')
        ax2.set_facecolor('#FAEBD7')

        ax3 = fig.add_subplot(2, 2, 3)
        ax3.bar(self.df['Date'], self.df['new_recovered'], color='green', lw=2, alpha=0.4)
        ax3.plot(self.df['Date'], self.df['new_recovered_mean_7days'], color='orange', lw=3, alpha=1)
        ax3.set_xticks(
            [self.df['Date'][0], self.df['Date'].iloc[int(len(self.df['Date']) / 2)], self.df['Date'].iloc[-1]])
        ax3.set_xlabel('Date')
        ax3.set_ylabel('New_Recovered')
        ax3.set_facecolor('#eafff5')

        ax4 = fig.add_subplot(2, 2, 4)
        ax4.bar(self.df['Date'], self.df['new_active'], color='green', lw=2, alpha=0.4)
        ax4.plot(self.df['Date'], self.df['new_active_mean_7days'], color='orange', lw=3, alpha=1)
        ax4.set_xticks(
            [self.df['Date'][0], self.df['Date'].iloc[int(len(self.df['Date']) / 2)], self.df['Date'].iloc[-1]])
        ax4.set_xlabel('Date')
        ax4.set_ylabel('New_Active')
        ax4.set_facecolor('#FAEBD7')

        plt.show()
        return fig

#
# C1 = Total_and_New_Cases(300, 'germany', 'db')
# C1.data_frame()
# C1.visualization_total_cases()
# C1.new_cases_calculation()
# C1.new_cases_median()
# C1.visualization_new_cases()

# V1 = Visual(525, 'germany')
# print(V1.DataFrame())
# V1.Graphics()

# V1 = Visual(600, 'chile')
# df2 = V1.data_frame_2()
# V1.Graphics()
# print(df2)