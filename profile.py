import cProfile
import pstats
import main
import changing_environment_ga

args = "\"-c vector_config.ini -o profile_junk_data\""

cProfile.run("changing_environment_ga.main(" + args + ")", None, "time")
