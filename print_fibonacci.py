"""
Develop a Python project that includes a "main" function and at least two additional functions. Your program should:
Ask the user to enter a number (N).
Print all values in the Fibonacci series up to N.
Calculate and print the factorial of N.
Once you have completed the project, push it to GitHub and share your GitHub repository link here.
"""
def print_fibonacci(terminal = 100):
    first = 0
    second = 1

    print(f'{first} {second}', end=' ')
    while True:
        third = first + second
        if terminal <= third:
            break

        print(f'{third}', end=' ')
        first = second
        second = third
        
    print('')

def calculate_factorial(base: int):
    if base < 0:
        print('invalid base')

    result = 1
    if base > 0:
        for i in range(1, base + 1):
            result *= i

    print(f'The factorial of {base} is {result}')
    

if __name__ == '__main__':
    maximum = int(input('Please input a maximum number of Fibonacci sequences: '))
    print_fibonacci(maximum)

    base = int(input('Please input a base of factorial: '))
    calculate_factorial(base)