#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>

#define MAXLINE 256
#define MAX_PASSWORD 10

#define SUCCESS "Password verified\n"
#define INVALID "Invalid password\n"
#define NO_USER "No such user\n"

int main(void) {
  char user_id[MAXLINE];
  char password[MAXLINE];
  char input[MAXLINE];
  int status,check, fd[2];

  if(fgets(user_id, MAXLINE, stdin) == NULL) {
      perror("fgets");
      exit(1);
  }
  if(fgets(password, MAXLINE, stdin) == NULL) {
      perror("fgets");
      exit(1);
  }

  strncpy(input,user_id,MAX_PASSWORD);
  for(int i=0;i<MAX_PASSWORD-strlen(user_id);i++){
    strcat(input,"\n");
  }
  strncat(input,password,MAX_PASSWORD);

  if(pipe(fd)){
    perror("pipe error");
    return -1;
  }

  int n = fork();
  if(n==-1){
    perror("fork");
    return -1;
  }
  else if(n==0){
    check = close(fd[1]);
    if(check==-1){
        perror("close");
        return -1;
    }
    dup2(fd[0],STDIN_FILENO);
    check = close(fd[0]);
    if(check==-1){
        perror("close");
        return -1;
    }
    execl("./validate","validate",NULL);
  }
  else{
    check = close(fd[0]);
    if(check==-1){
        perror("close");
        return -1;
    }
    check = write(fd[1],input,sizeof(input));
    if(check==-1){
        perror("write");
        return -1;
    }
    check = close(fd[1]);
    if(check==-1){
        perror("close");
        return -1;
    }
    wait(&status);
    if(WIFEXITED(status)){
        int exit_stat = WEXITSTATUS(status);
        switch(exit_stat){
            case 0:
                printf("%s\n",SUCCESS);
                break;
            case 2:
                printf("%s\n",INVALID);
                break;
            case 3:
                printf("%s\n",NO_USER);
                break;
            default:
                printf("%s%d\n",input,exit_stat);
        }
    }
  }
  


  return 0;
}
