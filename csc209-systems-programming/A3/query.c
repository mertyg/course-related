#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <sys/wait.h>
#include "freq_list.h"
#include "worker.h"
#define MAXPATHS 200


//Helper program for error_checking.
void error_check(int code, char *msg) {
    if(code<0) {
        perror(msg);
        exit(1);
    }
}


int main(int argc, char **argv) {
    char ch;
    char path[PATHLENGTH];
    char *startdir = ".";

    /* this models using getopt to process command-line flags and arguments */
    while ((ch = getopt(argc, argv, "d:")) != -1) {
        switch (ch) {
        case 'd':
            startdir = optarg;
            break;
        default:
            fprintf(stderr, "Usage: queryone [-d DIRECTORY_NAME]\n");
            exit(1);
        }
    }
    // Open the directory provided by the user (or current working directory)
    DIR *dirp;
    if ((dirp = opendir(startdir)) == NULL) {
        perror("opendir");
        exit(1);
    }

    /* For each entry in the directory, eliminate . and .., and check
     * to make sure that the entry is a directory, then call run_worker
     * to process the index file contained in the directory.
     * Note that this implementation of the query engine iterates
     * sequentially through the directories, and will expect to read
     * a word from standard input for each index it checks.
     */
    struct dirent *dp;
    char path_list[MAXPATHS][PATHLENGTH];
    int dir_count=0;
    while ((dp = readdir(dirp)) != NULL) {
        if (strcmp(dp->d_name, ".") == 0 ||
                strcmp(dp->d_name, "..") == 0 ||
                strcmp(dp->d_name, ".svn") == 0 ||
                strcmp(dp->d_name, ".git") == 0) {
            continue;
        }

        strncpy(path, startdir, PATHLENGTH);
        strncat(path, "/", PATHLENGTH - strlen(path));
        strncat(path, dp->d_name, PATHLENGTH - strlen(path));
        path[PATHLENGTH - 1] = '\0';
        struct stat sbuf;
        if (stat(path, &sbuf) == -1) {
            // This should only fail if we got the path wrong
            // or we don't have permissions on this entry.
            perror("stat");
            exit(1);
        }

        // Add the found path to the path_list. Later on we will run
        // run_worker on these paths.
        if (S_ISDIR(sbuf.st_mode)) {
            strcpy(path_list[dir_count],path);
            dir_count+=1;
        }
    }
    if(dir_count > MAXRECORDS) {
        fprintf(stderr,"Number of directories greater than MAXRECORDS\n");
        exit(2);
    }

    //Create file descriptors for pipes.
    //We need 2 pairs for each paths, because we will both write to and read
    //from each child.

    int fd1[dir_count][2],fd2[dir_count][2];
    int r,w,c1,c2;
    for(int i=0; i<dir_count; i++) {

        //for each path, first create pipes, then create a child.
        c1 = pipe(fd1[i]);
        error_check(c1,"pipe");
        c2 = pipe(fd2[i]);
        error_check(c2,"pipe");
        r = fork();
        error_check(r,"fork");

        if(r==0) {
            //Closing pipes for the children.
            c1 = close(fd2[i][0]);
            error_check(c1,"close");
            c2 = close(fd1[i][1]);
            error_check(c2,"close");

            //Close all the pipes from the previous children.
            for(int j=0; j<i; j++) {
                c1 = close(fd2[j][0]);
                error_check(c1,"close");
                c2 = close(fd1[j][1]);
                error_check(c2,"close");
            }
            //Run worker for each child. Then exit, since we do not want any extra children.
            run_worker(path_list[i],fd1[i][0],fd2[i][1]);
            exit(0);
        }
        else {
            //Handling pipes for parent.
            c1 = close(fd1[i][0]);
            error_check(c1,"close");
            c2 = close(fd2[i][1]);
            error_check(c2,"close");
        }
    }
    //input is the word that we will get as an input from stdin.
    char input[MAXWORD];
    FreqRecord *record = malloc(sizeof(FreqRecord));
    FreqRecord master_array[MAXRECORDS];
    int master_size, place;
    char *check;

    while(1) {
        //Get the word from stdin. If CTRL+D is pressed, break.
        //r = read(STDIN_FILENO,input,MAXWORD);
        check = fgets(input,MAXWORD,stdin);
        if(check==NULL) break;
        //input[r-1]='\0';
        r = strlen(input);
        input[r-1] = '\0';
        master_size = 0;

        //refresh the master_array, we do not want anything remaining from the previous iteration.
        for(int j=0; j<MAXRECORDS; j++) {
            master_array[j].freq = 0;
            strcpy(master_array[j].filename,"\0");
        }

        //Write the word to pipe, for each children to recieve it.
        for(int i=0; i<dir_count; i++) {
            w = write(fd1[i][1],input,MAXWORD);
            error_check(w,"write");
        }

        for(int i=0; i<dir_count; i++) {
            //For each children, read records from the pipe.
            r = read(fd2[i][0],record,sizeof(FreqRecord));
            error_check(r,"read");

            while(r>0) {
                //frequency being zero is an indicator of end-of-list.
                if(record->freq==0) {
                    break;
                }

                //we will try to find if the record is one of the top MAXRECORDS.
                //Below routine finds the place for each record.
                place = master_size;
                for(int pos=0; pos<master_size; pos++) {
                    if(record->freq > master_array[pos].freq) {
                        place = pos;
                        break;
                    }
                }
                if(place<MAXRECORDS) {
                    if(master_size<MAXRECORDS) {
                        master_array[master_size] = *record;
                        master_size+=1;
                    }
                    else {
                        master_array[MAXRECORDS-1] = *record;
                    }
                    //keeping the master_array sorted, utilizing cmprecord comparator func.
                    qsort(master_array,master_size,sizeof(FreqRecord),cmprecord);
                }
                r = read(fd2[i][0],record,sizeof(FreqRecord));
                error_check(r,"read");
            }

        }
        //printing the master_array to stdout.
        print_freq_records(master_array);
    }
    int status;
    for(int i=0; i<dir_count; i++) {
        //handling pipes and wait calls for each child.
        c1 = close(fd1[i][1]);
        error_check(c1,"close");
        c2 = close(fd2[i][0]);
        error_check(c2,"close");
        error_check(wait(&status),"wait");
    }
    //closing the directory and freeing the dynamically allocated
    error_check(closedir(dirp),"closedir");
    free(record);

    return 0;
}
