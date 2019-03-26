#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char **argv){
  if (argc>2){
    printf("USAGE: most_processes [ppid]\n");
    return 1;
  }
    int count=0,ppid,max_count=0;
    char str[1024];
    char uid[31],max_uid[31],prev_uid[31];
    int argv1;
    strcpy(prev_uid, "");
    if(argc==2){
      sscanf (argv[1],"%d",&argv1);
      //printf("%d",argv1);
    }
    while (1){
	if(fgets(str,1024,stdin)==NULL){
	if(max_count==0 && count ==0){
	  return 0;
	    }
	break;
	}
      sscanf(str,"%s %*d  %d %*s",uid,&ppid);
      
      if(argc==2 && ppid!=argv1){
        strcpy(uid,prev_uid);
	continue;
      }
      if(strcmp(uid,prev_uid)!=0){
	//printf("%s %s",uid,prev_uid);
	if(count>max_count){
	  strcpy(max_uid,prev_uid);
	  strcpy(prev_uid,uid);
	  max_count = count;
	  count=1;
	}
	else{
	  strcpy(prev_uid,uid);
	  count=1;
	}
      }
      else{
	count++;
      }
    }

      if(count > max_count){
	max_count = count;
	strcpy(max_uid,uid);
      }

      // printf("%s %d\n",uid,ppid);
      
    //printf("last line: %s\n",str);
    if(max_count==0){
      return 0;
    }
    printf("%s %d\n",max_uid,max_count);
    
  return 0;
}
