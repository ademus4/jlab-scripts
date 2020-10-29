import argparse
import getpass
import os
from datetime import datetime
from string import Template


def main(args):
    # load template file
    with open(args['template'], 'r') as f:
        src = Template(f.read())

    # prepare the input files
    input_files = args['input_files']  # can be a list
    output_dir = args['output_dir']
    jsub_filename = "finalstate_{:05d}.qsub"
    user = getpass.getuser()

    for i, item in enumerate(input_files):
        # set all the values for each input file
        output_filename = os.path.join(args['job_file_dir'], jsub_filename.format(i))
        data = args
        extras = {
            "input_file": item,
            "output_dir": output_dir,
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
        description=('A program to create finalstate jsub '
                     'files for the Glasgow farm'))
    parser.add_argument('-i', '--input_files',
                        help='Full path to the input file(s)'
                             '(use * wildcard for multiple files',
                        required=True,
                        action='store',
                        nargs='+')
    parser.add_argument('-o', '--output_dir',
                        help='Full path to the job output directory',
                        required=True)
    parser.add_argument('-c', '--config',
                        help='Full path to the chanser config file',
                        required=True)
    parser.add_argument('-j', '--job_file_dir',
                        help='Full path for the job files to be saved',
                        required=True)
    parser.add_argument('-t', '--template',
                        help='Template file to use',
                        required=True)
    parser.add_argument('-e', '--email',
                        help='Email address for job messages',
                        required=False)
    args = vars(parser.parse_args())
    main(args)
