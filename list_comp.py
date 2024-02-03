# List comprehension example

# Given the list of integers, find the square of each element in the list and make new list of squares.

nums = [1, 2, 3, 5, 6, 7]
squares = []

print(nums)

print("Using classic for loop:")

# Classic for loop
for num in nums:
    squares.append(num * num)

print(squares)

# List comprehension
# [expression for variable in sequence]
print("Using list comprehension:")
squares = [x * x for x in nums]
print(squares)

print("Cube of all integeres between 10 and 20")

print([x**3 for x in range(10, 21)])

print("Split hyphenated words")
hwords = ["karun-subramanian", "vani-karun", "sarvajith-karun", "samy-karun"]
print([word.split("-") for word in hwords])

# print cubes of integers between 10 and 20 that are not multiples of 3
print([x**3 for x in range(10, 21) if x % 3 != 0])

# Find all characters in a string that is alphabetic:
mystring = "Karun is 46 years old"
print([x for x in mystring if x.isalpha() == True])

mylist = [1, 2, 3, 4, 5]
print("My list")
print(mylist)
double_of_odd_integers = [x * 2 for x in mylist if x % 2 != 0]
print("Double of odd integers")
print(double_of_odd_integers)
