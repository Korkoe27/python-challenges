# You are given the heads of two sorted linked lists list1 and list2.

# Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists.

# Return the head of the merged linked list.



def sortLists(list1, list2):
    list1.sort()
    list2.sort()
    list3 = list1+list2
    list3.sort()
    print(list3)


sortLists([1,2,4], [1,3,4])


# list1 = [19,309,42580,234,321,2343]

# list1.sort

# print(list1)