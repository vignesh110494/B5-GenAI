'''
for i in range(9,10):
   # print(i)

    list = [1,2,3,4,5,6,7,8,9]
    for i in list:
        print(i)
        if i == 5:
            break
'''
my_dict = {
    "name": "vignesh",
    "age": 31,
    "city": "Hosur"
}

#loop key
# for key in my_dict:
    # print(key)
    #  print(my_dict[key])

#loop values
# for value in my_dict.values():
#      print(value)

# Loop through keys and values
# for key,value in my_dict.items():
#     print(key, ":-", value)

# Loop through keys and values with index
# for index, (key, value) in enumerate(my_dict.items()):
#     print(index, key, value)


#convert the two list into a dictionary
list1 = ["name","age"]
list2=  ["vignesh",31]  
dictionarysample = {}
print (range(len(list1)))

for i in range(len(list1)):
    dictionarysample[list1[i]] = list2[i]

print(dictionarysample)