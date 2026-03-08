from functools import reduce

numbers = [1, 2, 3, 4, 5]

# map() example
squared = list(map(lambda x: x**2, numbers))
print("Squared numbers:", squared)

# filter() example
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", even_numbers)

# reduce() example
sum_numbers = reduce(lambda a, b: a + b, numbers)
print("Sum of numbers:", sum_numbers)