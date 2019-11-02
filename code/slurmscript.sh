#!/bin/sh
#SBATCH --nodes=2
#SBATCH --job-name="hello_test"
#SBATCH --output=test-srun.out
# The initial srun will trigger the SLURM prologue on the compute nodes.
echo "SLURM_JOBID="$SLURM_JOBID
echo "SLURM_JOB_NODELIST"=$SLURM_JOB_NODELIST
echo "SLURM_NNODES"=$SLURM_NNODES
echo "SLURMTMPDIR="$SLURMTMPDIR
echo "working directory = "$SLURM_SUBMIT_DIR
NPROCS=`srun --nodes=${SLURM_NNODES} bash -c 'hostname' |wc -l`
echo NPROCS=$NPROCS
srun --nodes=${SLURM_NNODES} bash -c 'hostname'
echo "Launch helloworld with srun"

#The PMI library is necessary for srun
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
srun ./hello
#
echo "All Done!"
