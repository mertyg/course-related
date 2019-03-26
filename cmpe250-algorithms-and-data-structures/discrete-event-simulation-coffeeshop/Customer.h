//
// Created by student on 02.11.2017.
//

#ifndef PROJECT2_CUSTOMER_H
#define PROJECT2_CUSTOMER_H


#include <queue>

class Customer{
public:
    Customer(int custID,double arr,double ord,double pr,double br);
    Customer();
    int ID;
    double arrival;
    double order;
    double price;
    double brew;
    double cashIn;
    double barIn;
    double turnaround;
    int cashDex;
    int barDex;
    Customer& operator=(const Customer& other);
};


#endif //PROJECT2_CUSTOMER_H
