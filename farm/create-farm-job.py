import argparse
import os
import glob
from pprint import pprint
from lxml import etree


def main(args):
    # set all the values from input
    root = etree.Element("Request")
    etree.SubElement(root, "Project",
                     name=args['project'])
    etree.SubElement(root, "Track",
                     name=args['track'])
    etree.SubElement(root, "Memory",
                     space=str(args['memory']), unit=args['memory_unit'])
    etree.SubElement(root, "Diskspace",
                     space=str(args['diskspace']), unit=args['diskspace_unit'])
    etree.SubElement(root, "OS",
                     name=args['os'])
    etree.SubElement(root, "TimeLimit",
                     time=str(args['time']), units="minutes")

    command = etree.SubElement(root,"Command")
    command.text = etree.CDATA("root -l -b -q "
                               "--farm "
                               "--hsdata ConvertHSHipoTriggerChain.C "
                               "--hsin=./ "
                               "--hsout=outfiles/")
    etree.SubElement(root, "Input",
                     src="$HSANA/../Projects/hiporeader/ConvertHSHipoTriggerChain.C",
                     dest="ConvertHSHipoTriggerChain.C")

    # set the job input and output
    input_path = args['input_file']
    output_path = args['output_path']
    base, filename = os.path.split(input_path)
    input_files = []
    if '*' in filename:
        # write logic for file searching (glob library)
        raise ValueError('Wildcards not implemented yet!')
    else:
        input_files.append(os.path.join(base, filename))

    for item in input_files:
        job = etree.SubElement(root, "Job")
        etree.SubElement(job, "Input",
                         src=item,
                         dest="infile")
        etree.SubElement(job, "Output",
                         src=os.path.join("outfiles", os.path.split(item)[1] + ".root"),
                         dest=output_path)

    # write to file
    print(etree.tostring(root, pretty_print=True))


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
    parser.add_argument('-o', '--output_path',
                        help='Full path to the output directory',
                        required=True)

    args = vars(parser.parse_args())
    main(args)
