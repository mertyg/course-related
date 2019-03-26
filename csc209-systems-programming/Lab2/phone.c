#include <stdio.h>

int main(void){
  char string[11];
  int input;
  scanf("%s",string);
  scanf("%d",&input);
  if(input == -1){
    printf("%s\n",string);
    return 0;
  }
  else{
    if(input>=0 && input<=9){
      printf("%c",string[input]);
      return 0;
    }
    else{
      printf("ERROR\n");
      return 1;
    }
  }


}
