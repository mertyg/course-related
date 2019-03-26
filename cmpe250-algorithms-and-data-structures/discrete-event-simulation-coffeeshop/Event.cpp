//
// Created by student on 02.11.2017.
//
#include "Event.h"
Event::Event(int ID,EVENT_TYPE eType,double t){
    custId = ID;
    type = eType;
    time = t;
}
Event::Event(){
    custId=0;
    type = ARRIVAL;
    time = 0;
}