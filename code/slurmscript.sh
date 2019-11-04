#!/bin/bash
#
#SBATCH --job-name=helloworld
#SBATCH --output=results.out
#
#SBATCH --nodes=2

python3 -m pip install --upgrade pip --user
python3 -m pip install mpi4py --user
python3 -m pip install numpy --user
module load mpi/openmpi-x86_64
python3 -c "import mpi4py"
mpirun python3 helloworld.py