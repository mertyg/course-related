
## Discrete Event Simulation of a Coffee Shop

The project description can be found in Project3.pdf.

## Implementation Details

System and DivSystem classes are for the simulation first and second parts of the project. In both classes, RunSym() function handles the simulation process.

I have a priority queue that I keep the events, which takes the time field of the Event class as the key.
There are 3 types of events;

ARRIVAL - It is the event when the customer arrives.
CASHOUT - It is the event when the customer leaves the cashiers.
BAROUT - It is the event when the customer leaves the barista.

Consequences are handled accordingly.

I keep information related to Customer, Barista and Cashier in so named classes. 

In the main function, I handle the input, and print out the required info from the created System and DivSystem objects.


## How to compile

In a terminal, call commands:
```
>cmake CMakeLists.txt

>make

OR

>cmake CMakeLists.txt && make

```
Make sure the executable is produced.

Then you can test the project with the command:
```
>./project3 inputValuesFile outputValuesFile
```


