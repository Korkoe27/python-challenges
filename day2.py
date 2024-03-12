# Given an list nums of size n, return the majority element.

# The majority element is the element that appears more than ⌊n / 2⌋ times. You may assume that the majority element always exists in the array.

def most_frequent(List):
    counter = 0
    most_frequent_elements = []

    for i in List:
        curr_frequency = List.count(i)
        if curr_frequency > counter:
            counter = curr_frequency
            most_frequent_elements = [i]
        elif curr_frequency == counter and i not in most_frequent_elements:
            most_frequent_elements.append(i)

    return most_frequent_elements
 
List = [2,2,4,3,5,3,5]
print(most_frequent(List))