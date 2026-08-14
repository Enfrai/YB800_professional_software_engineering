from ucimlrepo import fetch_ucirepo

iris = fetch_ucirepo(id=53)

x = iris.data.features
y = iris.data.targets

print(f'The total number of records is {len(x)}')
print(f'The total number of different flower available is {y['class'].nunique()}')
print(f'The names of all diferent flowers are: {y['class'].unique().tolist()}')

# print(iris.metadata)

# print(iris.variables)