//
// Created by student on 02.11.2017.
//

#include "DivSystem.h"

int DivSystem::freeBar(int num,bool &found) {

        if(baristas[num].busy==false){
            found=true;
            return num;
        }

    found=false;
    return -1;

}

int DivSystem::freeCash(bool &found) {
    for(int i=0;i<cashiers.size();i++){
        if(cashiers[i].busy==false){
            found=true;
            return i;
        }

    }
    found=false;
    return -1;

}

DivSystem::DivSystem(int numCashiers, int numCustomers,vector<Customer>customs) {
    cashiers.resize(numCashiers);
    baristas.resize(numCashiers/3);
    baristaQue.resize(numCashiers/3);
    lengthBar.resize(numCashiers/3);
    for(int i=0;i<numCashiers/3;i++)
        lengthBar[i]=0;
    lengthCash=0;
    totalRunTime = 0;
    customers = customs;
}
void DivSystem::runSym() {

    Event e1, e2;
    for (int i = 0; i < customers.size(); i++) {
        Event e1(customers[i].ID, ARRIVAL, customers[i].arrival);
        events.push(e1);
    }
    bool isFound;
    while(!events.empty()){
        e1 = events.top();
        events.pop();
        totalRunTime = e1.time;
        if(e1.type==ARRIVAL){
            int arrivingID = e1.custId;
            cashierQue.push(customers[arrivingID]);
            if(cashierQue.size()>lengthCash)
                lengthCash=cashierQue.size();
            int cashNum;
            cashNum = freeCash(isFound);

            if(cashNum!=-1){
                int cashingID = cashierQue.front().ID;
                cashierQue.pop();
                customers[cashingID].cashIn = customers[arrivingID].arrival;
                customers[cashingID].cashDex=cashNum;
                //cout<<"Cashing time of customer "<<cashing.ID<<" is: "<<cashing.cashIn<<endl;
                //cout<<" CashDex is "<<cashing.cashDex<<endl;
                cashiers[cashNum].utilTime+=customers[cashingID].order;
                cashiers[cashNum].busy=true;
                e1.custId=customers[cashingID].ID;
                e1.time=customers[cashingID].arrival+customers[cashingID].order;
                e1.type=CASHOUT;
                events.push(e1);
            }
        }
        else if(e1.type==CASHOUT){
            int leavingID = e1.custId;
            int outCash = customers[e1.custId].cashDex;
            //cout<<"Leaving customer is "<<customers[leavingID].ID<< " from "<<customers[customers[leavingID].ID].cashDex<< " at "<<e1.time<<endl;
            double leaveTime = e1.time;
            cashiers[customers[leavingID].cashDex].busy=false;
            if(!cashierQue.empty()){
                int cashingID = cashierQue.front().ID;
                cashierQue.pop();
                customers[cashingID].cashDex = freeCash(isFound);
                customers[cashingID].cashIn = e1.time;
                cashiers[customers[cashingID].cashDex].busy=true;
                cashiers[customers[cashingID].cashDex].utilTime+=customers[cashingID].order;
                //cout<<"Cashing time of customer "<<cashing.ID<<" is: "<<cashing.cashIn<<endl;

                e1.custId=customers[cashingID].ID;
                e1.type=CASHOUT;
                e1.time=customers[cashingID].cashIn+customers[cashingID].order;
                events.push(e1);
            }

            baristaQue[outCash/3].push(customers[leavingID]);
            if(baristaQue[outCash/3].size()>lengthBar[outCash/3])
                lengthBar[outCash/3]=baristaQue[outCash/3].size();
            int barNum = freeBar(outCash/3,isFound);
            if(barNum!=-1){
                int baringID = baristaQue[outCash/3].top().ID;
                //cout<<"Customer "<<customers[baringID].ID<<" is going to bar "<<barNum<<" at "<<leaveTime<< endl;
                baristaQue[barNum].pop();
                customers[customers[baringID].ID].barDex=barNum;
                customers[baringID].barIn=customers[leavingID].cashIn+customers[leavingID].order;
                baristas[barNum].busy=true;
                baristas[barNum].utilTime+=customers[baringID].brew;
                customers[baringID].turnaround=customers[baringID].barIn+customers[baringID].brew-customers[baringID].arrival;
                e1.custId=customers[baringID].ID;
                e1.type=BAROUT;
                e1.time=leaveTime+customers[baringID].brew;
                events.push(e1);
            }

        }
        else if(e1.type==BAROUT){
            int outID = e1.custId;
            baristas[customers[outID].barDex].busy=false;
            int barNum = customers[outID].barDex;
            //cout<<"Barista out time of "<<customers[outID].ID<<" from "<<customers[outID].barDex<<" is "<<e1.time<<endl;
            if(!baristaQue[barNum].empty()){
                int baringID = baristaQue[barNum].top().ID;
                baristaQue[barNum].pop();
                customers[baringID].barIn=e1.time;
                customers[baringID].turnaround=customers[baringID].barIn+customers[baringID].brew-customers[baringID].arrival;
                customers[baringID].barDex=barNum;
                //cout<<"Customer "<<customers[baringID].ID<<" is going to bar "<<customers[baringID].barDex<<" at "<<customers[baringID].barIn<<endl;
                baristas[customers[baringID].barDex].busy=true;
                baristas[customers[baringID].barDex].utilTime+=customers[baringID].brew;
                e1.custId=customers[baringID].ID;
                e1.type=BAROUT;
                e1.time=customers[baringID].barIn+customers[baringID].brew;
                events.push(e1);
            }
        }

    }





}

void DivSystem::printSingular() {
    cout<<totalRunTime<<endl;
    cout<<lengthCash<<endl;
    for(int i=0;i<lengthBar.size();i++)
        cout<<lengthBar[i]<<endl;
    for(int i=0;i<cashiers.size();i++){
        float uTime = cashiers[i].utilTime;
        uTime = (int)(uTime*100/totalRunTime + 0.5);
        uTime/=100;
        cout<<uTime<<endl;
    }
    for(int i=0;i<baristas.size();i++){
        float uTime = baristas[i].utilTime;
        uTime = (int)(uTime*100/totalRunTime + 0.5);
        uTime/=100;
        cout<<uTime<<endl;
    }
    for(int i=0;i<customers.size();i++)
        cout<<customers[i].turnaround<<endl;
}

//
// Created by student on 10.11.2017.
//

