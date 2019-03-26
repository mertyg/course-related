PORT=59195
CFLAGS= -DPORT=\$(PORT) -g -Wall

hcq_server: hcq_server.o hcq.o
	gcc $(CFLAGS) -o hcq_server hcq_server.o hcq.o

hcq.o: hcq.c hcq.h
	gcc $(CFLAGS) -c hcq.c

hcq_server.o: hcq_server.c hcq.h
	gcc $(CFLAGS) -c hcq_server.c

clean: 
	rm hcq_server *.o
