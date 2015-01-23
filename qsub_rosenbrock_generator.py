import sys
import itertools
from subprocess import call

array_size = 100

def convert_config_file_name_to_job(file_name, output_dir_base):
    return "python changing_environment_ga.py -c {0} -o {1}/{0}_${{PBS_ARRAYID}}".format(file_name, output_dir_base)

common = """
#!/bin/bash -login

#PBS -l walltime=3:30:00
#PBS -l nodes=1:ppn=1
#PBS -l mem=1gb
#PBS -N changing_environment_test
#PBS -t 1-{0}

module load NumPy
module load SciPy

cd ~/ChangingEnvironmentGA
""".format(array_size)


config_common = """
[DEFAULT]
fitness_function_type = {0}
number_of_organisms = 500
mutation_rate = 0.20
number_of_generations = {2}
org_type = vector
length = 200
range_minimum = -2.048
range_maximum = 2.048
tournament_size = 10
mutation_effect_size = .1
alternate_environment_corr = {1}
verbose = False
crowding = False
"""

alt_corrs = [-1, 0, 1]
#function_types = ["schafferf7"]
function_types = ["rosenbrock"]
#alt_corrs = [-.99, .99]
#alt_corrs = [1]
num_gens = [2500]
def write_to_file(filename, contents):
    with open(filename, "w") as file_handle:
        file_handle.write(contents)


if __name__ == "__main__":
    config_files = []

    for function_type, alt_corr, gen in itertools.product(function_types, alt_corrs, num_gens):
        config_filename = "{0}_{1}_{2}gen.ini".format(function_type, alt_corr, gen)
        contents = config_common.format(function_type, alt_corr, gen)
        write_to_file(config_filename, contents)
        config_files.append(config_filename)

    output_dir_base = "rosenbrock"
    jobs = [convert_config_file_name_to_job(name, output_dir_base) for name in config_files]


    for job in jobs:
        contents = common + "\n" + job + "\n"
        write_to_file("tmp.sub", contents)
        print "----------Submitting----------"
        print contents
        call(["qsub", 'tmp.sub'])
        call(["rm", 'tmp.sub']) 
