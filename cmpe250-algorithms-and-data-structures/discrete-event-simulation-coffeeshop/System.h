//
// Created by student on 02.11.2017.
//

#ifndef PROJECT2_SYSTEM_H
#define PROJECT2_SYSTEM_H

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

class System{
public:
    vector<Cashier>cashiers;
    int freeCash(bool &found);
    vector<Barista>baristas;
    int freeBar(bool &found);
    priority_queue<Event,vector<Event>,early> events;
    priority_queue<Customer,vector<Customer>,lessPrice> baristaQue;
    queue<Customer> cashierQue;
    vector<Customer>customers;
    double totalRunTime;
    int lengthCash;
    int lengthBar;
    vector<double>utilCash;
    vector<double>utilBarista;
    vector<double>turnarounds;
    System(int numCash,int numCust,vector<Customer>customs);
    void runSym();
    void printSingular();
};

#endif //PROJECT2_SYSTEM_H
