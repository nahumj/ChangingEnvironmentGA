import cProfile
import pstats
import main
import changing_environment_ga

for i in range(10):
    args = "\"-c vector_config.ini -o multiprofile_junk_data/%d\"" % i
    filename = "multiprofile_junk_data/profile_stats_%d.stats" % i
    cProfile.run("changing_environment_ga.main(" + args + ")", filename)
stats = pstats.Stats("multiprofile_junk_data/profile_stats_0.stats")
for i in range(1, 10):
    stats.add("multiprofile_junk_data/profile_stats_%d.stats" % i)
stats.strip_dirs()
stats.sort_stats('time')
stats.print_stats()
