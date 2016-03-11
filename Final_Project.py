# CSE 160 AC 
# Homework 7 - Final Project - Part 2
# Allyson Kline & Josephine Le
# Most recently updated: March 7, 1:01 AM 

import csv
import os
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np
import pandas as pd

from os import path
from PIL import Image 
from wordcloud import WordCloud
from pandas import *

# Plotly graph to browser -- requires authentication of one account
py.sign_in('jojole', '8o3knsdwg8')
#py.sign_in('allykli','crj9pw4dqu')

def read_csv(filename, column_name):   
    """
    Takes in a string filename and string column_name
    
    Returns a list of all entries in a column name of an input file
    """
    pets_csv = csv.DictReader(open(filename))
    
    entries = []

    for row in pets_csv:
        for entry in row.keys():
            if entry in column_name and row[entry] != '':
                entries.append(row[entry])
    return entries
 
def count_entries(entries):
    """
    Takes in a list of entries
    
    Returns a dictionary in which the keys are the names of each entry, 
    and the values are the amount of times it occurs
    """
    entries_counts = {}
    
    for entry in entries:
        if entry not in entries_counts:
            entries_counts[entry] = 0
        entries_counts[entry] += 1
    return entries_counts

def most_common(count_dict):
    """
    Takes in a dictionary of entries with their corresponding counts 
    
    Returns a single-entry dictionary that contains the most commonly occuring
    entry and its counts
    """
    max_dict = {}
    max_count = 0
    for entry in count_dict.keys():
        if count_dict[entry] > max_count:
            max_count = count_dict[entry]
            highest = entry
    
    max_dict[highest] = max_count
    return max_dict 
    
def week_order(days_order, unordered_days, pets_per_day):
    """
    Takes in a lexicographically ordered list of strings representing the days
    of a week and a corresponding list of numbers.
    Returns a list of numbers reordered based on the correct ordering of days
    of week
        e.g. ['Fri', 'Mon', 'Wed'], [6, 2, 3] --> [2, 3, 6]
    
    Parameters:
        days_order: a dictionary that maps numbers 0-6 to string days of week
        unordered_days: a list of strings of days, ordered lexicographically
        pets_per_day: a list of numbers
    """    
    mapped = {}
    for i in range(len(unordered_days)):
        mapped[unordered_days[i]] = pets_per_day[i] 
     
    ordered_count = []
    for day in days_order.values():
        ordered_count.append(mapped[day])
    
    return ordered_count
    
def write_descriptions_csv(input_file, output_csv):  
    """
    """  
     # WRITE NEW CSV
    with open(output_csv, 'wb') as f: # output csv file
        writer = csv.writer(f)
        with open(input_file,'r') as csvfile: # input csv file
            reader = csv.DictReader(csvfile, delimiter=',')
            for row in reader:
                    writer.writerow([[row["Animal_Color"], row["Animal_Gender"], 
                                      row["Animal_Breed"], row["animal_type"]]])
                                      
def plot_city_bar(input_dict, xax_name, yax_name, title):
    """
    Makes a bar graph of given input dictionary with axes labels
    
    Parameters:
        input_dict: a dictionary mapping strings to numbers
        xax_name: a string for x-axis title
        yax_name: a string for y-axis title
        title: a string for title of plot and plotly page
        
    Returns None
    """
    # Data features
    data = [
        go.Bar(
            x = input_dict.keys(),
            y = input_dict.values(),
            opacity = 0.8,
            name = title,
            marker = dict(color = input_dict.values())
        )
    ]
    
    # Layout of plot
    layout = go.Layout(
        title = title,
        xaxis = dict(title = xax_name),
        yaxis = dict(title = yax_name)
    )
    
    # Plots figure to browser using Plotly
    fig = go.Figure(data = data, layout = layout)
    py.plot(fig, filename = title) 
    
def plot_record_pie(input_dict, title):
    """
    Makes a pie graph of given input dictionary keys and values
    
    Parameters:
        input_dict: a dictionary mapping strings to numbers
        title: a string for title of plot and plotly page
        
    Returns None
    """
    # Data features
    data = {
        'data': [{'labels': input_dict.keys(),
        'values': input_dict.values(),
        'type': 'pie',
        'hole': .4,
        'insidetextfont': dict(color = 'rgb(255, 255, 255)')
        }],
        'layout': {'title': title}
    }

    # Plots data to browser using Plotly
    py.plot(data, filename = title)
    
def filter_dataframe(filename, col_names, record):
    """
    Takes in a string filename and reads the file, selects specific columns of
    a dataset, then filters those columns by a specific row entry
    
    Parameters:
        filename: a string for name of file to read in
        col_names: a list of strings of specific column names to select
        record: a string that represents selected record type
        
    Returns a smaller/new dataframe from the given .csv file with specified 
    columns/rows
    """
    df = pd.read_csv(filename)
    selected = df[col_names] # select certain columns
    filtered = selected[selected.Record_Type == record] # filter to lost pet rows
    
    return filtered    
    
