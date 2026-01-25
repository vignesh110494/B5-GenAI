# newdictionary={
#     "name": "vignesh",
#     "age":   31,
#     "city":  "chennai"
# }
# print(newdictionary["city"])
# newdictionary["city"]="bangalore"
# print(newdictionary)

# newdictionary["age"] += 10
# print(newdictionary)

# print("Merging and updating dictionaries")
newdictionaryA={
    "name": "vignesh",
    "age":   31,
    "city":  "hosur"
}
newdictionaryB={
    "names": "Anchana",
    "ages":   26,
    "citys":  "Tiruvallur"
}
# print("newdictionaryA",newdictionaryA)
# print("newdictionaryB",newdictionaryB)

# mergeddictoinary = newdictionaryA.copy()
# print("mergeddictiaryafter1stcopy",mergeddictoinary)

# mergeddictoinary.update(newdictionaryB)
# print("mergeddictiary",mergeddictoinary)


print("updating the dictionary")

newdictionaryA.update({"age":32})
print("updatednewdictionaryA",newdictionaryA)
newdictionaryA.update({"newproperty":32})
print("UpdictionaryA",newdictionaryA)
print("UpdictionaryA",newdictionaryA["city"])


