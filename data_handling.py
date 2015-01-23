import csv
import os
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
#import scipy.stats as stats

def main():
    test_dir = "RTR"
    data = get_data(test_dir)
    plot_aggregate_over_time(data, "deceptive", test_dir)
    plot_stddev_over_time(data, "deceptive", test_dir)
    plot_average_final_fitness(data, "deceptive", test_dir)
    #plot_single_run_over_time(data[data.keys()[0]]["1"]["average_experienced"], test_dir)
    #print data.keys()[0]

def get_data(common_dir):
    data = {}
    for d in os.listdir(common_dir):
        if not os.path.isdir(common_dir + "/" + d):
            continue

        dir_name_list = d.split("/")[-1].split("_")
        idnum = dir_name_list[-1]
        config = "_".join(dir_name_list[:-1])

        if config in data:
            data[config][idnum] = {}
        else:
            data[config] = {}
            data[config][idnum] = {}

        with open(common_dir+"/"+d+"/correlation.dat") as infile:
            data[config][idnum]["correlation"] = float(infile.readline())

        data[config][idnum]["average_experienced"] = \
            pd.read_csv(common_dir+"/"+d+"/experienced_fitnesses.csv")
        data[config][idnum]["average_reference"] = \
            pd.read_csv(common_dir+"/"+d+"/reference_fitnesses.csv")
        data[config][idnum]["best_experienced"] = \
            pd.read_csv(common_dir+"/"+d+"/experienced_best_fitnesses.csv")
        data[config][idnum]["best_reference"] = \
            pd.read_csv(common_dir+"/"+d+"/reference_best_fitnesses.csv")

    return data

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
        for run in data[config]:
            series.append(data[config][run]["average_reference"]["Average_Fitness"])
        
        averages = []
        #stdevs = []

        for i in range(len(series[0])):
            add_factor = 0
            if "rana" in config:
                add_factor = 20000
            logs = [np.log(s[i]+add_factor) for s in series]
            averages.append(sum(logs)/float(len(logs)))
        lines[config] = Line2D(data[config][data[config].keys()[0]]["average_reference"]["Generation"], averages)
    
        x = data[config][data[config].keys()[0]]["average_reference"]["Generation"]
        plt.plot(x, averages, hold=True, label=config)
    plt.legend(loc="upper right")
    plt.xlabel("Generation")
    plt.ylabel("Average Fitness")
    #plt.figlegend([lines[l] for l in lines], [l for l in lines])
    plt.savefig(directory+"/runs_over_time_"+key+"_2500gen.png")

def plot_stddev_over_time(data, key=None, directory="."):
    plt.clf()
    lines = {}
    for config in data:
        if (key != None and key not in config):
            continue
        series = []
        for run in data[config]:
            series.append(data[config][run]["average_reference"]["Standard_Deviation"])
        
        averages = []
        #stdevs = []

        for i in range(len(series[0])):
            add_factor = 0
            if "rana" in config:
                add_factor = 20000
            devs = [s[i] for s in series]
            averages.append(sum(devs)/float(len(devs)))
        lines[config] = Line2D(data[config][data[config].keys()[0]]["average_reference"]["Generation"], averages)
    
        x = data[config][data[config].keys()[0]]["average_reference"]["Generation"]
        plt.plot(x, averages, hold=True, label=config)
    plt.legend(loc="upper right")
    plt.xlabel("Generation")
    plt.ylabel("Average Fitness")
    #plt.figlegend([lines[l] for l in lines], [l for l in lines])
    plt.savefig(directory+"/diversity_over_time_"+key+"_2500gen.png")

def plot_average_final_fitness(data, key=None, directory="."):
    plt.clf()
    corrs = []
    finals = []
    
    for config in data:
        if key == None or key in config:
            for run in data[config]:
                corrs.append(data[config][run]["correlation"])
                add_factor=0
                if "rana" in config:
                    add_factor = 20000
                finals.append(add_factor+float(data[config][run]["average_reference"]["Average_Fitness"][-1:]))
                #finals.append(float(data[config][run]["best_reference"]["Best_fitness"][-1:]))
    
    plt.plot(corrs, np.log(finals), ".")
    plt.xlabel("Correlation")
    plt.ylabel("Average Fitness")
    plt.savefig(directory+"/correlation_vs_final_fitness_scatter_"+key+".png")

if __name__ == "__main__":
    main()
        
