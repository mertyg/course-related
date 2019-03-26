#include "System.h"
#include "DivSystem.h"
#include <iomanip>


using namespace std;


    template <class Container>
    void split1(const string& str, Container& cont)
    {
        istringstream iss(str);
        copy(istream_iterator<string>(iss),
             istream_iterator<string>(),
             back_inserter(cont));
    }

    int main(int argc, char* argv[]) {
        // below reads the input file
        // in your next projects, you will implement that part as well
        if (argc != 3) {
            cout << "Run the code with the following command: ./project1 [input_file] [output_file]" << endl;
            return 1;
        }

        //cout << "input file: " << argv[1] << endl;
        //cout << "output file: " << argv[2] << endl;


        ifstream infile(argv[1]);
        string line;
        // process first line
        getline(infile, line);
        int numCash = stoi(line);
        //cout << "number of cashiers: " << numCash << endl;
        //process second line
        getline(infile, line);
        int numCust = stoi(line);
        //cout<< "number of customers: " << numCust <<endl;
        vector<Customer>customers;

        for (int i=0; i<numCust; i++) {
            getline(infile, line);
            vector<string> words;
            split1(line,words);
            Customer cust(i,stod(words[0]),stod(words[1]),stod(words[3]),stod(words[2]));
            customers.push_back(cust);

        }
        System Simulate(numCash,numCust,customers);
        Simulate.runSym();
        DivSystem DivSimulate(numCash,numCust,customers);
        DivSimulate.runSym();


        ofstream myfile;
        myfile.open (argv[2]);

        myfile<<fixed<<setprecision(2)<<Simulate.totalRunTime<<endl;
        myfile<<Simulate.lengthCash<<endl;
        myfile<<Simulate.lengthBar<<endl;
        for(int i=0;i<Simulate.cashiers.size();i++){
            double uTime = Simulate.cashiers[i].utilTime;
            uTime = (int)(uTime*100/Simulate.totalRunTime + 0.5);
            uTime/=100;
            myfile<<fixed<<setprecision(2)<<uTime<<endl;
        }
        for(int i=0;i<Simulate.baristas.size();i++){
            double uTime = Simulate.baristas[i].utilTime;
            uTime = (int)(uTime*100/Simulate.totalRunTime + 0.5);
            uTime/=100;
            myfile<<fixed<<setprecision(2)<<uTime<<endl;
        }
        for(int i=0;i<Simulate.customers.size();i++)
            myfile<<Simulate.customers[i].turnaround<<endl;

        myfile<<endl;
        myfile<<fixed<<setprecision(2)<<DivSimulate.totalRunTime<<endl;
        myfile<<DivSimulate.lengthCash<<endl;

        for(int i=0;i<numCash/3;i++)
        myfile<<DivSimulate.lengthBar[i]<<endl;


        for(int i=0;i<DivSimulate.cashiers.size();i++){
            double uTime = DivSimulate.cashiers[i].utilTime;
            uTime = (int)(uTime*100/DivSimulate.totalRunTime + 0.5);
            uTime/=100;
            myfile<<fixed<<setprecision(2)<<uTime<<endl;
        }
        for(int i=0;i<DivSimulate.baristas.size();i++){
            double uTime = DivSimulate.baristas[i].utilTime;
            uTime = (int)(uTime*100/DivSimulate.totalRunTime + 0.5);
            uTime/=100;
            myfile<<fixed<<setprecision(2)<<uTime<<endl;
        }
        for(int i=0;i<DivSimulate.customers.size();i++)
            myfile<<DivSimulate.customers[i].turnaround<<endl;


        myfile.close();


        return 0;
    }