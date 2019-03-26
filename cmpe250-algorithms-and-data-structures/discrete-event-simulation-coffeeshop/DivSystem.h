//
// Created by student on 10.11.2017.
//

#ifndef PROJECT2_DIVSYSTEM_H
#define PROJECT2_DIVSYSTEM_H

#include "Cashier.h"
#include "Barista.h"
#include "Event.h"
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <iterator>
#include "Customer.h"

using namespace std;

class DivSystem{
public:
    vector<Cashier>cashiers;
    int freeCash(bool &found);
    vector<Barista>baristas;
    int freeBar(int num,bool &found);
    priority_queue<Event,vector<Event>,early> events;
    vector<priority_queue<Customer,vector<Customer>,lessPrice>> baristaQue;
    queue<Customer> cashierQue;
    vector<Customer>customers;
    double totalRunTime;
    int lengthCash;
    vector<int> lengthBar;
    vector<double>utilCash;
    vector<double>utilBarista;
    vector<double>turnarounds;
    DivSystem(int numCash,int numCust,vector<Customer>customs);
    void runSym();
    void printSingular();
};


#endif //PROJECT2_DIVSYSTEM_H
