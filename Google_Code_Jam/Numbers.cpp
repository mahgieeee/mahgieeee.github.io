#include <iostream>
#include <math.h>
#include <string>
#include <sstream>
#include <stdlib.h>
#include <cstring>
#include <iomanip>

template<typename T>
std::string to_string(T val){
	std::stringstream ss("");
	ss<<val;
	return ss.str();
}

std::string getExponent(std:: string val){
	//char* s; (a string)
	//char s[]; (a character array)
	char newVal[2];

	for (int i=0;i<val.length();i++){
		if (val[i]=='+'){
		//	for (int j=val[i+1]; j<val.length(); j++)
			newVal[i]=val[i+1];
			newVal[i+1]=val[i+2]; 
		}
	//std::cout << newVal[i];
		return to_string(newVal[i]);	
	}
	return "wrong string obtained";
}

	
int doubletoInt(double answer){
	return static_cast<int>(answer);
}	

	
			
int main(){
	int n;
	double answer;
	
	std:: cout << "Type in n for calculation: ";
	std :: cin >> n;
	answer=pow((3+sqrt(5)),n);
	
	std:: cout << std:: setprecision(100) << "Answer: " << answer << std::endl;
	std:: cout << std::fixed; 

	std:: cout << "Answer(str): " << to_string(answer) << std::endl;
	std:: cout << "Exponent: " << getExponent(to_string(answer)) << std :: endl;
//	getExponent(to_string(answer));	
	std:: cout << "Answer(int): " << doubletoInt(answer) << std:: endl;
 	std:: cout << "Answer(3 digits before .): " << doubletoInt(answer)%1000 << std:: endl;
	return 0;
}

