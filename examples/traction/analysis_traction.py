import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

## Get data file and return a dataframe
def get_data_traction(filename):
    datafile = pd.read_csv(filename, header=None, skiprows=1, delimiter="\t", names=['Time', 'Loadvolt', 'LoadKg'])
    return datafile

## Draw a graph with time vs load
def draw_time_vs_load(dataframe, title='Time vs Load', x_base = 0, y_base = 0, 
                      offset_time = False, offset_load = False, with_lines = True, convert_force = False):
    
    fig, ax = plt.subplots(figsize=(5, 5), nrows=1, ncols=1)
    xlabel = 'Time (s)'
    ylabel = 'Load (Kg)'
    
    if offset_time:
        dataframe['Time'] = dataframe['Time'] - dataframe['Time'][0]

    if offset_load:
        dataframe['LoadKg'] = dataframe['LoadKg'] - dataframe['LoadKg'][0]

    if convert_force:
        dataframe['LoadKg'] = dataframe['LoadKg'] * 9.81
        ylabel = 'Load (N)'

    if with_lines:
        style = "-"
    else:
        style = "None"
    
    ax.plot(dataframe['Time'], dataframe['LoadKg'], linestyle=style, marker = "x", markersize=2, color='blue')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    ax.set_xlim(x_base)
    ax.set_ylim(y_base)
    plt.show()


data = get_data_traction('example_traction_1.txt')
print(data.head())
draw_time_vs_load(data, x_base=0, y_base=0, offset_load=True, with_lines=True, convert_force=True)