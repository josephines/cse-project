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
py.sign_in('allykli','crj9pw4dqu')

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

record = read_csv("lost__found__adoptable_pets.csv", "Record_Types")
city = read_csv("lost__found__adoptable_pets.csv", "City") 

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
    
def pet_descriptions(column_names):
    """ 
    Takes in a list of column names
    
    Returns a list of lists containing information describing each pet
    """
    #need to get specifically to adoptable pets, right now it is for all types
    description_list = []
    for col_name in column_names:
        # if Record_Type == 'ADOPTABLE' (or parameter 'type')
        description_list.append(read_csv("lost__found__adoptable_pets.csv", \
                                         col_name))
    return description_list
    
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
                                      
def plot_city_bar(input_dict, title):
    """
    Takes in a list of data, a dictionary of selected column type and counts, 
    and a string title. Plots a bar graph using the keys of the dictionary
    as the x-values and the values as the y-values. Returns None.
    """
    
    data = [
        go.Bar(
            x = input_dict.keys(),
            y = input_dict.values(),
            opacity = 0.8,
            name = title,
            marker = dict(color = input_dict.values())
        )
    ]
    
    layout = go.Layout(
        title = title,
        xaxis = dict(title = "Cities"),
        yaxis = dict(title = "Animal Counts")
    )
    fig = go.Figure(data = data, layout = layout)
    
    py.plot(fig, filename = title) 
    
def plot_record_pie(input_dict, title):
    """
    """
    data = {
        'data': [{'labels': input_dict.keys(),
        'values': input_dict.values(),
        'type': 'pie',
        'hole': .4,
        'insidetextfont': dict(color = 'rgb(255, 255, 255)')
        }],
        
        'layout': {'title': title}
    }

    py.plot(data, filename = title)
    
def filter_dataframe(filename, col_names, record):
    df = pd.read_csv(filename)
    selected = df[col_names] # select certain columns
    filtered = selected[selected.Record_Type == record] # filter to lost pet rows
    
    return filtered    
    
def plot_scatter(x_axis, y_axis, title):
    trace = go.Scatter(
        x = x_axis,
        y = y_axis,
        name = title,
        mode = 'markers'
    )
    data = [trace]
    py.plot(data, filename = title)   
    
def wordcloud(input_csv, mask_file):
    """
    """
    d = path.dirname(__file__)
    text = open(path.join(d, input_csv)).read()
    mask_img = np.array(Image.open(path.join(d, mask_file)))
    wordcloud = WordCloud(background_color="white", mask=mask_img).generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.savefig("animal_wordcloud.png")
    plt.show()  
    
###############
# MAIN FUNCTION    
###############

def main(): 
    """
    Delete print statements later; they're just for debugging/showing outputs 
    """
    
    print "1. How many pets are lost, found, and adoptable?"
    record = read_csv("lost__found__adoptable_pets.csv", "Record_Type")
    lost = count_entries(record)["LOST"]
    found = count_entries(record)["FOUND"]
    adoptable = count_entries(record)["ADOPTABLE"]
    print "Lost:", lost
    print "Found:", found
    print "Adoptable:", adoptable
    #plot_record_pie(count_entries(record), "Lost & Found Animal Counts in King County")
    print
    
    
    print "2. Where are most pets found?"
    city = read_csv("lost__found__adoptable_pets.csv", "City")
    cities_count = count_entries(city)
    most_pets = most_common(cities_count).keys()[0]
    print "Most pets are found in", most_pets
    #plot_city_bar(count_entries(cities), "Cities Where Lost Pets are Found")
    print
    
    
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
    days = list(dataframe.index)
    
    # y-axis of scatter (counts)
    petcounts = DataFrame(day_counts['Count'])
    select_count = list(petcounts["Count"])
    
    print day_counts
    #plot_scatter(days, select_count, "Amount of Pets Found per Day of Week")
    print
    
    
    
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
    
    
    
    print "5. What are the more common traits of pets in King County?"   
    print "See animal_wordcloud.png"  
    write_descriptions_csv("lost__found__adoptable_pets.csv", 'out.csv')
    
    # PLOTTING WORDCLOUD
    #wordcloud('out.csv', 'cat.jpg') 
    
    #pd.options.mode.chained_assignment = None

if __name__ == "__main__":
    main()