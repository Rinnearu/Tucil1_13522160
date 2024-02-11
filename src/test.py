# seq = ["A1","FF","MK","KW","D9"]
# search = ["A1","FF"]

# print(search == search[:2])
# print("hello")
# print(__name__)

import random

my_set = {1, 2, 3, 4, 5}

# Specify the number of elements to select
n = 10
oberall = []

# Select random elements from the set with replacement
for _ in range(n):
    random_element = random.choice(list(my_set))
    oberall.append(random_element)

    print(random_element)

print(oberall)