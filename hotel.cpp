/*Define a class Hotel in C++ with the following specifications
Private members
• Rno Data member to store room number
• Name Data member to store customer name
• Tariff Data member to store per day charges
• NOD Data member to store number of days of stay
• CALC() Function to calculate and return amount as NOD*Tariff ,and if the value 
of days* Tariff >10000,
then total amount is 1.05* days*Tariff.
Public members
• Checkin() Function to enter the content Rno, Name, Tariff and NOD
• Checkout() Function to display Rno, Name, Tariff,
NOD and Amount (amount to be displayed by calling function) CALC()*/
#include<iostream>
using namespace std;
class hotel{
private:
    int rno;
    string name;
    float tarrif;
    int nod;
    float calc(){
        float a=0;
        a=nod*tarrif;
        if(a>10000){
            a=1.05*nod*tarrif;
        }
        return a;
    }
public:
    void checkin(){
    printf("enter room");
    cin>>rno;
    printf("enter name");
    cin>>name;
    printf("enter tarrif");
    cin>>tarrif;
    printf("enter days");
    cin>>nod;
    }
    void checkout(){
    cout<<rno<<name<<tarrif<<nod;
    cout<<calc();
    }
};
int main(){
    hotel d1;
    d1.checkin();
    d1.checkout();
}


