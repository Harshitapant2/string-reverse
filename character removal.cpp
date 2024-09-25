//Construct a C++ program that removes a specific character from a given string and return the updated string.
#include<iostream>
#include<string.h>
using namespace std;
int main(){
	string a;
	int i,j,l;
	getline(cin,a);
	char ch;
	cin>>ch;
	l=a.length();
	for(i=0;i<l;i++){
		if(a[i]!=ch){
			cout<<a[i];
		}
	}
}
