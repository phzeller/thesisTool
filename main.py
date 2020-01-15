#################################
#   written by Philipp Zeller   #
#################################

import time  # measure total run time of program
import cProfile, pstats, io
from pstats import SortKey
import io

import analyzeDirectory
import conf

# line profiling
import line_profiler
import atexit
profile = line_profiler.LineProfiler()
atexit.register(profile.print_stats)

# Credits to Sebastiaan Mathôt (https://www.youtube.com/watch?v=8qEnExGLZfY&t=915s) for the profile tutorial
# def profile(fnc):
#     def inner(*args, **kwargs):
#         pr = cProfile.Profile()
#         pr.enable()
#         retval = fnc(*args, **kwargs)
#         pr.disable()
#         s = io.StringIO()
#         sortby = SortKey.TIME
#         ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
#         ps.print_stats()
#         # print(s.getvalue())
#         with open('test.txt', 'w+') as f:
#             f.write(s.getvalue())
#
#         return retval
#     return inner


def main():
    print("Starting program:")
    start_time = time.time()

    with open(conf.output_fileName, mode="w",) as output_file:
        conf.output_file = output_file
        conf.create_csv_file()

        analyzeDirectory.processDirectory(conf.main_directory)

        conf.save_csv_file()


    print("No. of DMCA notices: " + str(conf.no_of_notices))
    print("time elapsed: {:.2f}s".format(time.time() - start_time))

if __name__ == '__main__':
    main()