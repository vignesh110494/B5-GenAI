# # print("python set datatype")
# # Techstack={"python","react","javascript"}
# # print(Techstack)
# # Techstack2={"aws","react","python",}
# # print(Techstack2) 

# # Techstack.add("Django")
# # print("After adding Django:",Techstack)

# # techstack3 = Techstack | Techstack2

# # print("After adding techsta1 and techstack2:",techstack3)

# # frozenset = frozenset(Techstack)
# # print("frozenset:",frozenset)

# set1 = {1, 2, 3, 4}
# set2 = {3, 4, 5, 6}

# print("Set 1:", set1)
# print("Set 2:", set2)

# # ---------- Set Operations ----------

# # Union
# print("\nUnion (set1 | set2):", set1 | set2)
# print("Union (set1.union(set2)):", set1.union(set2))

# # Intersection
# print("\nIntersection (set1 & set2):", set1 & set2)
# print("Intersection (set1.intersection(set2)):", set1.intersection(set2))

# # Difference
# print("\nDifference (set1 - set2):", set1 - set2)
# print("Difference (set2 - set1):", set2 - set1)

# # Symmetric Difference
# print("\nSymmetric Difference (set1 ^ set2):", set1 ^ set2)
# print("Symmetric Difference:", set1.symmetric_difference(set2))

# # ---------- Set Relationship Operations ----------

# # Subset
# print("\nIs set1 subset of set2?:", set1.issubset(set2))

# # Superset
# print("Is set1 superset of set2?:", set1.issuperset(set2))

# # Disjoint
# print("Are set1 and set2 disjoint?:", set1.isdisjoint(set2))

# # ---------- Set Methods ----------

# print("Set 1:", set1)
# print("Set 2:", set2)
# # Add element
# set1.add(10)
# print("\nAfter add(10):", set1)

# # Update (add multiple elements)
# set1.update([11, 12])
# print("After update([11, 12]):", set1)

# # Remove element
# set1.remove(11)
# print("After remove(11):", set1)

# # Discard element (no error if not found)
# set1.discard(10)
# print("After discard(10):", set1)

# # Pop random element
# removed = set1.pop()
# print("Popped element:", removed)
# print("After pop():", set1)

# # Copy
# set_copy = set1.copy()
# print("Copied set:", set_copy)

# # Clear
# set1.clear()
# print("After clear():", set1)

# frozen set with loop example
# Frozensets representing students enrolled in courses
python_students = frozenset(["A", "B", "C", "D"])
java_students   = frozenset(["C", "D", "E"])

print("Python students:", python_students)
print("Java students:", java_students)

# Find common students using intersection
common_students = python_students & java_students

print("\nCommon students in both courses:")

# Loop through the frozenset result
for student in common_students:
    print(student)

