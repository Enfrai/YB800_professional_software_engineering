my_list = [1,3,5,7,9,11]
my_list[2:4] = [-3, -9, -11, -13]
print(my_list)

middle = int(len(my_list) / 2)
my_list[middle:middle] = [99, 98, 97, 96, 95, 94, 93, 92, 91, 90]
print(my_list)