##include<iostream>
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
cout<<name<<ab;
}
int main(){
bank d;
d.show();
}

