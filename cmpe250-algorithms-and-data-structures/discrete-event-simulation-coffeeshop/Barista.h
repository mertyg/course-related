//
// Created by student on 02.11.2017.
//
#include "Customer.h"

#ifndef PROJECT2_BARISTA_H
#define PROJECT2_BARISTA_H
struct lessPrice{
    bool operator()(const Customer &c1,const Customer &c2){
        return (c1.price<c2.price);
    }

};

class Barista{
public:
    Barista();
    bool busy;
    double utilTime;

};

#endif //PROJECT2_BARISTA_H
