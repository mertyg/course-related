/* The purpose of this program is to practice writing signal handling
 * functions and observing the behaviour of signals.
 */

#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/time.h>

/* Message to print in the signal handling function. */
#define MESSAGE "%ld reads were done in %ld seconds.\n"

/* Global variables to store number of read operations and seconds elapsed. 
 */
long num_reads, seconds;

void pSigHandler(int signo){
    fprintf(stderr,"%ld reads were done in %ld seconds.\n",num_reads,seconds);
    exit(0);
}

/* The first command-line argument is the number of seconds to set a timer to run.
 * The second argument is the name of a binary file containing 100 ints.
 * Assume both of these arguments are correct.
 */

int main(int argc, char **argv) {
    if (argc != 3) {
        fprintf(stderr, "Usage: time_reads s filename\n");
        exit(1);
    }
    seconds = strtol(argv[1], NULL, 10);
    FILE *fp;
    if ((fp = fopen(argv[2], "r")) == NULL) {
      perror("fopen");
      exit(1);
    }

    /* In an infinite loop, read an int from a random location in the file,
     * and print it to stderr.
     */
    //( void * ptr, size_t size, size_t count, FILE * stream )
    int num,new_pos,r;
    struct itimerval timer ;
    timer.it_value.tv_sec = seconds;
    timer.it_value.tv_usec = 0;
    timer.it_interval.tv_sec = 0;
    timer.it_interval.tv_usec = 0;
    setitimer(ITIMER_PROF, &timer, NULL);
    struct sigaction handle;
    handle.sa_handler = pSigHandler;
    sigaction(SIGPROF, &handle, NULL);
    for (;;) {
        new_pos = random()%100;
        fseek(fp,new_pos*sizeof(int),SEEK_SET);
        r = fread(&num,sizeof(int),1,fp);
        if(r<0){
            perror("read");
            exit(1);
        }
        fprintf(stderr,"%d\n",num);
        num_reads+=1;
    }
    return 1; // something is wrong if we ever get here!
}
