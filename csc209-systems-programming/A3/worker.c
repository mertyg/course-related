#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <dirent.h>
#include "freq_list.h"
#include "worker.h"


//Comparison helper function for qsort.
//Will be used for maintaining a sorted array.
int cmprecord(const void *a, const void *b) {
    FreqRecord *f1 = (FreqRecord*)a;
    FreqRecord *f2 = (FreqRecord*)b;
    return f2->freq-f1->freq;
}

//helper write and read functions handling error checks
int Write_freq(int fd, FreqRecord *record, int size) {
    int written = write(fd, record, sizeof(FreqRecord));
    if(written<0) {
        perror("write");
        exit(1);
    }
    return written;
}

int
Read(int fd, char*buf, int size) {
    int to_return = read(fd,buf,size);
    if(to_return<0) {
        perror("read");
        exit(1);
    }
    return to_return;
}

//More elegant malloc, handling error automatically.
//Credit: Dr. Michelle Craig.
void *
Malloc (int size)
{
    void *result = malloc (size);
    if (result == NULL)
    {
        perror ("Malloc error");
        exit (1);
    }
    return result;
}

//helper function for initializing a word.
void
set_word_null(char *word) {
    for(int i =0; i<MAXWORD; i++) {
        word[i] = '\0';
    }
}

/*
Returns an array of frequencies for a given word.
Returns a single item with 0 frequency if the word is not found.
If the item is found, returns an array of size MAXRECORDS+1.
*/
FreqRecord *get_word(char *word, Node *head, char **file_names) {
    //search is pointing to the head currently.
    Node *search = head;
    FreqRecord *toAdd;

    //We will continue searching until we are at the end, or we have found the word.
    while((search!=NULL) && (strcmp(search->word,word)!=0)) {
        search = search->next;
    }

    //the word is not found
    if(search==NULL) {
        toAdd = Malloc(sizeof(FreqRecord));
        if(toAdd==NULL) {
            perror("Malloc");
            exit(1);
        }
        toAdd[0].freq = 0;
        strcpy(toAdd[0].filename,"");
        return toAdd;
    }
    //the word is found
    toAdd = Malloc(sizeof(FreqRecord)*(MAXRECORDS+1));
    int j=0;
    for(int i=0; i<MAXRECORDS && file_names[i]!=NULL; i++) {
        if(search->freq[i]!=0) {
            toAdd[j].freq = search->freq[i];
            strncpy(toAdd[j].filename,file_names[i],PATHLENGTH);
            //printf("%s %s %d\n",toAdd[j].filename,search->word, search->freq[i]);
            j+=1;
        }
    }
    toAdd[j].freq = 0;
    strcpy(toAdd[j].filename,"");
    return toAdd;

}

/* Print to standard output the frequency records for a word.
* Use this for your own testing and also for query.c
*/
void print_freq_records(FreqRecord *frp) {
    int i = 0;

    while (frp != NULL && frp[i].freq != 0) {
        printf("%d    %s\n", frp[i].freq, frp[i].filename);
        i++;
    }
}

/* Complete this function for Task 2 including writing a better comment.
*/
void run_worker(char *dirname, int in, int out) {
    //initializing fields for the get_word function.
    char **filenames = init_filenames();
    Node *head = NULL;
    FreqRecord *record_list;
    int bytes_read, pos;
    char current[MAXWORD];
    char index_path[PATHLENGTH];
    char name_path[PATHLENGTH];

    //create the paths for index and filenames.
    strncpy(index_path,dirname,PATHLENGTH);
    strncpy(name_path,dirname,PATHLENGTH);
    strncat(index_path, "/index", PATHLENGTH - strlen(dirname) - 1);
    strncat(name_path, "/filenames", PATHLENGTH - strlen(dirname) - 1);

    //reading list using the utility function.
    read_list(index_path, name_path, &head, filenames);
    set_word_null(current);
    bytes_read = Read(in,current,MAXWORD);

    //if the in-pipe is closed, bytes_read will become 0 and we will break.
    while(bytes_read > 0) {
        current[bytes_read-1]='\0';
        record_list = get_word(current,head,filenames);
        pos = 0;
        while(record_list[pos].freq!=0) {
            //for each valid record, write a FreqRecord to the out pipe.
            Write_freq(out, &record_list[pos], sizeof(FreqRecord));
            pos+=1;
        }
        //write the final record, having freq = 0 and filename = ""
        Write_freq(out, &record_list[pos], sizeof(FreqRecord));
        bytes_read = Read(in,current,MAXWORD);
    }
}
