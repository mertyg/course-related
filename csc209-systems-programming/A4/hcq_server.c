#define _POSIX_C_SOURCE 200809L
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include "hcq.h"
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/select.h>
#define _GNU_SOURCE

#define INPUT_BUFFER_SIZE 256
#define INPUT_ARG_MAX_NUM 3  
#define DELIM " \n"
#ifndef PORT
  #define PORT 59194
#endif
#define MAX_BACKLOG 5
#define BUFSIZE 30
#define EXIT_REMOVED_USER -3


//error handling malloc.
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
Ta *ta_list = NULL;
Student *stu_list = NULL;
Course *courses;  
int num_courses = 3;
int MAX_CONNECTIONS = 100;
User *users;
fd_set all_fds;

//Function for dynamically growing the users array.
void grow_users(User **users_ptr){
    //printf("came to grow\n");
    User *new_list = realloc(users,2*MAX_CONNECTIONS*sizeof(User));
    for(int i=MAX_CONNECTIONS;i<2*MAX_CONNECTIONS;i++){
        new_list[i].fd=-1;
        new_list[i].username=NULL;
        new_list[i].state=0;
        new_list[i].role='N';
        new_list[i].room=0;
        new_list[i].inbuf=0;
        new_list[i].after=NULL;
        new_list[i].buf=NULL;
    }
    MAX_CONNECTIONS*=2;
    *users_ptr = new_list;
    //printf("already growed\n");
}

//initialization for server address. 
//taken from course starter codes.
struct sockaddr_in *init_server_addr(int port) {
    struct sockaddr_in *addr = Malloc(sizeof(struct sockaddr_in));
    // Allow sockets across machines.
    addr->sin_family = PF_INET;
    // The port the process will listen on.
    addr->sin_port = htons(port);
    // Clear this field; sin_zero is used for padding for the struct.
    memset(&(addr->sin_zero), 0, 8);
    // Listen on all network interfaces.
    addr->sin_addr.s_addr = INADDR_ANY;
    return addr;
}

//helper function for setting server socket.
//taken from course starter codes.
int set_up_server_socket(struct sockaddr_in *self, int num_queue) {
    int soc = socket(PF_INET, SOCK_STREAM, 0);
    if (soc < 0) {
        perror("socket");
        exit(1);
    }
    // Make sure we can reuse the port immediately after the
    // server terminates. Avoids the "address in use" error
    int on = 1;
    int status = setsockopt(soc, SOL_SOCKET, SO_REUSEADDR,
        (const char *) &on, sizeof(on));
    if (status < 0) {
        perror("setsockopt");
        exit(1);
    }
    // Associate the process with the address and a port
    if (bind(soc, (struct sockaddr *)self, sizeof(*self)) < 0) {
        // bind failed; could be because port is in use.
        perror("bind");
        exit(1);
    }
    // Set up a queue in the kernel to hold pending connections.
    if (listen(soc, num_queue) < 0) {
        // listen failed
        perror("listen");
        exit(1);
    }
    return soc;
}

//helper function for printing an error message 
//to a client.
void error(char *msg, int client_fd) {
    dprintf(client_fd, "Error: %s\r\n", msg);
}

//helper function for finding the network inline in a 
//given buffer.
int find_network_newline(const char *buf, int n) {
    if(buf==NULL)
        return -1;
    for(int i=0;i<n;i++){
        //we will stop either when we see /r/n or /n.
        if (buf[i] == '\n'){
            return i + 1;
        }
    }
    return -1;
}


//helper function for disconnecting a specific client.
//idx is the position in the users array.
void handle_removal(User *users,int idx){
    if(users[idx].role=='T'){
        remove_ta(&ta_list,users[idx].username);
    }
    else{
        give_up_waiting(&stu_list,users[idx].username);
    }
    if(users[idx].username!=NULL){
        //printf("Before free username: %s\n",users[idx].username);
        free(users[idx].username);
    }
    if(users[idx].buf!=NULL){
        //printf("Before free buf: %s\n",users[idx].buf);
        free(users[idx].buf);
    }
    users[idx].fd=-1;
    users[idx].username=NULL;
    users[idx].state=0;
    users[idx].role='N';
    users[idx].room=0;
    users[idx].inbuf=0;
    users[idx].after=NULL;
    users[idx].buf=NULL;
}

