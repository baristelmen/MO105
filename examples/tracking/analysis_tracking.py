import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

def get_data_tracking(filename, number_of_roi):

    name_col = []
    name_col.append('Time')
    for i in range(number_of_roi):
        name_col.append('x' + str(i+1))
        name_col.append('y' + str(i+1))

    datafile = pd.read_csv(filename, header=None, skiprows=1, delimiter="\t", names=name_col)
    return datafile

def get_time_vs_displacement(dataframe, roi_number = [1,3], title = 'Time vs Displacement', x_base = None, y_base = None,
                             offset_time = False, offset_displacement = False, with_lines = True, strain=False):
    
    dataframe['Displacement'] = np.sqrt((dataframe['x' + str(roi_number[1])] - dataframe['x' + str(roi_number[0])])**2 + 
                                        (dataframe['y' + str(roi_number[1])] - dataframe['y' + str(roi_number[0])])**2)

    y_val = 'Displacement'
    x_val = 'Time'

    xlabel = 'Time (s)'
    ylabel = 'Displacement (mm)'

    if strain:
        dataframe['Strain'] = dataframe['Displacement'] / dataframe['Displacement'][0]
        y_val = 'Strain'
        ylabel = 'Strain (mm/mm)'

    fig, ax = plt.subplots(figsize=(5, 5), nrows=1, ncols=1)
    
    if offset_time:
        dataframe['Time'] = dataframe['Time'] - dataframe['Time'][0]

    if offset_displacement:
        dataframe[y_val] = dataframe[y_val] - dataframe[y_val][0]

    if with_lines:
        style = "-"
    else:
        style = "None"
    
    

    ax.plot(dataframe[x_val], dataframe[y_val], linestyle=style, marker = "x", markersize=2, color='blue')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True)
    ax.set_xlim(x_base)
    ax.set_ylim(y_base)
    plt.show()


data = get_data_tracking('output.mp4_tracking.csv', number_of_roi = 3)
print(data)
get_time_vs_displacement(data, roi_number=[1,3], offset_displacement=True, with_lines=True, strain=True)