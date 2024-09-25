#include<iostream>
#include<stdbool.h>
using namespace std;
class a{
    public:
    float calculatearea(int x){
        return x*x;
    }
    float calculatearea(int l,int b){
        return l*b;
    }
    float calculatearea(int k,int h,bool istriangle){
        if(istriangle){
return 0.5*k*h;
        }

    }
};
int main(){
    a a1;
    int x,l,b,h,k,c;
    cout<<"enter 1 to calculate area of square\n";
    cout<<"enter 2 to calculate area of rectangle\n";
    cout<<"enter 3 to calculate area of triangle\n";
    cout<<"enter 4 to exit\n";
    while(1){
        cout<<"enter choice";
        cin>>c;
        switch(c){
            case 1:
            cout<<"enter x";
            cin>>x;
            cout<<a1.calculatearea(x);
            break;
            case 2:
            cout<<"enter l and b";
            cin>>l>>b;
            cout<<a1.calculatearea(l,b);
            break;
            case 3:
            cout<<"enter k and h";
            cin>>k>>h;
            cout<<a1.calculatearea(k,h,1);
            break;
            case 4:
            return 0;

        }
    }

}