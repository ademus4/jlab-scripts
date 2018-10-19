import argparse
import os
import glob
from string import Template


def main(args):
    # set all the values from input
    with open(args['template'], 'r') as f:
        src = Template(f.read())

    input_path = args['input_file']
    base, filename = os.path.split(input_path)

    # check if a wildcard has been used to match files
    # otherwise just use input file
    input_files = []
    if '*' in filename:
        matches = glob.glob(os.path.join(base, filename))
        print(base, filename)
        for item in matches:
            input_files.append(item)
    else:
        input_files.append(os.path.join(base, filename))
    print(input_files)

    n = args['grouping']
    input_files_final = []
    for i in range(0, len(input_files), n):
        input_files_final.append(input_files[i:i+n])

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
    parser.add_argument('-i', '--input_file',
                        help='Full path to the input file \
                             (use * wildcard for multiple files',
                        required=True)
    #parser.add_argument('pattern', type=file, action='store', nargs='+')
    parser.add_argument('-o', '--output_path',
                        help='Full path to the output directory',
                        required=True)
    parser.add_argument('-temp', '--template',
                        help='Template file to use',
                        required=True)
    parser.add_argument('-g', '--grouping',
                        help='Number of input files per job',
                        required=False,
                        default=2)
    args = vars(parser.parse_args())
    main(args)
