#################################
#   written by Philipp Zeller   #
#################################

import time  # measure total run time of program

import analyzeDirectory
import conf


def main():
    print("Starting program:")
    start_time = time.time()

    conf.createDataframe()
    analyzeDirectory.processDirectory(conf.main_directory)

    conf.write_to_csv()
    print("No. of DMCA notices: " + str(conf.no_of_notices))
    print("time elapsed: {:.2f}s".format(time.time() - start_time))

if __name__ == '__main__':
    main()
