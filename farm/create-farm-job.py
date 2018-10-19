import argparse
import os
import glob
from string import Template


def main(args):
    # set all the values from input
    with open(args['template'], 'r') as f:
        src = Template(f.read())

    # sort the input files into groups
    n = int(args['grouping'])
    input_files = args['input_files']  # can be list
    input_files_final = []
    for i in range(0, len(input_files), n):
        input_files_final.append(input_files[i:i+n])

    # iterate the groups
    for item in input_files_final:
        data = args
        extras = {
            'command': 'root',
            'options': '-l -b -q --farm --hsdata ConvertHSHipoTriggerChain.C --hsin=./ --hsout=outfiles/',
            'other_files': '$HSANA/../Projects/hiporeader/ConvertHSHipoTriggerChain.C',
            'output_data': 'outfiles/*.root',
            'output_template': args['output_path'],
            'input_files': '\n'.join(item),
        }
        data.update(extras)
        print(src.substitute(data))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A program to create jsub files for ifarm jobs')
    parser.add_argument('-p', '--project',
                        help='Project name',
                        required=True)
    parser.add_argument('-tr', '--track',
                        help='Track name',
                        required=True)
    parser.add_argument('-i', '--input_files',
                        help='Full path to the input file(s)'
                             '(use * wildcard for multiple files',
                        required=True,
                        action='store',
                        nargs='+')
    parser.add_argument('-o', '--output_path',
                        help='Full path to the output directory',
                        required=True)
    parser.add_argument('-temp', '--template',
                        help='Template file to use',
                        required=True)
    parser.add_argument('-m', '--memory',
                        help='Memory request for job',
                        required=False,
                        default=2000)
    parser.add_argument('-mu', '--memory_unit',
                        help='Units for the memory request',
                        required=False,
                        default='MB')
    parser.add_argument('-d', '--diskspace',
                        help='Diskspace request for job',
                        required=False,
                        default=30)
    parser.add_argument('-du', '--diskspace_unit',
                        help='Units for the disk space request',
                        required=False,
                        default='GB')
    parser.add_argument('-os', '--os',
                        help='Operating system to use',
                        required=False,
                        default='centos7')
    parser.add_argument('-t', '--time',
                        help='Wall time for job (minutes)',
                        required=False,
                        default=60)
    parser.add_argument('-g', '--grouping',
                        help='Number of input files per job',
                        required=False,
                        default=2)
    args = vars(parser.parse_args())
    main(args)
