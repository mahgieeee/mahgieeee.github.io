#include <iostream>

signed int scalarProduct(signed int* vectorA, signed int* vectorB, int size){
	signed int* vectorC=new signed int[size];
	int sum=0;
	for (int j=0; j<size; j++){
		for (int i=0; i<size;i++){
			if (i==j)
				vectorC[i]=vectorA[i]*vectorB[j];
		}	
	}
	for (int k=0;k<size;k++){
		std::cout << "Vector C: " << vectorC[k] << std:: endl;
		sum+=vectorC[k];
	}

	delete vectorC;
	return sum;
}

signed int findMin(signed int vector[], int size){
	if (size==1)
		return vector[0];

	int tempValue=findMin(vector,size-1);

	if(vector[size-1]<tempValue)
		return vector[size-1];
	else return tempValue;
}  

signed int* selectionSortRecursive(signed int vector[], int size){	
	if(size==2){
		if (vector[1]<vector[0]){
			int temp=vector[0];
			vector[0]=vector[1];
			vector[1]=temp;
		}
		return vector;
	}
	return selectionSortRecursive(vector,size-1);	
}


void selectionSort(signed int vector[], int size) {    
      for (int i = 0; i < size - 1; i++) {
            int startIndex = i;
            for (int j = i + 1; j < size; j++)
                  if (vector[j] < vector[startIndex])
                        startIndex = j;
            if (startIndex != i) {
		  //swap elements
                  int temp = vector[i];
                  vector[i] = vector[startIndex];
                  vector[startIndex] = temp;
            }
      }
}

void reverse(signed int arr[], int size){
	for (int i=0;i<size/2;i++){
		int temp=arr[i];
		arr[i]=arr[size-i-1];
		arr[size-i-1]=temp;
	}
}
		
int main(){
	int elements;
	signed int* vectorA;
	signed int* vectorB;
	std:: cout << "Type in number of elements in vector: ";
	std:: cin >> elements;
	if (elements>0){
		vectorA=new signed int [elements];
		vectorB=new signed int [elements];
	}

	/*Read in Values*/
	std:: cout << "Type in " << elements << " elements in vector A: ";
	for (int i=0; i<elements;i++)
		std::cin >> vectorA[i];
	//std:: cout << findMin(vectorA,elements);
	selectionSort(vectorA,elements);
		
	std:: cout << "Type in " << elements << " elements in vector B: ";
	for (int j=0; j<elements;j++)	
		std::cin >> vectorB[j];

	//Minimum Scalar product is produced by multiplying the smaller number in vector A with a larger number in vector B and add the sums
	//Sort A and B, reverse B.
	selectionSort(vectorB,elements);
	reverse(vectorB,elements);
	std:: cout << "Minimum Scalar Product:" << scalarProduct(vectorA,vectorB,elements) << std:: endl;

	delete vectorA;
	delete vectorB;
	return 0;
}
