#include<iostream>
using namespace std;
class time{
int hours;
int minutes;
int seconds;
public:
time(){
hours=0;
minutes=0;
seconds=0;
}
time(int hours,int minutes,int seconds){
this->hours=hours;
this->minutes=minutes;
this->seconds=seconds;
}
void display(){
if(hours<10){
    cout<<'0';
}
cout<<hours<<':';

if(minutes<10){
    cout<<'0';
}
cout<<minutes<<':';

if(seconds<10){
    cout<<'0';
}
cout<<seconds<<':';
}


void add(time t1,time t2){
seconds=t1.seconds+t2.seconds;
minutes=t1.minutes+t2.minutes;
hours=t1.hours+t2.hours;
if(seconds>=60){
seconds=seconds-60;
minutes++;
}

if(minutes>=60){
minutes=minutes-60;
hours++;
}

if(hours>=24){
hours=hours-24;
}
}
};
int main(){
int h,m,s;

cout<<"enter hours minutes and seconds for t1;";
cin>>h>>m>>s;
time t1(h,m,s);
cout<<"enter hours minutes and seconds for t2;";
cin>>h>>m>>s;
time t2(h,m,s);

time t3;
t3.add(t1,t2);
t3.display();
}
