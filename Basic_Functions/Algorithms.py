from __future__ import print_function
from __future__ import division
import math 

#the array input needs to be already sorted
def binary_search(array, start, end, key):
    if end >= 1:
        mid = start + (end-start)//2
        if array[mid] is key:
            return mid
        elif array[mid] > key:
            return binary_search(array, start, mid-1, key)
        # binary search the second half
        elif array[mid] < key:
            return binary_search(array, mid+1, end, key)
    return -1 #point where key is not present in the array anymore

    
'''Knuth's algorithm for uniform binary search:
    based on the idea that instead of having an upper bound,
    a lower bound and a midpoint, we use two ptrs: current
    position i and one for delta (rate of change)'''
def uniform_binary_search(array, i, delta, key):
    i = math.ceil(array.size()/2) #current position
    m = math.floor(array.size()/2) #num of current records
    if (key == array[i]):
        return i
    elif m is not 0: 
        if array[i] > key: 
            i = i - math.ceil(m/2)
            m = math.floor(m/2)
            return uniform_binary_search(array, i, m, key)
        else:
            i = i + math.ceil(m/2)
            m = math.floor(m/2)
            return uniform_binary_search(array, i, m, key)
        
# but don't need to maintain the value of m at all, we
# only need to refer to a short table of the various delta
# to use at each evel of the tree, alg is reduced to a lookup table
def delta_table(num, j):
    delta = []
    if j >= 1 and j <= math.floor(math.log(num[2])) + 2:
        delta[j] = math.floor(num + math.pow(2, j-1))
        j = j + 1
        return delta[j-1]
    return -1 #error

def uniform_binary_search_delta(array, i, delta, key):
    i = delta_table(array.size(), 0) - 1 #midpoint of array
    d = 0
    if key == array[i]:
        return i
    elif delta_table(array.size(), d) == 0:
        return -1
    else:
        if array[i] > key:
            d = d + 1
            i = i - delta_table(array.size(), d)
        elif array[i] < key:
            d = d + 1
            i = i + delta_table(array.size(), d)

def factorial(n): #this is better in dynamic programming
    if n == 1:
        return 1
    elif n > 1:
        return n*factorial(n-1)        
    return -1

def palidrome(word, start, end):
    length = word.length()
    if length == 0 or length == 1:
        return True
    if word[0] == word[length]:
        return True    
    return palidrome(word, start+1, end-1)

'''
If n is even, then x^n = (x^2)^(n/2)
If n is odd, then x^n = x * (x^2)^((n-1)/2)
'''
def powers_of_number(base, exponent):
    if exponent == 0:
        return 1
    #return powers_of_number(base, exponent-1) * base #this takes too much time if the base and exponent are large
    elif exponent%2 == 0 and exponent > 0: 
        print("even")
        return powers_of_number(base*base, exponent/2) 
    elif exponent%2 == 1 and exponent > 0:
        print("odd")
        return powers_of_number(base*base, (exponent-1)/2) * base 
    elif exponent < 0:
        return powers_of_number(base, exponent+1)/base
         

def insertion_sort(array):
    done = False
    i =  1
    while not done:
        j = i 
        temp = array[i]
        while temp < array[j-1] and j > 0:
            array[j] = array[j-1]
            j = j - 1
        array[j] = temp #put it into position
        i = i + 1
        if i >= len(array) or j >= len(array):
            done = True
        
def merge_sort(array):
    if len(array) > 1:
        mid = len(array)//2
        left_half = array[ :mid]
        right_half = array[mid: ] 
        merge_sort(left_half)
        merge_sort(right_half)
        
        left_index = 0   
        right_index = 0
        k = 0
        while left_index < len(left_half) and right_index < len(right_half):
            if left_half[left_index] < right_half[right_index]:
                array[k] = left_half[left_index]
                left_index = left_index + 1
            else: 
                array[k] = right_half[right_index]
                right_index = right_index + 1
            k = k + 1
        #exhaused arrays:
        #if left_index == len(left_half)-1:
        while right_index < len(right_half):
            array[k] = right_half[right_index]
            right_index = right_index + 1
            k = k + 1
                
        #if right_index == len(right_half)-1:
        while left_index < len(left_half):
            array[k] = left_half[left_index]
            left_index = left_index + 1
            k = k + 1

'''
uses left and right pointers to array elm to find correct partitioning 
locations separating partition index value 
'''
def swap(array, left, right):
    temp = array[left]
    array[left] = array[right]
    array[right] = temp
    
def partition(array, left, right):
    mid = left + (right-left)//2
    # make pivot the of array and swap it with leftmost elm
    pivot = array[mid]
    array[mid] = array[left]
    array[left] = pivot
    print("pivot in partition: ", pivot)
    forward = left + 1
    backward = right
    done = False
    # while forward <= backward: doesn't work
    while not done:
        while forward <= backward and array[forward] <= pivot:
           forward = forward + 1   
        while array[backward] >= pivot and backward >= forward:
           backward = backward - 1
        # should stop at this point when they are improperly placed 
        # array[forward] > pivot and when array[backward] < pivot
        if backward < forward:
            done = True #exit out of loop
        #if forward < backward:
        else:
            swap(array, forward, backward)
            
    # reach until they cross when backward < forward
    # swap backward and first to put mid back in partition position
    swap(array, left, backward)
    print ("array backward: ", backward)
    # return backward index
    return backward 

def quicksort(array, front, back):
    if front < back:
        pivot_position = partition(array, front, back)
        quicksort(array, front, pivot_position-1)
        quicksort(array, pivot_position+1, back)

if __name__ == '__main__':
    array = [54,26,93,17,77,31,44,55,20]
    print ("Original array:", array)
    quicksort(array, 0, len(array) - 1)
    print ("After quicksort: ", array)
    #insertion_sort(array)
    #merge_sort(array)
    #print(array)
    #print (powers_of_number(2, -1))
    print (binary_search(array, 0, len(array)-1, 31))