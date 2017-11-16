#include <iostream>
#include <fstream>
#include <vector>
#include "Board.h"

int main(){

	int joinK, numCases, nLines;
  
 	std :: cin >> numCases;
  	for (int i = 0; i < numCases; i++){
    		std::cin >> nLines >> joinK;
    
    		std::string initBoard[100];
    		for (int j = 0; j < nLines; j++) {
      			std::cin >> initBoard[j];
    		}
    
		Board b(joinK, initBoard);
    		b.print();
    		b.rotate();
    		b.print();
    		b.gravity();
    		b.print();
    		std::cout << b.whoWinsNext() << std::endl;  
  	}
   
  	return 0;
}

