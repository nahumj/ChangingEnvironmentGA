import sys
import itertools
from subprocess import call
import datetime

array_size = 40
walltime = "03:59:00"
today = "{0:%Y}_{0:%B}_{0:%d}".format(datetime.datetime.now())
alt_corrs = [-1, -.99, -0.8, -0.5, -0.25, 0, 0.25, 0.5, 0.8, .99, 1]
#function_types = ["schafferf7"]
function_types = ["sphere", "rana"]
#alt_corrs = [-.99, .99]
#alt_corrs = [1]
num_gens = [10000]
num_runs_per_job = 2
output_dir_base = "length_100_" + today

common = """
#!/bin/bash -login

#PBS -l walltime={1}
#PBS -l nodes=1:ppn=1
#PBS -l mem=1gb
#PBS -N changing_environment_{2}
#PBS -t 1-{0}

module load NumPy
module load SciPy

cd ~/ChangingEnvironmentGA
""".format(array_size, walltime, today)


config_common = """
[DEFAULT]
fitness_function_type = {0}
number_of_organisms = 500
mutation_rate = 0.20
number_of_generations = {2}
org_type = vector
length = 100
range_minimum = -512
range_maximum = 512
tournament_size = 10
mutation_effect_size = 10
alternate_environment_corr = {1}
verbose = False
crowding = False
"""

def convert_config_file_name_to_job_string(file_name, output_dir_base):
    common_name = "python changing_environment_ga.py -c {0} -o {1}/{0}_arr${{PBS_ARRAYID}}".format(
        file_name, output_dir_base)
    result = [common_name + "_run{}".format(run_number) for run_number in range(num_runs_per_job)]
    return "\n".join(result)

def write_to_file(filename, contents):
    with open(filename, "w") as file_handle:
        file_handle.write(contents)

def start_runs(jobs, submit_jobs=True, print_jobs=True):
    for job in jobs:
        contents = common + "\n" + job + "\n"
        write_to_file("tmp.sub", contents)
        if print_jobs:
            print("----------Submitting----------")
            print(contents)
        if submit_jobs:
            call(["qsub", 'tmp.sub'])
            call(["rm", 'tmp.sub']) 
    
def create_config_files():
    config_files = []
    for function_type, alt_corr, gen in itertools.product(function_types, alt_corrs, num_gens):
        config_filename = "{0}_{1}_{2}gen.ini".format(function_type, alt_corr, gen)
        contents = config_common.format(function_type, alt_corr, gen)
        write_to_file(config_filename, contents)
        config_files.append(config_filename)
    return config_files

if __name__ == "__main__":
    config_files = create_config_files()
    jobs = [convert_config_file_name_to_job_string(name, output_dir_base) for name in config_files]
    start_runs(jobs, submit_jobs=True, print_jobs=True)
