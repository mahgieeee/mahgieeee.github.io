#include <iostream>
#include <string>

const int MAXSIZE=50;
int dynLetters(int n){//where n is the length of the string - not string &alphabet as para
	//store the count in an array for dynLetters to retrieve it later
	int count;
	int arr[MAXSIZE];

	//check for previously results and return 
	if (alphabet[n]=='a' && alphabet[n+1]='a') return count;
	
	//else execute the recursion base case
	if (n==1) count=2;
	else if (n==0) count=1;

	else count=dynLetters(n-2) + dynLetters(alphabet,n-2);
	
	//store the result and return its value
	arr[0]=count;
	return count;
}

/*Given an 9 × 9 board with some squares already filled with hint values, the objective of the
Sudoku problem is to fill all the empty squares with values in 1..9, such that each row, each
column, and each of the 9 blocks are filled with distinct values.*/

bool distinctLocation(const int matrix[9], int row, int column){ //set vector to value...
	int distinctCol, distinctRow;
	for (distinctRow=0; distinctRow<row; distinctRow++){
		for (distinctCol=0; distinctCol<column; distinctCol++){
			if (matrix[distinctRow][distinctCol] == matrix[row][column]) return false; 
			//does this check for top and bottom?
		}
	}
	for (distinctCol=0; distinctCol<column; distinctCol++){
		for (distinctRow=0; distinctRow<row; distinctRow++){
			if (matrix[distinctRow][distinctCol] == matrix[row][column]) return false;
	}
	return true;
}

bool placeValue(const int matrix[][9], int row, int col){
	int row=0, col=0;
	bool foundLocation;
	if (col==9 && row==9) //stopping condition
		foundLocation=true;
	foundLocation=false;
	
	if distinctLocation(matrix,row,col) == true){
		while(row<9 && col<9 && !foundLocation){
			queenList[col]=row;
			//try to place queens col 1 through 7
			foundLocation=placeValue(matrix[],col+1);
			
			if (!foundLocation) {
				matrix[col++]=row;
				row++; //use next row since current row doesn't lead to solution
			}
			else row++; //current row fails go to the next row
		}
	}
	return safeLocation;
}

bool sudoku(vector<int> &matrixList, int row){
	matrixList[0]=row; 
	if (placeValue(matrixList,1)) return true;
	return false;
}

int main(){
	std:: string alphabet= "abaaabaabbbbbba";
	std:: cout << dynLetters(alphabet,5);
	int row;
	vector<int> sudoku(9);
	board chessBoard;
}
