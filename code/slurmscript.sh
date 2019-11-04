#!/bin/bash
#
#SBATCH --job-name=gameoflife
#SBATCH --output=output.txt
#
#SBATCH --nodes=2

python3 -m pip install --upgrade pip --user
python3 -m pip install mpi4py --user
python3 -m pip install numpy --user
module load mpi/openmpi-x86_64
python -c "import mpi4py"
srun python3 helloworld.py