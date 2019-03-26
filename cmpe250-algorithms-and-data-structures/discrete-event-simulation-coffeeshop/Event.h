//
// Created by student on 02.11.2017.
//

#ifndef PROJECT2_EVENT_H
#define PROJECT2_EVENT_H
#include "Customer.h"
enum EVENT_TYPE{
    ARRIVAL,CASHOUT,BAROUT
};


class Event{
public:
    int custId;
    EVENT_TYPE type;
    double time;
    Event(int ID,EVENT_TYPE eType,double t);
    Event();

};
struct early{
    bool operator()(const Event &e1,const Event &e2){
        return (e1.time>e2.time);
    }

};
#endif //PROJECT2_EVENT_H
