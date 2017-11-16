#include <iostream>
#include <string>
#include <stack>

int main(){
	std:: string word;
	std:: stack <std::string> reversedWords;

	std:: cout << "Type in words in sentences: (EOF to end input):" << std:: endl;

	while (std:: cin >> word && word != "EOF" ){
		reversedWords.push(word);
	}

	while(!reversedWords.empty()){
		std:: cout << reversedWords.top() << " ";
		reversedWords.pop();
	}
	

	return 0;
}
