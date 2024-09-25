#include<iostream>
using namespace std;
class savingsaccount{
float savingbalance;
public:
savingsaccount(float balance){
savingbalance=balance;
}
static float annualinterestrate;
void calculatemonthlyinterest(){
float mi;
mi=savingbalance*annualinterestrate/12;
savingbalance=savingbalance+mi;
}
static void modifyinterestrate(float newrate){
annualinterestrate=newrate;
}
float getbalance(){
return savingbalance;
}
};
float savingsaccount::annualinterestrate=0;
int main(){
savingsaccount server1(200);
savingsaccount server2(300);
savingsaccount::modifyinterestrate(0.04);
server1.calculatemonthlyinterest();
server2.calculatemonthlyinterest();
cout<<server1.getbalance()<<endl;
cout<<server2.getbalance()<<endl;
savingsaccount::modifyinterestrate(0.05);
server1.calculatemonthlyinterest();
server2.calculatemonthlyinterest();
cout<<server1.getbalance()<<endl;
cout<<server2.getbalance();
}
