#! /usr/bin/env bash
#
#SBATCH --job-name=labelling
#SBATCH --output=output.out
#
#SBATCH --ntasks=1
#SBATCH --nodelist=a100-002
#SBATCH --time=20:00 # this sets the maximum time the job is allowed before killed

#SBATCH --partition=a100
##SBATCH --partition=cpu # the double hash means that SLURM won't read this line.

# load the python module
module load Python/Python3.10 # make sure to load the modules needed

python3.10 labelling.py # the program that is run

