# list =["one","two","three","four","five"]
# # print(list)
# list.append("six")
# print(list)

# for i in list:
#     print(i)
#     if i == "one":
#         print("found it at start")
#     elif i == "five":
#         print("ending the loop")
#     else:
#         print("not found")
#         continue


# Creating a list
list = [1, 2, 3, 4, 5]
print("Initial list:", list)

# append() – Adds an element at the end
list.append(6)
print("After append(6):", list)

# extend() – Adds multiple elements
list.extend([7, 8])
print("After extend([7, 8]):", list)

# insert() – Inserts element at a specific index
list.insert(2, 10)
print("After insert(2, 10):", list)

# remove() – Removes first occurrence of value
list.remove(10)
print("After remove(10):", list)

# pop() – Removes element by index (default last)
list.pop()
print("After pop():", list)

list.pop(1)
print("After pop(1):", list)

# clear() – Removes all elements
temp_list = list.copy()
temp_list.clear()
print("After clear():", temp_list)

# index() – Returns index of element
print("Index of 4:", list.index(4))

# count() – Counts occurrences of element
print("Count of 4 number:", list.count(4))

# sort() – Sorts the list
list.sort()
print("After sort():", list)

# reverse() – Reverses the list
list.reverse()
print("After reverse():", list)

# copy() – Creates a shallow copy
new_list = list.copy()
print("Copied list:", new_list)

# len() – Returns length of list
print("Length of list:", len(list))

# max() and min()
print("Maximum value:", max(list))
print("Minimum value:", min(list))

# sum()
print("Sum of list:", sum(list))

    