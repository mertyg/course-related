//
// Created by student on 02.11.2017.
//
#include "Customer.h"
Customer::Customer(int custID,double arr,double ord,double pr,double br){
    ID = custID;
    arrival = arr;
    order = ord;
    price=pr;
    brew=br;
    cashDex=0;
    barDex=0;
    cashIn=0;
    barIn=0;
}
Customer::Customer(){
    ID=0;
    arrival=0;
    order=0;
    price=0;
    brew=0;
    cashDex=0;
    barDex=0;
    cashIn=0;
    barIn=0;
    turnaround=0;
}

Customer& Customer::operator=(const Customer& other){
    this->ID=other.ID;
    this->arrival=other.arrival;
    this->order=other.order;
    this->price=other.price;
    this->brew=other.brew;
    this->cashDex=other.cashDex;
    this->barDex=other.barDex;
    this->cashIn=other.cashIn;
    this->barIn=other.barIn;
    turnaround=other.turnaround;


}