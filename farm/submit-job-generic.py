import argparse
import getpass
import os
import subprocess
from datetime import datetime
from string import Template

def main(args):
    # load template file
    with open("./templates/pbs_example.txt", 'r') as f:
        src = Template(f.read())
    
    i=0
    data = args
    extras = {
        "jobid": "{:05d}".format(i)
    }
    data.update(extras)
    command = src.substitute(data)

    # run the job
    proc = subprocess.Popen(['qsub'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            encoding='utf8'
    )
    stdout_value = proc.communicate(command)
    print(stdout_value[0])



if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=('Submit qsub jobs direct from subprocess'))
    parser.add_argument('-c', '--command',
                        help='Command to submit to PBS',
                        required=True,
                        action='store')
    parser.add_argument('-e', '--email',
                        help='Email address for job messages',
                        required=True)
    args = vars(parser.parse_args())
    main(args)
