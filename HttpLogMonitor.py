# HTTPLogMonitor is the main prog which takes two arguments sample log file and the config file
#Command to Run: python HttpLogMonitor.py --input_file <logfile> --config_file <config file  optional argument >

import sys
import argparse
from os import path
from Parser import Parser
from Config import Config

def main():
    argops = argparse.ArgumentParser()
    # add long and short argument
    argops.add_argument("--input_file", "-i", help="input log file")
    argops.add_argument("--config_file", "-c", help="config file with options for the system")
    # read arguments from the command line
    args = argops.parse_args()
    filePath=""
    configFile=""
    if args.input_file:
        if path.isfile(args.input_file):
            filePath=args.input_file
        else:
            print("Please provide a valid log file")
            sys.exit(1)
    else:
        argops.print_help(sys.stderr)
        sys.exit(1)

    config=Config()# Pass a file as argument here 
    if args.config_file: #config file is a optional parameter
        configFile=args.config_file
        config.populate(configFile)
           
    parser_= Parser(filePath,config)
    parser_.Process()



if __name__ == "__main__":
        main()

