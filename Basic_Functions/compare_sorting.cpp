#include <iostream>
#include <vector>
#include <time>


template <typename T>
class Compare {
public:
	bool operator() (T temp, T target) {
		if (temp < target)
			return true;
		return false;
	}
};

template <typename T, typename Compare>
void insertionSort(std::vector<T> &v, Compare comp) {
	int i, j, n = v.size();
	T temp;

	for (i = 1; i<n; i++) {
		j = i;
		temp = v[i];
		while (j>0 && comp(temp, v[j - 1])) {
			v[j] = v[j - 1];
			j--;//shifts the elements to leave room for insert
		}
		v[j] = temp; //when v[j] is greater than v[i] swap
	}
}

/*MergeSort
 merges two sorted subarrays*/
template <typename T>
void merge(std::vector <T> &vec, int front, int mid, int back) {
	std::vector <T> tmpVec;
	int leftIndex = front, rightIndex = mid;
	while (leftIndex<mid && rightIndex<back) {
		if (vec[leftIndex] < vec[rightIndex]) {
			tmpVec.push_back(vec[leftIndex]);
			leftIndex++;
		}
		else {
			tmpVec.push_back(vec[rightIndex]);
			rightIndex++;
		}
	}
	//exhaused subarray either left or right
	while (rightIndex<back || leftIndex<mid) {
		if (leftIndex == mid) { //add right elements to tmpvec
			tmpVec.push_back(vec[rightIndex]);
			rightIndex++;
		}
		else if (rightIndex == back) {
			tmpVec.push_back(vec[leftIndex]);
			leftIndex++;
		}
	}

	//copy tmpArray back to original array
	int vecIndex = 0;
	for (int i = 0; i<tmpVec.size(); i++) {
		vec[i] = tmpVec[vecIndex];
		vecIndex++;
	}
}

/*recursively divides the array*/
template <typename T>
void mergeSort(std::vector <T> &vec, int front, int back) {
	int mid = front+ (front - back)/ 2; //to prevent overflow 
	mergeSort(vec, front, mid - 1);
	mergeSort(vec, mid, back);
	merge(vec, front, mid, back);
}


template <typename T>
void startMergeSort(std::vector <T> vec) {
	mergeSort(vec, 0, vec.size() - 1);
}

template <typename T>
void swap(std::vector <T> &vec, int front, int back) {
	T temp;
	temp = vec[front];
	vec[front] = vec[back];
	vec[back] = temp;
}

template <typename T>
int findpivotIndex(std::vector <T> &vec, int front, int back) {
	T pivot;
	int mid = front + (back - front)/ 2;
	pivot = vec[mid];
	vec[mid] = vec[front];
	vec[front] = pivot;
	int forward = front + 1, backward = back - 1; //move to vec[1] because vec[0] contains pivot
	while (forward <= backward) {
		while (vec[forward] >= pivot) backward--;
		while (vec[forward]<pivot && forward<backward) forward++;
		if (forward < backward) swap(vec, forward++, backward--);
	}
	swap(vec, mid, backward);
	return backward;
}

/*QuickSort
 finds changing pivot using recursion*/
template <typename T>
void quickSort(std::vector <T> &vec, int front, int back) {
	int pivotIndex =findpivotIndex(vec, front, back);
	quickSort(vec, front, pivotIndex);
	quickSort(vec, pivotIndex + 1, back);
}

template <typename T>
void startQuickSort(std::vector <T> &vec) {
	quickSort(vec, 0, vec.size());
}

int main(){

	/*object to calculate CPU time*/
	clock_t time;
	time=clock();
	
	std::vector<int> testVec={8, 64, 52, 3, 4, 2 };
	Compare <int> integers;
	insertionSort(testVec,integers);

	std::cout << "After Insertion sort:" << std::endl;
	for (unsigned int i = 0; i < testVec.size(); i++)
		std:: cout << testVec[i] << " ";
	std::cout << std::endl;
	std::cout << "Insertion sort took: " << time << "seconds" << std::endl;

	std::vector<int> testVec1 = { 0, 64, 52, 3, 4, 2 };
	startMergeSort(testVec1);
	std::cout << "After Merge sort:" << std::endl;
	for (unsigned int i = 0; i < testVec1.size(); i++)
		std::cout << testVec1[i] << " ";
	std::cout << "Merge sort took: " << time << "seconds" << std::endl;

	startQuickSort (testVec1);
	std::cout << "After Quick sort:" << std::endl;
	for (unsigned int i = 0; i < testVec1.size(); i++)
		std::cout << testVec1[i] << " ";
	std::cout << "Merge sort took: " << time << "seconds" << std::endl;

	system("PAUSE");
    return 0;
}