//helper function for processing arguments.
int process_args(int cmd_argc, char **cmd_argv, int idx,User *users) {

    char *print_str=NULL;
    int client_fd = users[idx].fd;
    if (cmd_argc <= 0) {
        return 0;
    }   
    //If stats and TA, we can print full queue.
    else if (strcmp(cmd_argv[0], "stats") == 0 && cmd_argc == 1 && users[idx].role=='T') {
        print_str = print_full_queue(stu_list);
        dprintf(client_fd,"%s\r\n",print_str);
        if(print_str!=NULL)
            free(print_str);
    }
    //if stats is called by a student, we should print currently serving. 
    else if (strcmp(cmd_argv[0], "stats") == 0 && cmd_argc == 1  && users[idx].role=='S') {
        print_str = print_currently_serving(ta_list);
        dprintf(client_fd,"%s\r\n",print_str);
        if(print_str!=NULL)
            free(print_str);
    } 
    //If next is called by TA, she should call the next student.
    else if (strcmp(cmd_argv[0], "next") == 0 && cmd_argc == 1 && users[idx].role=='T') {
        int result= next_overall(users[idx].username, &ta_list, &stu_list,users);
        if(result==-2){
            return 0;
        }
        if (result == -1) {
            //should never come here.
           dprintf(client_fd,"Invalid TA username.\r\n");
        }
        return result+1;
    } else {
        dprintf(client_fd,"Incorrect syntax\r\n");
    }
    return 0;
}

//Handler function for input coming from a user.
int handler(char *input,int idx, User *users){
    int cmd_argc;
    char *cmd_argv[INPUT_ARG_MAX_NUM];
    char *next_token = strtok(input, DELIM);
    int client_fd = users[idx].fd;

    //If initial state, we should get the role.
    if(users[idx].state==0){
        users[idx].username=Malloc(30);
        strncpy(users[idx].username,input,29);
        users[idx].username[29]='\0';
        users[idx].state=1;
        dprintf(client_fd,"Are you a TA or a Student (enter T or S)?\r\n");
    }
    //If we have the role and she is a TA, we can take her to idle state.(3)
    else if(users[idx].state==1){
        if(input[0]=='T'){
            users[idx].role='T';
            users[idx].state=3;
            add_ta(&ta_list, users[idx].username);
            dprintf(client_fd,"Valid commands for TA:\r\n");
            dprintf(client_fd,"\t stats\r\n");
            dprintf(client_fd,"\t next\r\n");
            dprintf(client_fd,"\t (or use Ctrl-C to leave)\r\n");
        }
        //If student and we have the role, we should ask for the course.
        else if(input[0]=='S'){
            users[idx].role='S';
            users[idx].state=2;
            dprintf(client_fd,"Valid courses: CSC108, CSC148, CSC209\r\n");
            dprintf(client_fd,"Which course are you asking about?\r\n");
        }
        else{
            dprintf(client_fd,"Invalid Role: (enter T or S)\r\n");
        }
    }
    else if(users[idx].state==2){
        int result = add_student(&stu_list, users[idx].username, input, courses,
                        num_courses); 
        //If we cannot successfully add the student and the result is 1, this means she is already in the queue.
        if (result == 1) {
            dprintf(client_fd,"You are already in the queue and cannot be added again for any course. Good-bye.\r\n");
            close(users[idx].fd);
            FD_CLR(users[idx].fd, &all_fds);
            users[idx].fd=-1;
            handle_removal(users,idx);
            return EXIT_REMOVED_USER;
        } 
        //If we cannot add because the course is invalid, we disconnect the user.
        else if (result == 2) {
            dprintf(client_fd,"Please enter a valid course from: CSC108, CSC148.\r\n");
            //close(users[idx].fd);
            //FD_CLR(users[idx].fd, &all_fds);
            //users[idx].fd=-1;
            //handle_removal(users,idx);
            //return EXIT_REMOVED_USER;
        }
        else{
            dprintf(client_fd,"You have been entered into the queue. While you wait, you can use the command stats to see which TAs are currently serving students.\r\n");
            users[idx].state=3;
        }
    }
    //For commands coming from idle state, we should check validity using 
    //process_args, and handle accordingly.
    else if(users[idx].state==3){
        cmd_argc = 0;
        while (next_token != NULL) {
            if (cmd_argc >= INPUT_ARG_MAX_NUM) {
                error("Incorrect syntax",client_fd);
                cmd_argc = 0;
                break;
            }
            cmd_argv[cmd_argc] = next_token;
            cmd_argc++;
            next_token = strtok(NULL, DELIM);
        }
        int result = process_args(cmd_argc, cmd_argv,idx,users);
        if (cmd_argc > 0 &&  result == -1) {
            return result; // can only reach if quit command was entered
        }
        if(cmd_argc >0 && result>0){
            return result;
        }
    }
        return 0;
}


//Helper function for accepting connections and initializing a user.
int accept_connection(int fd,User **users_ptr) {
    int idx = 0;
    User *users = *users_ptr;
    while (idx < MAX_CONNECTIONS && users[idx].fd != -1) {
        idx++;
    }

    if (idx == MAX_CONNECTIONS) {
        grow_users(users_ptr);
    }
    //printf("came after grow\n");
    users = *users_ptr;
    int client_fd = accept(fd, NULL, NULL);
    if (client_fd < 0) {
        perror("server: accept");
        close(fd);
        exit(1);
    }

    users[idx].fd = client_fd;
    users[idx].username = NULL;
    users[idx].state=0;
    users[idx].role = 'N';
    users[idx].buf = Malloc(BUFSIZE);
    users[idx].after = NULL;
    users[idx].room=0;
    users[idx].inbuf=0;
    return idx;
}


