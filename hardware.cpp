#include<iostream>
using namespace std;
class invoice{
string partno;
string partdescription;
int quantity;
double price;
public:
invoice(){}
invoice(string partno,string partdescription,int quantity,double price){
    this->partno=partno;
    this->partdescription=partdescription;
    this->quantity=quantity;
    this->price=price;
}
void setpartno(string partno){
    this->partno=partno;

}
void setpartdescription(string partdescription){
this->partdescription=partdescription;
}
void setquantity(int quantity){
    this->quantity=quantity;

}
void setprice(double price){
    this->price=price;

}
string getpartno(){
return partno;
}
string getpartdescription(){
    return partdescription;
}
int getquantity(){
    return quantity;
}
double getprice(){
    return price;
}
double getinvoiceamount(){
    double t;
    if(price>0){
    t=quantity*price;
    return t;
    }
    else{
        return 0;
    }
}

};
int main(){
    invoice test[100];
    int n,i,q;
    string no,d;
    double a;
    cout<<"enter n";
    cin>>n;
    for(i=0;i<n;i++){
        cout<<"enter no.";
        cin>>no;
test[i].setpartno(no);
cout<<"enter ds";
        cin>>d;
test[i].setpartdescription(d);
cout<<"enter q";
        cin>>q;
test[i].setquantity(q);
cout<<"enter amount";
        cin>>a;
test[i].setprice(a);
cout<<test[i].getpartno();
cout<<test[i].getpartdescription();
cout<<test[i].getquantity();
cout<<test[i].getprice();
cout<<test[i].getinvoiceamount();
    }

}