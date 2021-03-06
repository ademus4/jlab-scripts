import argparse
import configparser
import getpass
import os
from datetime import datetime
from glob import glob
from string import Template

  
def main(args):
    # load configuration file
    config = configparser.ConfigParser()
    config.read(args['config'])

    # prepare the input files
    jsub_filename = "gemc_singularity_{:05d}.qsub"
    user = getpass.getuser()
    
    for section in config.sections():
        # load template file
        with open(config[section]['template'], 'r') as f:
            src = Template(f.read())


        input_files = glob(os.path.join(config[section]['input_dir'], '*.ld'))
        for i, item in enumerate(input_files):
            # set all the values for each input file
            output_filename = section + '_' + jsub_filename.format(i)
            output_filename = os.path.join(config[section]['qsub_dir'], output_filename)
            input_path, input_file = os.path.split(item)
            data = config[section]
            extras = {
                "input_file": input_file,
                "input_path": input_path,
                "output_name": input_file.split('.')[0],
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
        description=('A program to create GEMC Singularity based jsub '
                     'files for the Glasgow farm'))
    parser.add_argument('-c', '--config',
                        help='Path to the configuration file',
                        required=True)
    args = vars(parser.parse_args())
    main(args)
