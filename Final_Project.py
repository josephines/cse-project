# CSE 160 AC 
# Homework 7 - Final Project - Part 2
# Allyson Kline & Josephine Le
# Most recently updated: March 7, 1:01 AM 

import csv
import os
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go

from os import path
from wordcloud import WordCloud

# Record_Type, Current_Location, City, Memo (word cloud only)

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

"""
def word_cloud():
"""

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
    

###############
# MAIN FUNCTION    
###############

def main(): 
    """
    Delete print statements later; they're just for debugging/showing outputs 
    """
    
    # 1. How many pets have been lost and how many have been found?
    record = read_csv("lost__found__adoptable_pets.csv", "Record_Type")
    plot_record_pie(count_entries(record), "Lost & Found Animal Counts in King County")
    
    # 2. Where are most pets found?
    cities = read_csv("lost__found__adoptable_pets.csv", "City")
    plot_city_bar(count_entries(cities), "Cities Where Lost Pets are Found")
    
    """      
    Gets the city with the most lost pets found 
    city = read_csv("lost__found__adoptable_pets.csv", "City")
    cities = count_entries(city)
    most_pets = most_common(cities).keys()[0]
    print "Most pets are found in", most_pets
    """
    
    # 3. Is there a correlation between the day of the week and the amount of 
    # pets lost?
    
    # 4. How many adoptable animals are there currently and where can they be 
    # adopted?
    adoptable = count_entries(record)["ADOPTABLE"]
    location = read_csv("lost__found__adoptable_pets.csv", "Current_Location")
    adopt_locations = count_entries(location)
    print "Currently,", adoptable, "animals are available for adoption."
    print "Animals can be adopted at", adopt_locations.keys()
    
    # 5. How are adoptable pets described? -> maybe change to: What are the more 
    # common traits of adoptable pets?
    
    # filter down to adoptable pets
    # access "Animal_Color", "Animal_Gender", "Animal_Breed", "animal_type", 
    # "Age" columns
    #  (^^^ same info as the memo column)
    # gather each column entry into a list (could be later compiled into a list
    #   of lists if necessary for the word cloud)
        
    descriptions = ["Animal_Color", "Animal_Gender", "Animal_Breed", "animal_type",
    "Age"]
    pet_descriptions(descriptions)
    
    # PLOTTING WORDCLOUD
    d = path.dirname(__file__)
    text = open(path.join(d, "lost__found__adoptable_pets.csv")).read()
    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
      

if __name__ == "__main__":
    main()