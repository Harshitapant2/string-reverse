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


