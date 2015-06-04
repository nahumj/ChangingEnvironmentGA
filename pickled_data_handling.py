import csv
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
#import scipy.stats as stats
import cPickle

def main():
    test_dir = "length_100_2015_May_27"
    data = get_data(test_dir)
    landscape = "schafferf7"
    plot_aggregate_over_time(data, landscape, test_dir)
    plot_stddev_over_time(data, landscape, test_dir)
    plot_average_final_fitness(data, landscape, test_dir)
    #plot_single_run_over_time(data[data.keys()[0]]["1"]["average_experienced"], test_dir)
    #print data.keys()[0]

#Not currently used, but could be used to grab one set of data
def new_way_to_get_desired_data(common_dir, desired_data):
    #Make a new dictionary
    data = {}
    #For each sub directory...
    for sub_dir in os.listdir(common_dir):
        #If it's not actually a directory, skip it
        if not os.path.isdir(common_dir + "/" + sub_dir):
            continue
        #Grab the meaningful config name
        sub_dir_name_list = sub_dir.split("/")[-1].split("_")
        config = "_".join(dir_name_list[:-2])
        #Make sure the config name is in the dictionary
        if config not in data:
            data[config] = []
        #Append the desired data to the associated list
        #with open(common_dir+"/"+d+"/correlation.dat") as infile:
        #    data[config].append(float(infile.readline()))
        if desired_data == "average_experienced":
            data[config].append(pd.read_csv(common_dir+"/"+sub_dir+"/experienced_fitnesses.csv"))
        elif desired_data == "average_reference":
            data[config].append(pd.read_csv(common_dir+"/"+sub_dir+"/reference_fitnesses.csv"))
        elif desired_data == "best_experienced":
            data[config].append(pd.read_csv(common_dir+"/"+sub_dir+"/experienced_best_fitnesses.csv"))
        elif desired_data == "best_reference":
            data[config].append(pd.read_csv(common_dir+"/"+sub_dir+"/reference_best_fitnesses.csv"))
        else:
            #Not sure of best way to throw error
            print("***INVALID DATA REQUESTED***")
    return data

def get_data(common_dir):
    file_name = common_dir + "/pickled_data"
    try:
        data_file = open(file_name, "r")
        data = pickle.load(data_file)
        data_file.close()
        return data
    except:
        pass
    data_file = open(file_name, "w")
    #Make a new dictionary
    data = {}
    #For each sub directory...
    for sub_dir in os.listdir(common_dir):
        #If it's not actually a directory, skip it
        if not os.path.isdir(common_dir + "/" + sub_dir):
            continue
        #Grab the meaningful config name
        sub_dir_name_list = sub_dir.split("/")[-1].split("_")
        config = "_".join(sub_dir_name_list[:-2])
        #Make sure the config name is in the dictionary
        if config not in data:
            data[config] = []
        #Get Correlation
        with open(common_dir+"/"+sub_dir+"/correlation.dat") as infile:
            corr = float(infile.readline())
        #Merge the rest of the data into one dataframe, merging on generation
        #Get Generation, Average_Fitness, and Standard_Deviation
        df = pd.read_csv(common_dir+"/"+sub_dir+"/experienced_fitnesses.csv")
        #Get Ref_Average_Fitness and Ref_Standard_Deviation
        df = df.merge(pd.read_csv(common_dir+"/"+sub_dir+"/reference_fitnesses.csv"), on="Generation")
        #Get Best_Fitness and Best_Org
        df = df.merge(pd.read_csv(common_dir+"/"+sub_dir+"/experienced_best_fitnesses.csv"), on="Generation")
        #Get Ref_Best_Fitness and Ref_Best_Org
        df = df.merge(pd.read_csv(common_dir+"/"+sub_dir+"/reference_best_fitnesses.csv"), on="Generation")
        #Append the correlation and dataframe to the associated list
        data[config].append([corr, df])
    pickle.dump(data, data_file)
    data_file.close()
    return data

#Not corrected for use with the new data
def plot_single_run_over_time(single_run_data, directory):
    plt.clear()
    plt.plot(single_run_data["Generation"], np.log(single_run_data["Average_Fitness"]))
    plt.savefig(directory+"/single_run_over_time.png")

def plot_aggregate_over_time(data, key=None, directory="."):
    plt.clf()
    lines = {}
    for config in data:
        if (key != None and key not in config):
            continue
        series = []
        for run in range(len(data[config])):
            series.append(data[config][run][1]["Ref_Average_Fitness"])
        
        averages = []
        #stdevs = []

        for i in range(len(series[0])):
            add_factor = 0
            #if "rana" in config:
            #    add_factor = 20000
            logs = [np.log(s[i]+add_factor) for s in series]
            averages.append(sum(logs)/float(len(logs)))
        lines[config] = Line2D(data[config][0][1]["Generation"], averages)
    
        x = data[config][0][1]["Generation"]
        plt.plot(x, averages, hold=True, label=(config.split("_")[1]))
    plt.legend(loc="upper right")
    plt.xlabel("Generation")
    plt.ylabel("Log of Reference Average Fitness")
    #plt.figlegend([lines[l] for l in lines], [l for l in lines])
    plt.savefig(directory+"/runs_over_time_"+key+"_10000gen.png")

def plot_stddev_over_time(data, key=None, directory="."):
    plt.clf()
    lines = {}
    for config in data:
        if (key != None and key not in config):
            continue
        series = []
        for run in range(len(data[config])):
            series.append(data[config][run][1]["Ref_Standard_Deviation"])
        
        averages = []
        #stdevs = []

        for i in range(len(series[0])):
            add_factor = 0
            #if "rana" in config:
            #    add_factor = 20000
            devs = [s[i] for s in series]
            averages.append(sum(devs)/float(len(devs)))
        lines[config] = Line2D(data[config][0][1]["Generation"], averages)
    
        x = data[config][0][1]["Generation"]
        plt.plot(x, averages, hold=True, label=(config.split("_")[1]))
    plt.legend(loc="upper right")
    plt.xlabel("Generation")
    plt.ylabel("Log of Reference Average Fitness")
    #plt.figlegend([lines[l] for l in lines], [l for l in lines])
    plt.savefig(directory+"/diversity_over_time_"+key+"_10000gen.png")

def plot_average_final_fitness(data, key=None, directory="."):
    plt.clf()
    corrs = []
    finals = []
    
    for config in data:
        if key == None or key in config:
            for run in range(len(data[config])):
                corrs.append(data[config][run][0])
                add_factor=0
                #if "rana" in config:
                #    add_factor = 20000
                finals.append(add_factor+float(data[config][run][1]["Ref_Average_Fitness"][-1:]))
                #finals.append(float(data[config][run]["best_reference"]["Best_fitness"][-1:]))
    
    plt.plot(corrs, np.log(finals), ".")
    plt.xlabel("Correlation")
    plt.ylabel("Log of Reference Average Fitness")
    plt.savefig(directory+"/correlation_vs_final_fitness_scatter_"+key+".png")

if __name__ == "__main__":
    main()
        
