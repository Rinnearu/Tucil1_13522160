# seq = ["A1","FF","MK","KW","D9"]
# search = ["A1","FF"]

# print(search == search[:2])
# print("hello")
# print(__name__)

# list1 = [1, 2, 3, 4, 5]
# list2 = [3, 4]
# if any(list2 == list1[i:i+len(list2)] for i in range(len(list1) - len(list2) + 1)):
#     print("Yes, {} is a subsequence of {}.".format(list2, list1))
# else:
#     print("No, {} is not a subsequence of {}.".format(list2, list1))

buffer_sequence = [1, 2, 3]
checked_sequence = buffer_sequence

# Modify checked_sequence
checked_sequence[0] = 100

print(buffer_sequence)   # Output: [100, 2, 3]
print(checked_sequence)  # Output: [100, 2, 3]