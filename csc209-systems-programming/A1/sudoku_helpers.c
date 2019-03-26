#include <stdio.h>
#include <stdlib.h>

/* Each of the n elements of array elements, is the address of an
 * array of n integers.
 * Return 0 if every integer is between 1 and n^2 and all
 * n^2 integers are unique, otherwise return 1.
 */

#include <stdio.h>

int check_group(int **elements, int n) {
    // TODO: replace this return statement with a real function body
    int total[n*n];
    int limit = n*n;
    int curr;
    for(int i=0;i<limit;i++){
      total[i]=0;
    }
    for(int i=0;i<n;i++){
      for(int j=0;j<n;j++){
      curr = elements[i][j];
      if(curr<1 || curr>limit){
	    return 1;
      }
      if(total[curr-1]++!=0){
	    return 1;
      }
    }
    }
    return 0;
}

/* puzzle is a 9x9 sudoku, represented as a 1D array of 9 pointers
 * each of which points to a 1D array of 9 integers.
 * Return 0 if puzzle is a valid sudoku and 1 otherwise. You must
 * only use check_group to determine this by calling it on
 * each row, each column and each of the 9 inner 3x3 squares
 */
int check_regular_sudoku(int **puzzle) {
    // TODO: replace this return statement with a real function body
  int *elements_rows[3];
  int *elements_cols[3];
  int *elements_groups[3];
  for(int i=0;i<3;i++){
      elements_rows[i]=malloc(3*sizeof(int));
      elements_cols[i]=malloc(3*sizeof(int));
      elements_groups[i]=malloc(3*sizeof(int));
  }
  int curr_result;
  for(int i=0;i<9;i++){
    curr_result=0;
    for(int j=0;j<3;j++){
      for(int k=0;k<3;k++){
	elements_rows[j][k]=puzzle[i][3*j+k];
	elements_cols[j][k]=puzzle[3*j+k][i];
	elements_groups[j][k]=puzzle[j+3*(i/3)][k+(i%3)*3];
      }
    }
    curr_result+=check_group(elements_rows,3);
    curr_result+=check_group(elements_cols,3);
    curr_result+=check_group(elements_groups,3);
    if(curr_result!=0){
      return 1;
    }
  }
    return 0;
}