int main(int argc, char* argv[]) {
    users = Malloc(MAX_CONNECTIONS*sizeof(User));
    if (argc < 1 || argc > 2) {
        fprintf(stderr, "Usage: ./helpcentre [commands_filename]\n");
        exit(1);
    }

    if ((courses = Malloc(sizeof(Course) * 3)) == NULL) {
        perror("Malloc for course list\n");
        exit(1);
    }
    //Creating valid courses and initializing connection list.
    strcpy(courses[0].code, "CSC108");
    strcpy(courses[1].code, "CSC148");
    strcpy(courses[2].code, "CSC209");
    for(int i=0;i<MAX_CONNECTIONS;i++){
        users[i].fd=-1;
        users[i].username=NULL;
        users[i].state=0;
        users[i].role='N';
        users[i].room=0;
        users[i].inbuf=0;
        users[i].after=NULL;
        users[i].buf=NULL;
    }

    //Setting up the sockets and the connections.
    struct sockaddr_in *server = init_server_addr(PORT);
    int sock_fd = set_up_server_socket(server,MAX_BACKLOG);
    int max_fd = sock_fd;
    FD_ZERO(&all_fds);
    FD_SET(sock_fd, &all_fds);


    while(1){
        fd_set listen_fds = all_fds;
        int nready = select(max_fd + 1, &listen_fds, NULL, NULL, NULL);
        if (nready == -1) {
            perror("server: select");
            exit(1);
        }
        if (FD_ISSET(sock_fd, &listen_fds)) {
        int idx = accept_connection(sock_fd,&users);
        if(idx<0){
            continue;
        }
        strncpy(users[idx].buf,"\0",1);
        users[idx].inbuf = 0;           // How many bytes currently in buffer?
        users[idx].room = BUFSIZE;  // How many bytes remaining in buffer?
        users[idx].after = users[idx].buf;
        FD_SET(users[idx].fd, &all_fds);
        dprintf(users[idx].fd,"Welcome to the Help Centre, what is your name?\r\n");
        if(users[idx].fd > max_fd){
            max_fd = users[idx].fd;
        }
    }
        //Checking all of the users
        for(int idx=0;idx<MAX_CONNECTIONS;idx++){
            if (users[idx].fd > -1 && FD_ISSET(users[idx].fd, &listen_fds)) {
                int nbytes = read(users[idx].fd, users[idx].after, users[idx].room);
                //if not read, this means the read end of the pipe is closed.
                if(nbytes==0){
                    FD_CLR(users[idx].fd, &all_fds);
                    close(users[idx].fd);
                    handle_removal(users,idx);
                    continue;
                }
                users[idx].inbuf+=nbytes;
                int where;
                //Handling the input. If we can find \r\n or \n, then pass the input to the handler.
                while ((where = find_network_newline(users[idx].buf, users[idx].inbuf)) > 0) {
                    if(where >= 2 && users[idx].buf[where-2]=='\r')
                        users[idx].buf[where-2]='\0';
                    else
                        users[idx].buf[where-1]='\0';
                    char input[BUFSIZE];
                    strncpy(input,users[idx].buf,strlen(users[idx].buf)+1);
                    int res = handler(input,idx,users);
                    if(res>0){
                        res-=1;
                        dprintf(users[res].fd,"Your turn to see the TA.\r\n");
                        dprintf(users[res].fd,"We are disconnecting you from the server now. Press Ctrl-C to close nc\r\n");
                        close(users[res].fd);
                        FD_CLR(users[res].fd, &all_fds);
                        users[res].fd=-1;
                        handle_removal(users,res);
                    }
                    //EXIT_REMOVED_USER=-3 is the code for removed user due to a reason. 
                    //Hence we don't need to process any other thing.
                    if(res==EXIT_REMOVED_USER)
                        break;
                if(users[idx].buf!=NULL){
                users[idx].inbuf-=where;
                //printf("%s buf\n",users[idx].buf);
                memmove(users[idx].buf,users[idx].buf+where,users[idx].inbuf);
                //printf("%s after buf+where\n",users[idx].buf);
            }
        }
            //If user is removed, we don't want to get a SEG Fault.
            if(users[idx].buf!=NULL){
            users[idx].after = users[idx].buf+users[idx].inbuf;
            users[idx].room = BUFSIZE-users[idx].inbuf;
        }
        }
    }
}
//should never come here.
return 1;
}
