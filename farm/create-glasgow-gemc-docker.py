import argparse
import getpass
import os
from datetime import datetime
from string import Template

# create a temp folder for the job in scratch (input and output)
# -> use some numbering considering multiple tasks on same machine
# copy across the input file for that task
# run the program on the input file, point to output folder
# copy output file to work area
# remove input and output files from farm node

# params to define
## input file(s), each input file will be a job
## output directory (on work), names must be unique
## number of events to process (optional)


def main(args):
    # load template file
    with open(args['template'], 'r') as f:
        src = Template(f.read())

    # prepare the input files
    input_files = args['input_files']  # can be a list
    jsub_filename = "gemc_docker_{:05d}.jsub"
    user = getpass.getuser()

    for i, item in enumerate(input_files):
        # set all the values for each input file
        output_filename = jsub_filename.format(i)
        input_path, input_file = os.path.split(item)
        data = args
        extras = {
            "input_file": input_file,
            "input_path": input_path,
            "user": user,
            "jobid": "{:05d}".format(i)
        }
        data.update(extras)

        # write out the jsub
        with open(output_filename, 'w') as f:
            f.write(src.substitute(data)+'\n')

        # print message for debugging, adding the output file to a list
        print("Created {}".format(output_filename))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=('A program to create GEMC Docker based jsub '
                     'files for the Glasgow farm'))
    parser.add_argument('-i', '--input_files',
                        help='Full path to the input file(s)'
                             '(use * wildcard for multiple files',
                        required=True,
                        action='store',
                        nargs='+')  # needed for multiple inputs
    parser.add_argument('-o', '--output_dir',
                        help='Full path to the output directory',
                        required=True)
    parser.add_argument('-t', '--template',
                        help='Template file to use',
                        required=True)
    parser.add_argument('-n', '--events',
                        help='Number of events to read from the input file',
                        required=False,
                        default=100000000)
    parser.add_argument('-r', '--runid',
                        help='ID for the run',
                        required=False,
                        default=11)
    parser.add_argument('-to', '--torus',
                        help='Value for the torus setting, match gcard',
                        required=False,
                        default=-1.0)
    parser.add_argument('-so', '--solenoid',
                        help='Value for the solenoid setting, match gcard',
                        required=False,
                        default=-1.0)
    parser.add_argument('-g', '--gcard',
                        help='Path to the gcard to use with GEMC',
                        required=False,
                        default="/jlab/work/clas12.gcard")
    parser.add_argument('-tc', '--threads',
                        help='Number of threads to use with clara',
                        required=False,
                        default=1)
    parser.add_argument('--memory',
                        help='Memory request for job',
                        required=False,
                        default=2000)
    parser.add_argument('--diskspace',
                        help='Diskspace request for job',
                        required=False,
                        default=30)
    args = vars(parser.parse_args())
    main(args)
