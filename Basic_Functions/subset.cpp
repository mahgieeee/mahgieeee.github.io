#include <iostream>
#include <set>
#include <list>


/*function that retuns a list of all the n-elm subsets of a given set
if the given set is [1,2,3] and n is 2, then the returned list should contain [1,2], [1,3], and
[2,3]. The order of the elements is not important.*/
template <typename T>
std::list<std::set<T>> subSet(std::set<T> &s, int num){
	std::list<T> tempList;
	std::set<T> tmpSet;
	std::set <T> :: iterator iterFront, iterNext; 
	if (num==0)
		tmpList.insert(tmpSet);//emptyList
		
	else if (num==1){ //copy the set as a list 
		while(iterFront!=s.end()){
				tmpList.insert(*iterFront); //copies combinations in subsets [num,num2]
				iterFront++;
		}
	}
	
	else if (num>1){
		iterFront=s.begin(); //points to first elm, (1,2)...(1 3) (2 2)
		iterNext=iterFront;
		while (iterFront!=s.end()){
			while(iterNext!=s.end()){
				for (int i=0; i<num; i++){
					tmpSet.insert(*iterFront); //copies combinations in subsets [num,num2]
					tmpSet.insert(*(iterNext+1)); 
					tempList.insert(subSet(s),i); //inserts each subset into list
				}
				iterNext++; //move on to the next iterator 
			}
			s.erase(iterFront);//removes first elm since all is copied with first elm in it
			iterFront++;
		}
	}
	return tempList;
}

template <typename T>
void printList(std::list<T> &argList){
	std::list<T>::iterator iter;
	for (iter=argList.begin(); iter<argLst.end(); iter++)
		std::cout << *iter << " ";
}

int main(){
	int n, int num;
	std::set <int> s;
	std::list <set<int>> returnList;
	std::cout << "Enter set.size() : "
	std::cin >> n;
	
	for (int i=0; i<n; i++)
		s.insert(i); //numbers 1...n
	
	std::cout << "Enter num : "
	std::cin >> num;
	
	returnList=subset(s,num);
	printList(returnList);
}
