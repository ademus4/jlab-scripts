# Indirect (templates)

The scripts in this folder can be used to generate submission files to be used with the batch system (PBS) for running jobs on the farm.

An example of generating qsub files that use Singularity to run GEMC and the HIPO post-processing and reconstruction:
```
#!/usr/bin/env bash
python3 create-glasgow-gemc-singularity.py \
    -i /my/lund/files/*.ld \
    -c ./configs.ini
```

The input event files should be in LUND format. The config file contains the parameters used by GEMC, CLARA etc. The script will loop though
all the configurations set inside the config file.

# Direct (subprocess)

A general example of submitting a qsub job using the 'submit-generic-job.py' script is as follows:
```
#!/usr/bin/env bash
python3 submit-generic-job.py \
    -c "echo 'hello farm world'" \
    -e myuser@myinstitute.com
```

This will submit the command given to the PBS batch system using subprocess to call the qsub command and run on a random node. 
This example is based on the template "./templates/pbs_example.txt", which can be modified to suit the users need.
