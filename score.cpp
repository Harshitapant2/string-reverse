#include<iostream>
using namespace std;
class student{
int score[5];
public:
void input(){
for(int i=0;i<5;i++){
        cout<<"enter score";
cin>>score[i];
}
}
int ts(){
int t=0;
for(int i=0;i<5;i++){
t=t+score[i];
}
return t;
}
};
int main(){
    int c=0;
student s1[100];
for(int i=0;i<3;i++){
s1[i].input();
}
for(int i=0;i<3;i++){
    if(s1[i].ts()>s1[0].ts()){
        c++;
    }
}
cout<<c;

}
