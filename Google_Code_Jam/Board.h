/*See notes in Board.cpp file*/

#include <iostream> //std::string
#include <vector>
#ifndef BOARD_H
#define BOARD_H


class Board {
  
	private:
  		std::string *internalBoard;
  		int connectSize;
  		int size;
  		bool singleWin(char color);
  
	public:
  		Board(int connectSize, std::string *initBoard);
  		void rotate();
  		void gravity();
  		void print();
  		int addPiece(char color, int column);
  		std::string whoWinsNext();
};
#endif

