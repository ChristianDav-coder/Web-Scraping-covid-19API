'''
Graphical User Interface
'''

import tkinter as tk
from indicators import *
from total_and_new_cases import *
from data_acquisition import *



# MAIN WINDOW
window = tk.Tk()
window.title('covid19 API Visualization')
window.resizable(width="True", height="True")

# FUNCTIONS
def runApp():
    Country = country_1.get()
    Days = int(days_1.get())
    Choice = choice_1.get()
    Population = int(population_1.get())

    print(f'The selected country is {Country.upper()},')
    print(f'for {Days} days,')
    print(f'using {Choice} data,')
    print(f'The population of {Country} is {Population}.')

    C1 = Total_and_New_Cases(Days, Country, Choice)
    C1.data_frame()
    C1.visualization_total_cases()
    C1.new_cases_calculation()
    C1.new_cases_median()
    C1.visualization_new_cases()


    I1 = Indicators(Days, Country, Choice, Population)
    I1.incidence_rate()
    I1.growth_rate()
    I1.visualization_indicators()



def saveData():
    Country = country_1.get()
    Days = int(days_1.get())
    print(f'Saving data of {Country},')
    print(f'for {Days} days...')
    S1 = Data(Days, Country)
    S1.url()
    S1.data_fetch()
    S1.save_data_to_db()


def closeApp():
    window.destroy()

# WIDGETS
# Frames : header, center, bottom
frame_header = tk.Frame(window, borderwidth=2, pady=2)
center_frame = tk.Frame(window, borderwidth=2, pady=5)
bottom_frame = tk.Frame(window, borderwidth=2, pady=5)
frame_header.grid(row=0, column=0)
center_frame.grid(row=1, column=0)
bottom_frame.grid(row=2, column=0)

# Frame (header)-------------------------------------------------------------
header = tk.Label(frame_header, text = "covid19 API", bg='black', fg='white',
                  height='3', width='50', font=("Helvetica 16 bold"))
header.grid(row=0, column=0)

# Frame (center)-------------------------------------------------------------
frame_main_1 = tk.Frame(center_frame, borderwidth=1, relief='sunken')
country = tk.Label(frame_main_1, text = "Country: ")
days = tk.Label(frame_main_1, text = "Days:")
choice = tk.Label(frame_main_1, text ="live/db:" )
population = tk.Label(frame_main_1, text = "Population:")

# Entries
country_1 = tk.StringVar()
days_1 = tk.StringVar()
choice_1 = tk.StringVar()
population_1 = tk.StringVar()
country_entry = tk.Entry(frame_main_1, textvariable = country_1, width=12)
days_entry = tk.Entry(frame_main_1, textvariable = days_1, width=4)
choice_entry = tk.Entry(frame_main_1, textvariable = choice_1, width=4)
population_entry = tk.Entry(frame_main_1, textvariable = population_1, width=12)
frame_main_1.pack(fill='x', pady=1)

# Packs
country.pack(side='left')
country_entry.pack(side='left', padx=5)
days.pack(side='left', padx=5)
days_entry.pack(side='left')
choice.pack(side='left', padx=5)
choice_entry.pack(side='left')
population.pack(side='left', padx=5)
population_entry.pack(side='left')

# Frame (bottom)------------------------------------------------------------
button_run = tk.Button(bottom_frame, text="Run", command=runApp, bg='dark green',
                       fg='white', relief='raised', width=10, font=('Helvetica 9 bold'))
button_run.grid(column=0, row=0, sticky='w', padx=100, pady=2)

button_close = tk.Button(bottom_frame, text="Exit", command=closeApp, bg='dark red',
                         fg='white', relief='raised', width=10, font=('Helvetica 9'))
button_close.grid(column=1, row=0, sticky='e', padx=100, pady=2)

button_save = tk.Button(bottom_frame, text="Save", command=saveData, bg='blue',
                         fg='white', relief='raised', width=10, font=('Helvetica 9'))
button_save.grid(column=2, row=0, sticky='e', padx=100, pady=2)

# Compiler
window.mainloop()