/*The Parallel Hello World Program*/
#include <mpi.h>
#include <stdio.h>

main(int argc, char** argv) {
  int node;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &node);

  printf("Hello World from Node %d\n", node);

  MPI_Finalize();
}
