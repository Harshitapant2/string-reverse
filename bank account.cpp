/*Implement a Program in C++ by defining a class to represent a bank account.
Include the following:
Data Members
● Name of the depositor
● Account number
● Type of account (Saving, Current etc.)
● Balance amount in the account
Member Functions
● To assign initial values
● To deposit an amount
● To withdraw an amount after checking the balance
● To display name and balance*/
#include<iostream>
using namespace std;
class bank{
string name;
int an;
float ab;
public:
void setdata(){
printf("enter name");
cin>>name;
printf("enter ac no.");
cin>>an;
printf("enter balance");
cin>>ab;
}
int da(int ab){
int x;
printf("enter value of x");
cin>>x;
ab=ab+x;
return ab;
}
int wd(int ab){
int v;
printf("enter v");
cin>>v;
if(v>ab){
cout<<"np";
}
else{
ab=ab-v;
}
return ab;
}
void show(){
cout<<name<<wd(ab);
}
};
int main(){
bank d;
d.setdata();
d.show();
}

