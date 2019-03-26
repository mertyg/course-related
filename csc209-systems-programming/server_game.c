#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <netinet/in.h>    /* Internet domain header */
#include <arpa/inet.h>     /* only needed on my mac */

// change this value to customize the port per student (step 2)
#define PORT 59194
#define LEGO_PIECES 10

/* read and return a valid move from socket
 * a valid move is a text integer between 1 and 3 followed by a \r\n)
 * 
 * Hint: read from the socket into a buffer, loop over the buffer
 *   until you find \r\n and then replace the \r with \0 to make a 
 *   string. Then use strtol to convert to an integer. If the result
 *   isn't in range, write a message to the socket and repeat. 
 */
int read_a_move(int socket) {
    // you must complete this function
    while(1){
        char line[10];
        int num;
        read(socket, line, 10);
        line[9] = '\0';
        num = strtol(line,NULL,10);
        if(num>=1 && num<=3){
            return num;
        }
        dprintf(socket,"Illegal Move! Please enter a num between 1-3 \r\n");
    }
    
}
int socket1,socket2;

void send_message_to_both(char *message){
    dprintf(socket1, message);
    dprintf(socket2, message);
}

int main() {
    // create socket
    int listen_soc = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_soc == -1) {
        perror("server: socket");
        exit(1);
    }

    //initialize server address    
    struct sockaddr_in server;
    server.sin_family = AF_INET;
    server.sin_port = htons(PORT);  
    memset(&server.sin_zero, 0, 8);
    server.sin_addr.s_addr = INADDR_ANY;

    // recycle port right away (step 3) 
    int on = 1;
    int status = setsockopt(listen_soc, SOL_SOCKET, SO_REUSEADDR, 
                            (const char *) &on, sizeof(on));
    if (status == -1) {
        perror("setsockopt -- REUSEADDR");
    }


    // bind socket to an address
    if (bind(listen_soc, (struct sockaddr *) &server, sizeof(struct sockaddr_in)) == -1) {
      perror("server: bind");
      close(listen_soc);
      exit(1);
    } 


    // Set up a queue in the kernel to hold pending connections.
    if (listen(listen_soc, 5) < 0) {
        // listen failed
        perror("listen");
        exit(1);
    }
   
    struct sockaddr_in client_addr;
    unsigned int client_len = sizeof(struct sockaddr_in);
    client_addr.sin_family = AF_INET;

    socket1 = accept(listen_soc, (struct sockaddr *)&client_addr, &client_len);
    if (socket1 == -1) {
        perror("accept");
        return -1;
    } 

    dprintf(socket1, "You are Player 1. We are waiting for Player 2\r\n");
    // accept a second player  
    socket2 = accept(listen_soc, (struct sockaddr *)&client_addr, &client_len);
    if (socket2 == -1) {
        perror("accept");
        return -1;
    } 
    char *msg;
    asprintf(&msg, "You can call a number of 1-3 pieces. One who takes the last piece wins\r\n");
    free(msg);
    send_message_to_both(msg);
    // demonstrating writing a message to player 1
    int item = LEGO_PIECES;
    asprintf(&msg, "There are %d lego pieces left.\r\n", item);
    send_message_to_both(msg);
    free(msg);
    int req;

    while(1){
        send_message_to_both("Player 1's turn\r\n");
        req = read_a_move(socket1);
        item-=req;
        asprintf(&msg, "There are %d lego pieces left.\r\n", item);
        send_message_to_both(msg);
        free(msg);
        if(item==0){
            send_message_to_both("Player 1 Wins!\r\n");
            exit(0);
        }
        send_message_to_both("Player 2's turn\r\n");
        req = read_a_move(socket2);
        item-=req;
        asprintf(&msg, "There are %d lego pieces left.\r\n", item);
        send_message_to_both(msg);
        free(msg);
        if(item==0){
            send_message_to_both("Player 2 Wins!\r\n");
            exit(0);
        }
    }


    return 0;
}