def plot_scatter(x_axis, y_axis, xax_name, yax_name, title):
    """
    Plots a scatterplot of given input lists with axes labels
    
    Parameters:
        x_axis: a list that represents x-values        
        y_axis: a list that represents y-values  
        xax_name: a string for x-axis title
        yax_name: a string for y-axis title
        title: a string for title of plot and plotly page
        
    Returns None
    """
    trace = go.Scatter(
        x = x_axis,
        y = y_axis,
        mode = 'markers',
        marker = dict(
            size = 20,
            color = y_axis)
    )
    data = [trace]
    
    layout = go.Layout(
        dict(title = title,
        xaxis = dict(title = xax_name),
        yaxis = dict(title = yax_name))
    )
                  
    fig = dict(data = data, layout = layout)
    py.plot(fig, filename = title)   
    
def wordcloud(filename, mask_file, output_name):
    """
    Generates a word cloud 
    
    Parameters:
        filename: a string representing the name of a file
        mask_file: a string representing the name of an image file
        output_name: a string representing the name of the wordcloud output file
            
    Returns None
    """
    d = path.dirname(__file__)
    text = open(path.join(d, filename)).read()
    mask_img = np.array(Image.open(path.join(d, mask_file)))
    wordcloud = WordCloud(background_color = "white", 
                          mask = mask_img).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig(output_name)
    plt.show()  
    
###############
# MAIN FUNCTION    
###############

def main(): 
    """
    """
    
    ## 1
    print "1. How many pets are lost, found, and adoptable?"
    record = read_csv("lost__found__adoptable_pets.csv", "Record_Type")
    lost = count_entries(record)["LOST"]
    found = count_entries(record)["FOUND"]
    adoptable = count_entries(record)["ADOPTABLE"]
    print "Lost:", lost
    print "Found:", found
    print "Adoptable:", adoptable
    plot_record_pie(count_entries(record), \
                    "Lost & Found Animal Counts in King County")
    print
    
    
    ## 2
    print "2. Where are most pets found?"
    city_col = read_csv("lost__found__adoptable_pets.csv", "City")
    cities = count_entries(city_col)
    most_pets = most_common(cities).keys()[0]
    print "Most pets are found in", most_pets
    plot_city_bar(count_entries(city_col), "Cities", "Animal Counts", \
                                "Cities Where Lost Pets are Found")
    print
    
    
    ## 3
    print "3. How does the number of pets lost vary per day of week?"
    filter_days = filter_dataframe("lost__found__adoptable_pets.csv", \
                                   ["Record_Type","Date"],"LOST")
    
    filter_days['Date'] = pd.to_datetime(filter_days['Date']) # transpose it to proper date format
    filter_days['day_of_week'] = filter_days['Date'].dt.dayofweek # turn it into day of week
    days = {0:'Mon',1:'Tues',2:'Weds',3:'Thurs',4:'Fri',5:'Sat',6:'Sun'} # re-label to str days
    filter_days['day_of_week'] = filter_days['day_of_week'].apply(lambda x: days[x]) # applying new labels
    
    info = filter_days.groupby("day_of_week") # group data by day of the week
    day_counts = (info.agg({"Record_Type": "count"}) # collect counts (don't care about record data anymore)
                      .rename(columns={"Record_Type": "Count"})) # rename column to counts
                             
    # x-axis of scatter (days of week)                         
    dataframe = DataFrame(day_counts)              
    week_days = list(dataframe.index)
    
    # y-axis of scatter (counts)
    petcounts = DataFrame(day_counts['Count'])
    select_count = list(petcounts["Count"])
    
    print day_counts
    ordered_counts = week_order(days, week_days, select_count)
    plot_scatter(days.values(), ordered_counts, "Days of the week", \
                 "Pet counts", "Amount of Pets Found per Day of Week")
    print
    
    
    ## 4
    print "4. Where can animals be adopted, and how many are at each location?"

    filter_adoptable = filter_dataframe("lost__found__adoptable_pets.csv", \
                                     ["Record_Type", "Current_Location"], \
                                     "ADOPTABLE")
    
    location_group = filter_adoptable.groupby("Current_Location") # group data by day of the week
    location_count = (location_group.agg({"Record_Type": "count"}) # collect counts (don't care about record data anymore)
                      .rename(columns={"Record_Type": "Count"}) # rename column to counts
                     )          
        
    print location_count
    print
    
    
    ## 5
    print "5. What are the more common traits of pets in King County?"   
    print "***See animal_wordcloud.png in cse-project folder***"  
    # Plots wordcloud
    write_descriptions_csv("lost__found__adoptable_pets.csv", 'out.csv')
    wordcloud('out.csv', 'cat.jpg', 'animal_wordcloud.png') 

if __name__ == "__main__":
    main()