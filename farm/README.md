The scripts in this folder can be used to generate submission files to be used with the batch system (PBS) for running jobs on the farm.

An example of generating qsub files that use Singularity to run GEMC and the HIPO post-processing and reconstruction:
```
#!/usr/bin/env bash
python3 create-glasgow-gemc-singularity.py \
    -c ./configs.ini
```

The config file contains the parameters used by GEMC, CLARA etc. The script will loop though all the configurations set inside the config file. See the example config file to check the parameters to set.
