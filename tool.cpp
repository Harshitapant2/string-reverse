#include<iostream>
using namespace std;
class toolbooth{
    int cars;
    double money;
    public:
    toolbooth(){
        cars=0;
        money=0;
    }
    void payingcar(){
        cars=cars+1;
        money=money+0.5;
    }
    void nonpaycar(){
        cars=cars+1;
    }
    void display(){
        cout<<cars<<endl<<money;
    }

};
int main(){
    toolbooth t1;
    char c;
    while(1){
        cout<<"enter choice";
    cin>>c;
    switch(c){
        case 'p':
        t1.payingcar();
        break;
        case 'n':
        t1.nonpaycar();
        break;
        case 'e':
        t1.display();
        return 0;
    }

    }
}
