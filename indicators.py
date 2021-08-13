'''
Indicators calculation
'''

import matplotlib.colors
import numpy
from scipy import optimize
from total_and_new_cases import *

class Indicators():
    '''
    This class retrieves data from the total_and_new_cases module.
    It calculates indicators such as the incidence rate and the
    growth rate. Furthermore, it generates the corresponding visualization.
    '''
    def __init__(self, days, country, choice, population):
        self.days = days
        self.country = country
        self.choice = choice
        self.population = population

        C1 = Total_and_New_Cases(self.days, self.country, choice)
        C1.data_frame()
        self.df_new_cases = C1.new_cases_calculation()


    def incidence_rate(self):

        sum_7days = []
        for i in range(0, (len(self.df_new_cases['Confirmed'])-7)):
            days_7 = (self.df_new_cases['Confirmed'].iloc[i+7]) - (self.df_new_cases['Confirmed'].iloc[i])
            calculation = (days_7 / self.population) * 100000
            sum_7days.append(calculation)

        for i in range(0, 7):
            sum_7days.insert(0, 0)
        self.df_new_cases['incidence_7days'] = sum_7days

        sum_14days = []
        for i in range(0, (len(self.df_new_cases['Confirmed'])-14)):
            days_14 = (self.df_new_cases['Confirmed'].iloc[i+14]) - (self.df_new_cases['Confirmed'].iloc[i])
            calculation = (days_14 / self.population) * 100000
            sum_14days.append(calculation)

        for i in range(0, 14):
            sum_14days.insert(0, 0)
        self.df_new_cases['incidence_14days'] = sum_14days

        return self.df_new_cases


    def growth_rate(self):

        growth_rate_list = []
        for i in range(0, (len(self.df_new_cases['new_confirmed']))):
            days_7_cases = self.df_new_cases['new_confirmed'][i:i+7]
            days_7_2 = [x for x in range(1,8)]

            try:
                result2 = optimize.curve_fit(lambda t, a, b: a * numpy.exp(b * t), days_7_2, days_7_cases, p0=(0.5, 0.1))
            except:
                print('not converge')
            print(result2[0][1])
            # Implement the try error function!!! there are some ranges where the fit does not converge!!!
            # Let´s try to test other fits. to calculate the growth rate
            growth_rate_list.append(result2[0][1])

        self.df_new_cases['growth_rate'] = growth_rate_list
        return self.df_new_cases


    def reproduction_rate(self):
        pass

    def visualization_indicators(self):
        '''
        This graphics show the evolution of important indicators of a
        epidemic spread
        :return Plots
        '''
        matplotlib.style.use('ggplot')
        fig = plt.figure(3, figsize=(12, 8))
        fig.add_axes([0, 0, 1, 1])
        fig.suptitle(self.country.upper())
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.bar(self.df_new_cases['Date'], self.df_new_cases['new_confirmed'], color='royalblue', lw=2, alpha=0.7)
        ax1.set_xticks(
            [self.df_new_cases['Date'][0], self.df_new_cases['Date'].iloc[int(len(self.df_new_cases['Date']) / 2)], self.df_new_cases['Date'].iloc[-1]])
        ax1.set_xlabel('Date')
        ax1.set_ylabel('New_Confirmed')
        ax1.set_facecolor('#FAEBD7')

        ax2 = fig.add_subplot(2, 2, 2)
        ax2.bar(self.df_new_cases['Date'], self.df_new_cases['incidence_7days'], color='green', lw=2, alpha=0.4)
        ax2.set_xticks(
            [self.df_new_cases['Date'][0], self.df_new_cases['Date'].iloc[int(len(self.df_new_cases['Date']) / 2)],
             self.df_new_cases['Date'].iloc[-1]])
        ax2.set_xlabel('Date')
        ax2.set_ylabel('incidence_7days')
        ax2.set_facecolor('#FAEBD7')

        ax3 = fig.add_subplot(2, 2, 3)
        ax3.bar(self.df_new_cases['Date'], self.df_new_cases['incidence_14days'], color='green', lw=2, alpha=0.4)
        ax3.set_xticks(
            [self.df_new_cases['Date'][0], self.df_new_cases['Date'].iloc[int(len(self.df_new_cases['Date']) / 2)],
             self.df_new_cases['Date'].iloc[-1]])
        ax3.set_xlabel('Date')
        ax3.set_ylabel('incidence_14days')
        ax3.set_facecolor('#FAEBD7')

        ax4 = fig.add_subplot(2, 2, 4)
        ax4.bar(self.df_new_cases['Date'], self.df_new_cases['growth_rate'], color='royalblue', lw=2, alpha=0.7)
        ax4.set_xticks(
            [self.df_new_cases['Date'][0], self.df_new_cases['Date'].iloc[int(len(self.df_new_cases['Date']) / 2)],
             self.df_new_cases['Date'].iloc[-1]])
        ax4.set_xlabel('Date')
        ax4.set_ylabel('growth_rate')
        ax4.set_facecolor('#FAEBD7')

        plt.show()
        return fig



# I1 = Indicators(100, 'germany', 'live' ,83783945)
# rate = I1.incidence_rate()
# print(rate)
# growth = I1.growth_rate()
# graph = I1.visualization_indicators()

