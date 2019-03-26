#include <stdio.h>

int main(void){
  char string[11];
  int input;
  int error_count=0;
  scanf("%s",string);

  while(scanf("%d",&input)!= EOF){
  if(input == -1){
    printf("%s\n",string);
  }
  else{
    if(input>=0 && input<=9){
      printf("%c\n",string[input]);
    }
    else{
      printf("ERROR\n");
      error_count+=1;
    }
  }
  }

  return error_count==0 ? 0 : 1;
}
