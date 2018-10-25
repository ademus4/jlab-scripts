import argparse
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

    jsub_filename = "run_{}_submitHSToFarm".format(args['run'])

    # iterate the groups
    output_filesnames = []
    for i, item in enumerate(input_files_final):
        # set all the values for each input file
        output_filename = jsub_filename + "_{}.jsub".format(i)
        data = args

        # check if DSTs are being used
        if args['dst']:
            command_file = 'ConvertHipoDSTChain.C'
        else:
            command_file = 'ConvertHSHipoTriggerChain.C'

        # build command options
        options = '-l -b -q --farm --hsdata {} ' \
                  '--hsin=./ --hsout=outfiles/'.format(command_file)
        other_files = '$HSANA/../Projects/hshiporeader/{}'.format(command_file)

        extras = {
            'command': 'root',
            'options': options,
            'other_files': other_files,
            'output_data': 'outfiles/*.root',
            'output_template': args['output_path'],
            'input_files': '\n'.join(item),
        }
        data.update(extras)

        # write each group of input files to a separate file
        with open(output_filename, 'w') as f:
            f.write(src.substitute(data)+'\n')

        # print message for debugging, adding the output file to a list
        print("Created {}".format(output_filename))
        output_filesnames.append(output_filename)

    # create a file for running all jsub input files
    run_filename = 'do_run_{}'.format(args['run'])
    with open(run_filename, 'w') as f:
        for line in output_filesnames:
            f.write("jsub {}".format(line) + '\n')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='A program to create jsub files for ifarm jobs')
    parser.add_argument('-p', '--project',
                        help='Project name',
                        required=True)
    parser.add_argument('-k', '--track',
                        help='Track name',
                        required=True)
    parser.add_argument('-i', '--input_files',
                        help='Full path to the input file(s)'
                             '(use * wildcard for multiple files',
                        required=True,
                        action='store',
                        nargs='+')  # needed for multiple inputs
    parser.add_argument('-o', '--output_path',
                        help='Full path to the output directory',
                        required=True)
    parser.add_argument('-t', '--template',
                        help='Template file to use',
                        required=True)
    parser.add_argument('-r', '--run',
                        help='Run number associated with input files '
                             '(only used for output jsub file names)',
                        required=True)
    parser.add_argument('--memory',
                        help='Memory request for job',
                        required=False,
                        default=2000)
    parser.add_argument('--memory_unit',
                        help='Units for the memory request',
                        required=False,
                        default='MB')
    parser.add_argument('--diskspace',
                        help='Diskspace request for job',
                        required=False,
                        default=30)
    parser.add_argument('--diskspace_unit',
                        help='Units for the disk space request',
                        required=False,
                        default='GB')
    parser.add_argument('--os',
                        help='Operating system to use',
                        required=False,
                        default='centos7')
    parser.add_argument('--time',
                        help='Wall time for job (minutes)',
                        required=False,
                        default=60)
    parser.add_argument('--grouping',
                        help='Number of input files per job',
                        required=False,
                        default=2)
    parser.add_argument('--dst',
                        help='Add if processing DSTs instead of raw data',
                        required=False,
                        action='store_true')
    args = vars(parser.parse_args())
    main(args)
