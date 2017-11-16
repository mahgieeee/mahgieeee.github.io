/*Alien Language: 
L - # of lowercase letters
D - # of words in the language
N = # of testCases
Find K - # of words in the alien language that match the pattern*
*/
#include <iostream>
#include <fstream>
#include <utility>
#include <string>
#include <stdio.h>
#include <cstring>

std:: pair <std::string*, std::string*> readStrings(std::fstream &file){
	file.open("alienLanguage.txt");
	
	int numLowercaseletters, numWords, testCases; 
	file >> numLowercaseletters >> numWords >> testCases;	
	
	std:: string* testWords=new std:: string [numWords+1];
	for (int i=0; i<=numWords; i++)
		file >> testWords[i];

	std:: string *cases=new std:: string [testCases+1];
	for (int j=0; j<=testCases; j++)
		file >> cases[j];
	
	std::pair <std::string*,std::string*> stringPair= std::make_pair(testWords,cases);
	
	file.close();
	return stringPair;
	delete [] testWords;
	delete [] cases;
}

int countIndexes(std::string testCases){
	int openCounter=0;	
	for (int i=0; i<testCases.length();i++){
		if (testCases[i]=='(')
			openCounter++;
	}
	return openCounter;
}

char* toCharArray(std::string testCases){
	char *charArray=new char[testCases.length()+1];
	charArray[testCases.length()]=0; //NULL at end;
	memcpy(charArray,testCases.c_str(),testCases.length());	
	return charArray;
}
 
std:: pair<int*,int*> findIndex(std::string testCases){
	int numParenthesis=countIndexes(testCases);
	char* charArray = toCharArray(testCases);	
	
	int* indexValues= new int[numParenthesis];
	int* indexValues_closed= new int[numParenthesis];

	int j=0;
	while (j<numParenthesis){
		for (int i=0;i<testCases.length();i++){
			if (charArray[i]=='('){	
			   indexValues[j]=i+1; //want to start position after '('
			   j++;
			}
		}
	}
	int k=0;
	while (k<numParenthesis){
		for (int i=0;i<testCases.length();i++){
			if (charArray[i]==')'){	
			   indexValues_closed[k]=i;
			   k++;
			}
		}
	}

	return std::make_pair(indexValues,indexValues_closed);
	delete charArray;
	delete indexValues;
	delete indexValues_closed;
}

/*make possibilities per string index of testCases and then compare it with words given in file*/
std::string* getStrings_Paren(std::string testCases){//NOTE: testCases is NOT a pointer
	int numParenthesis=countIndexes(testCases);
	std::string* paren_Strings= new std::string[numParenthesis];
	
	for (int i=0; i<numParenthesis; i++){
		paren_Strings[i]=testCases.substr(*((findIndex(testCases).first)+i),*((findIndex(testCases).second)+i)-*((findIndex(testCases).first)+i));
		//test print---> 
		//std:: cout << paren_Strings[i] << std::endl;
	}
	return paren_Strings;
	delete [] paren_Strings;
	/*paren_Strings[0]=testCases.substr(4+1,9-5);//second coordinate is length of string
	paren_Strings[1]=testCases.substr(12+1,17-13);*/
}

//std::string* 
void getPossibilities(std::string testCases){//set this to testCases[i] after testing
	int numParenthesis=countIndexes(testCases);
	char* perString;
	std:: string newString[3];
	int j=0;

	while (j<3){ //where 3 is the maximum size of strlen(perString)
		for (int i=0; i<numParenthesis;i++){
			//parse each individual string array as char array
			perString=toCharArray( *(getStrings_Paren(testCases)+i) );	
		
			//if a () is less than 3...need to go back again to the first position...
			if (strlen(perString)<3){
				newString[j].push_back(perString[0]);
			}

			//perString[j] is a single character from ( ) in array
			newString[j].push_back(perString[j]);//appends a character to a string
								 
		}
		j++;
	}
	std:: cout << newString[0];
} 


int main(){
	std:: fstream mainfile;
	/*function returns pair <words to be checked, testCases>*/
	readStrings(mainfile); 
	
	/*(readStrings(mainfile).second* --create all possibilities of testCases*/
	//getStrings_Paren("(gu)(umo)(cdq)(bru)(ote)(xyk)(oah)(hwc)(vdm)(xr)");
	getPossibilities("(gu)(umo)(cdq)(bru)(ote)(xyk)(oah)(hwc)(vdm)(xr)");
	

	return 0;
}
