#import pandas as pd
import numpy as np
import re
from src.utils import generate_plot


KANNA_HASHIMOTO = "https://i.pinimg.com/originals/f6/38/f8/f638f8a25b7c5239c23df2c16da631da.jpg"

def draw_country(dataframe):
    # print(dataframe)
    trans_dataframe = dataframe[["Country"]].to_numpy().flatten()
    # print(trans_dataframe)

    country, cnt = np.unique(trans_dataframe, return_counts=True)
    data = tuple(zip(country, cnt))

    # pick top 5 countries
    sorted_data = sorted(data, key=lambda tup: tup[1], reverse=True)
    others = 0
    while(len(sorted_data) > 5):
        last = sorted_data.pop()
        others += last[1]

    countries = list(map(lambda a: a[0], sorted_data))
    computers = list(map(lambda a: a[1], sorted_data))

    countries.append("others")
    computers.append(others)

    """ Generate plot """
    filename = generate_plot({
        "data": computers,
        "labels": countries,
    })

    return filename

def draw_energy(dataframe):
    trans_dataframe = dataframe[["Country"]].to_numpy().flatten()
    country, cnt = np.unique(trans_dataframe, return_counts=True)

    dataset = dict((nation, 0) for nation in country)
    #print(dataset)
    dataframe = dataframe.reset_index()
    error_country= []

    """ counting total power usage """
    for index, row in dataframe.iterrows():
        nation = row["Country"]
        try:
            power = re.search("<td>([0-9,]+)<\/td>", str(row["Power"])).group(1)
            power = int(power.replace(",", ""))
            dataset[nation] += power
        except:
            #print("error:",nation)
            error_country.append(nation)
    
    dataset_in_tuple = [(country_temp,power_temp) for country_temp,power_temp in dataset.items()]

    # pick top 5 contries
    sorted_data = sorted(dataset_in_tuple, key=lambda tup: tup[1], reverse=True)
    others = 0
    while(len(sorted_data) > 5):
        last = sorted_data.pop()
        others += last[1]
    
    countries = list(map(lambda a: a[0], sorted_data))
    power_usage = list(map(lambda a: a[1], sorted_data))

    countries.append("others")
    power_usage.append(others)

    """ Generate plot """
    filename = generate_plot({
        "data": power_usage,
        "labels": countries,
    })

    #print(error_country)
    return filename

def draw_manufacturer(dataframe):
    trans_dataframe = dataframe[["Manufacturer"]].to_numpy().flatten()
    manufacturers, cnt = np.unique(trans_dataframe, return_counts=True)

    brands = []
    for e in manufacturers:
        result = e.split("/")
        for ee in result:
            brands.append(ee.strip())

    brands = np.unique(brands)
    dataset = dict((brand, 0) for brand in brands)
    
    """ counting total power usage """
    for index, row in dataframe.iterrows():
        brand = row["Manufacturer"]
        
        result = brand.split("/")
        for ee in result:
            dataset[ee.strip()] += 1
        
    dataset_in_tuple = [(country_temp,power_temp) for country_temp,power_temp in dataset.items()]

    # pick top 5 manufactor
    sorted_data = sorted(dataset_in_tuple, key=lambda tup: tup[1], reverse=True)
    others = 0
    while(len(sorted_data) > 5):
        last = sorted_data.pop()
        others += last[1]
    
    manufacturer = list(map(lambda a: a[0], sorted_data))
    count = list(map(lambda a: a[1], sorted_data))

    manufacturer.append("others")
    count.append(others)

    filename = generate_plot({
        "data": count,
        "labels": manufacturer,
    })

    return filename

def draw_countability(dataframe):
    trans_dataframe = dataframe[["Country"]].to_numpy().flatten()
    country, cnt = np.unique(trans_dataframe, return_counts=True)

    dataset = dict((nation, 0.0) for nation in country)

    """ counting total countability """
    for index, row in dataframe.iterrows():
        nation = row["Country"]
        rpeak = re.search('<td style="text-align: right;">([0-9,.]+)<\/td>', str(row["Rpeak"])).group(1)
        rpeak = float(rpeak.replace(",", ""))

        dataset[nation] += rpeak
    
    dataset_in_tuple = [(country_temp,power_temp) for country_temp,power_temp in dataset.items()]

    """ picking top 5 countries """
    sorted_data = sorted(dataset_in_tuple, key=lambda tup: tup[1], reverse=True)
    others = 0
    while(len(sorted_data) > 5):
        last = sorted_data.pop()
        others += last[1]
    
    countries = list(map(lambda a: a[0], sorted_data))
    rpeak_total = list(map(lambda a: a[1], sorted_data))
    
    filename = generate_plot({
        "data": rpeak_total,
        "labels": countries,
    })

    return filename

def draw_cores(dataframe):
    trans_dataframe = dataframe[["Country"]].to_numpy().flatten()
    country, cnt = np.unique(trans_dataframe, return_counts=True)

    dataset = dict((nation, 0.0) for nation in country)

    """ counting total cores """
    for index, row in dataframe.iterrows():
        nation = row["Country"]
        
        cores = re.search('<td style="text-align: right;">([0-9,]+)</td>', str(row["cores"])).group(1)
        cores = int(cores.replace(",", ""))

        dataset[nation] += cores
    
    dataset_in_tuple = [(country_temp,power_temp) for country_temp,power_temp in dataset.items()]

    """ picking top 5 countries """
    sorted_data = sorted(dataset_in_tuple, key=lambda tup: tup[1], reverse=True)
    others = 0
    while(len(sorted_data) > 5):
        last = sorted_data.pop()
        others += last[1]

    countries = list(map(lambda a: a[0], sorted_data))
    cores = list(map(lambda a: a[1], sorted_data))
    
    filename = generate_plot({
        "data": cores,
        "labels": countries,
    })

    return filename