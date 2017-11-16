/*Program takes input from a file from a string[] of size N representing a NXN BOARD
ROTATE and GRAVITY is called at the beginning of the program after object is created.
Two players, Red and Blue, make a move
Based on K, winner is decided and move on to the next case*/

#include "Board.h"
#include <iostream>
#include <vector>
#include <string>

using namespace std;

/*initializes board by getting string ptr from main and int k to determine winner*/
Board::Board(int connectSize, std::string *initBoard){
	this->connectSize = connectSize;
  	this->internalBoard = initBoard;
  	this->size = this->internalBoard[0].size();
}

/*replaces the current string array with a gravitated string array*/
void Board::gravity(){//changes a string column by column if it sees '.' underneath
  	for (int col = 0; col < size; col++){
   	string newCol(size, '.');//new column with '.'
      	int fallTohere = size -1; //where the next piece will fall to

      		for (int row = size-1; row > -1; row--){//per first col, start at top and go down
      			char test = this->internalBoard[row][col]; //keeps track of curr location of board 
      			if (test == 'R' || test == 'B'){
         			newCol[fallTohere] = test; //sets '.' to letter
            			fallTohere--;
         		}
		}

        	//writes the string back to the board
        	for (int row = size-1; row > -1; row--)
            		this->internalBoard[row][col] = newCol[row];
    	}
}

/*when board is rotated, the coordinates change, find that change and set it to rotated*/
void Board::rotate(){
	string newCol(size, '.');
    	vector<string> rotated(size, newCol);
    	for (int col = 0; col < size; col++){
        	for (int row = 0; row < size; row++) 
            		rotated[col][size-row-1] = this->internalBoard[row][col]; //rotates at 90 clockwise  
    	}

    	//writes the strings back to the board
    	for (int col = 0; col < size; col++){
        	for (int row = 0; row < size; row++)
            		this->internalBoard[row][col] = rotated[row][col];//set location of board to rotated column 

   	}
}

/*prints the board row by row*/  
void Board::print(){ 
	for (int row = 0; row < size; row++)
      		cout << this->internalBoard[row] << endl;
}
  
/*player makes a move, per column like connect for*/
int Board::addPiece(char color, int column){
  
  	if(this->internalBoard[0][column] != '.') // already filled
    		return -1;
  
  	this->internalBoard[0][column] = color; //since column changes, you make it to the top row and it drops down by gravity
  	this->gravity();
	
	//row needs to be returned after player makes move to keep the board updated
  	int row = 0;
  	while (internalBoard[row][column] == '.')//for the piece to be legal no '.' in between
    		row++;//continue going down per column
  
	return row;
}

/*Board conditions, horizontal, vertical or diagonal, that determine win per player*/
bool Board::singleWin(char color){
  
	//horizontal connect K  
  	for(int row = 0; row < size; ++row){
    		for(int count = 0, ix = 0; ix < size; ++ix){ // go through all fields that might be part of the winning row
      			if (internalBoard[row][ix] == color){ // if it's the right color
        				if (++count == connectSize) // increase the count and check whether there are enough tokens
          					return true;
      			}
      			else count = 0; // reset the count because colors don't match to connectSize
    		}	
  	}
	   
    	//vertical connect K-same as horizontal except for column major
  	for(int col = 0; col < size; ++col){
    		for(int count = 0, iy = 0; iy < size; ++iy){ // go through all fields that might be part of the winning col
      			if (internalBoard[iy][col] == color){ 
    				if (++count == connectSize)
      					return true;
      			}
      			else count = 0; 
   		 }		
  	}

  	//diagonal connect K via left
  	for(int col = 0, row =size-1; col != size && row != 0; ){
    		for(int count = 0, ix = col, iy = row; iy < size && ix < size; ++iy, ++ix){ // go through all fields that might be part of the winning col
      			if (internalBoard[iy][ix] == color){ // if it's the active player's color...
    				if (++count == connectSize) // increase the count and check whether there are enough tokens
      					return true;
      			}
      			else count = 0; //reset count 
    		}
    
    		if (row == 0) col++; //continue moving right per col---this replaces the third ; in the above for loop to have multiple conditions
    		else row--; //unless go down
  	}

  	//diagonal connect K via right
  	for(int col = 0, row = 0; col != size-1 && row != size; ){
    		for(int count = 0, ix = col, iy = row; iy < size && ix < size; ++iy, --ix){ // go through all fields that might be part of the winning col
      			if (internalBoard[iy][ix] == color){ // if it's the active player's color...
    				if (++count == connectSize) // increase the count and check whether there are enough tokens
      					return true;
      			}
      			else count = 0; // reset the count
    		}
    		if (col == size-1) row++; //opposite of diagonal left function
    		else col++;
  	}

 	 return false;
}

/*Function that determine who wins next per case*/
std::string Board::whoWinsNext(){
  	//set players winning flags to false and there corresponding colors
  	bool bWin = false, rWin = false;
  	rWin = this->singleWin('R');
  	bWin = this->singleWin('B');

  	//boolean conditions for return string for winner
  	if (bWin && rWin)
    		return "Both";
  	else if (bWin)
    		return "Blue";
  	else if (rWin)
    		return "Red";
  	else
   		 return "Neither";
  
	//go through adding pieces for either player and set winner to the object
  	for(int col = 0; col < size; col++){
    		int row = this->addPiece('R', col);
    			if (row == -1) 
				continue;

    		rWin = this->singleWin('R');
    		internalBoard[row][col] = '.';
  	}

  	for (int col = 0; col < size; col++){
    		int row = this->addPiece('B', col);
    			if (row == -1)
      				continue;

    		bWin = this->singleWin('B');
    		internalBoard[row][col] = '.';
  	}
  
	//again, to loop through the cases
  	if (bWin && rWin)
    		return "Both";
  	else if (bWin)
    		return "Blue";
  	else if (rWin)
    		return "Red";
  	else
    		return "Neither";
}


