# Define the input key-value lists
key1 = ["a", "b", "c", "d", "f", "g", "h", "e", "a"]
value1 = [20, 3, 1, 88, 55, 92, 6, 90, 910]

key2 = ["u", "b", "o", "x", "e", "a"]
value2 = [200, 30, 10, 88, 55, 920]

merged_dict = {**{k: v for k, v in zip(key1, value1) if v % 2 != 0}, **{k:v for k, v in zip(key2, value2) if v % 2 != 0}}

print(merged_dict)