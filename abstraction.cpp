#include<iostream>
using namespace std;
class employee{
    private:
    float salary ;
    string name;
    public:
    void setsalary(float salary){
        this->salary=salary;
    }
    void setname(string name){
        this->name=name;
    }
    float getsalary(){
        return salary;
    }
    string getname(){
        return name;
    }
    void show(){
        
        cout<<getname()<<endl;
        cout<<getsalary();
    }
};
int main(){
    employee e1[10];
    int i,n;
    float salary;
    string name;
    cout<<"enter n";
    cin>>n;
    
    for(i=0;i<n;i++){
        cout<<"enter name and salary"<<endl;
    cin>>name;
    cin>>salary;
        e1[i].setname(name);
        e1[i].setsalary(salary);
        e1[i].show();
    }
}
