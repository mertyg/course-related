#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

int main(int argc, char **argv) {
    int i;
    int iterations;

    if (argc != 2) {
        fprintf(stderr, "Usage: forkloop <iterations>\n");
        exit(1);
    }
    int n;
    int done = 0;
    iterations = strtol(argv[1], NULL, 10);
    for (i = 0; i < iterations; i++) {
        if(done!=1){
            n = fork();
            done = 1;
            if(n==0){
                done = 0;
            }
        }
        if (n < 0) {
            perror("fork");
            exit(1);
        }
        printf("ppid = %d, pid = %d, i = %d\n", getppid(), getpid(), i);
    }

    int status;
    pid_t wpid;
    while ((wpid = wait(&status)) > 0);

    return 0;
}
