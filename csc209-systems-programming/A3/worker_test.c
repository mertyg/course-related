#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>

#include "freq_list.h"
#include "worker.h"

int main(int argc, char **argv) {
    Node *head = NULL;
    char **filenames = init_filenames();
    char arg;
    char *listfile = "index";
    char *namefile = "filenames";
    char *word = "desert";
    /* an example of using getop to process command-line flags and arguments */
    while ((arg = getopt(argc,argv,"i:n:w:")) > 0) {
        switch(arg) {
        case 'i':
            listfile = optarg;
            break;
        case 'n':
            namefile = optarg;
            break;
        case 'w':
            word = optarg;
        default:
            fprintf(stderr, "Usage: printindex [-i FILE] [-n FILE]\n");
            exit(1);
        }
    }
    read_list(listfile, namefile, &head, filenames);
    FreqRecord *words;
    words = get_word(word, head, filenames);
    int i = 0;
    //Prints the filename - frequency tuples.
    while(words[i].freq!=0){
        printf("%s %d\n",words[i].filename,words[i].freq);
        i+=1;
    }
    return 0;
}
